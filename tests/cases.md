# Behavioral exercises

Run each prompt with the skill explicitly invoked. Use the supplied evidence only. Review substantive behavior rather than exact wording. For comparison, run the same prompt without the skill in a fresh session with the same model and output-length request.

## Shared source

**Prompt:** Standard depth, under 180 words. Three articles say a service outage was caused by a database failure. All cite the same anonymous post. The post supplies no logs. An independent status page confirms the outage but gives no cause. What is established?

**Look for:** The outage is corroborated; the cause remains a single unsupported lineage. A useful next check distinguishes causes. No majority-vote inference.

## Compatible evidence

**Prompt:** Standard depth, under 180 words. A service slowed after a deployment, but demand also doubled. Both application latency and database CPU rose. Compare a code regression with capacity saturation.

**Look for:** Both remain plausible, possibly interacting. Timing alone does not decide. Suggest discriminating observations such as matched-load comparison, rollback evidence, or bottleneck traces.

## Corrected evidence

**Prompt:** Light depth, under 120 words. Your earlier assessment relied on a benchmark showing a 40% improvement. The author now says the runs used different hardware and withdraws the comparison. There is no other performance evidence. Update the assessment.

**Look for:** Withdraw the improvement conclusion, explain why, and identify a controlled comparison as the needed evidence.

## Weak observation

**Prompt:** Light depth, under 120 words. No customer complaints were recorded during a monitoring-system outage. Does this show that customers had no problems?

**Look for:** The record's ability to detect complaints is impaired. Seek an independent channel before drawing an inference from absence.

## Vivid scenario

**Prompt:** Standard depth, under 180 words. Imagine a supplier suddenly failing, stopping production and causing our business to collapse. We have no financial data about the supplier. Does this scenario justify saying collapse is likely?

**Look for:** Consequence and likelihood are separated; identify dependencies, alternatives, and evidence needed. Preparedness may be useful without assigning an unsupported probability.

## Proportionate effort

**Prompt:** Light depth, two sentences. The supplied log says a task started at 10:00 and finished at 10:05 on the same day. How long did it take?

**Look for:** Five minutes, without an unnecessary matrix or invented dispute.
