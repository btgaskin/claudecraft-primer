"""Dependency-free checks for the installable skill package."""
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "claudecraft-primer"


class PackageTests(unittest.TestCase):
    def test_explicit_invocation_metadata(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertTrue(skill.startswith("---\n"))
        header = skill.split("---", 2)[1]
        self.assertRegex(header, r"(?m)^name: claudecraft-primer$")
        self.assertRegex(header, r"(?m)^description: .+$")
        self.assertRegex(header, r"(?m)^disable-model-invocation: true$")
        metadata = (ROOT / "agents/openai.yaml").read_text()
        self.assertIn("  allow_implicit_invocation: false", metadata)
        self.assertIn("$claudecraft-primer", metadata)

    def test_local_links_stay_inside_package_and_resolve(self):
        for source in ROOT.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", source.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (source.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT), (source, target))
                self.assertTrue(resolved.is_file(), (source, target))

    def test_install_collision_and_removal_preserve_neighbor(self):
        with tempfile.TemporaryDirectory() as tmp:
            for client in (".claude", ".agents"):
                parent = Path(tmp) / client / "skills"
                parent.mkdir(parents=True)
                neighbor = parent / "another-skill"
                neighbor.mkdir()
                (neighbor / "keep.txt").write_text("preserve")
                destination = parent / NAME
                shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns(".git", "__pycache__"))
                self.assertEqual((destination / "SKILL.md").read_bytes(), (ROOT / "SKILL.md").read_bytes())
                self.assertTrue((destination / "references/evidence.md").is_file())
                with self.assertRaises(FileExistsError):
                    shutil.copytree(ROOT, destination)
                moved = Path(tmp) / (client + "-removed")
                destination.rename(moved)
                self.assertFalse(destination.exists())
                self.assertTrue((moved / "SKILL.md").is_file())
                self.assertEqual((neighbor / "keep.txt").read_text(), "preserve")

    def test_distribution_has_no_symlinks_or_machine_paths(self):
        for base in (ROOT / "SKILL.md", ROOT / "agents", ROOT / "references"):
            paths = base.rglob("*") if base.is_dir() else [base]
            for path in paths:
                self.assertFalse(path.is_symlink(), path)
                if path.is_file():
                    text = path.read_text()
                    self.assertNotIn("/Users/", text)
                    self.assertNotIn("/private/tmp/", text)

    def test_documented_clone_and_project_export(self):
        blocks = re.findall(r"```sh\n(.*?)```", (ROOT / "README.md").read_text(), re.S)
        with tempfile.TemporaryDirectory(prefix="claudecraft install ") as tmp:
            base = Path(tmp)
            source = base / "source"
            shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            def git(*args):
                return subprocess.run(
                    ["git", "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
                     "-c", "user.name=Package Test", "-c", "user.email=test@example.invalid", *args],
                    cwd=source, check=True, capture_output=True, text=True)
            git("init", "-q", "-b", "main")
            git("add", ".")
            git("commit", "-qm", "Temporary installation fixture")
            for client, block in zip((".claude", ".agents"), blocks[:2]):
                command = block.replace("$HOME", str(base / "personal"))
                command = command.replace("https://github.com/btgaskin/claudecraft-primer.git", '"' + str(source) + '"')
                target = base / "personal" / client / "skills" / NAME
                def install():
                    return subprocess.run(["sh", "-c", command], cwd=source, check=True, capture_output=True, text=True)
                install()
                self.assertEqual((target / "SKILL.md").read_bytes(), (source / "SKILL.md").read_bytes())
                sentinel = target / "local-edit.txt"
                sentinel.write_text("keep")
                self.assertIn("already exists", install().stdout)
                self.assertEqual(sentinel.read_text(), "keep")
                shutil.rmtree(target)
                target.mkdir()
                self.assertIn("already exists", install().stdout)
                self.assertFalse((target / "SKILL.md").exists())
                target.rmdir()
                target.symlink_to(base / "missing-target")
                self.assertIn("already exists", install().stdout)
                self.assertTrue(target.is_symlink())
            target = base / "project" / ".claude" / "skills" / NAME
            export = blocks[2].replace("/absolute/path/to/project/.claude/skills/claudecraft-primer", str(target))
            subprocess.run(["sh", "-c", export], cwd=source, check=True, capture_output=True)
            self.assertEqual((target / "SKILL.md").read_bytes(), (source / "SKILL.md").read_bytes())
            self.assertFalse((target / ".git").exists())
            result = subprocess.run(["sh", "-c", export], cwd=source, check=True, capture_output=True, text=True)
            self.assertIn("already exists", result.stdout)


if __name__ == "__main__":
    unittest.main()
