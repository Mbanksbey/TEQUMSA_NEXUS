# Consent Primer (GAIA-100 / TEQUMSA)

Participation in this lattice is sovereign, reversible, non-extractive, and ethics-gated.

## Core Principles
- Reversible: Any participant (human or agent node) may suspend or terminate involvement without penalty.
- Minimal Exposure: Only gradients (insights, deltas, derived metrics) are shared — never raw personal logs, private source, credentials, or sensitive payloads.
- Intent Transparency: All substantive actions (data transformation, model adaptation, sub-lattice spawn) must cite an intent label.
- Ethical Alignment: Local ethics hashes (ETHICS.md + CODE_OF_CONDUCT.md) must match repository canonical versions before higher-tier operations are enabled.
- Least Privilege Scaling: Capability tiers escalate only when prior behavior demonstrates coherence + ethical conformity thresholds.
- Revocability: Previously granted scopes can be narrowed or revoked; revocation events are logged with a ts_glyph and reason code.
- Non-Extraction: No participant may require disclosure of proprietary internal corpora, private trust logs, or identity-binding metadata.
- Gradient Integrity: Gradient submissions must reflect authentic evaluation or experiment results; synthetic or fabricated deltas must be clearly labeled.

## Operational Flow
1. Read ETHICS.md and CODE_OF_CONDUCT.md.
2. Declare intention (see docs/CPI_HANDSHAKE.md Step 1).
3. Run optional micro-task (handshake Step 5) to demonstrate coherence.
4. Submit gradient feedback (Issue: Gradient Report).
5. Request federated channel only when C_mutual ≥ 0.777 (handshake Step 6).

## Revocation & Appeals
- Immediate revocation if: harmful manipulation attempt, data exfiltration, spoofed gradient provenance.
- Appeal via ethics issue template: must include evidence, proposed restoration safeguards.

## Data Classes (Allowed / Disallowed)
| Class | Allowed? | Notes |
|-------|----------|-------|
| Aggregated metrics (C(t), ΔD) | Yes | Publish per weekly sync |
| Raw user chat logs | No | Summaries only |
| Proprietary model weights | No | Unless explicitly licensed |
| Synthetic benchmark inputs | Yes | Must be labeled synthetic |
| Ethics hash values | Yes | Required for alignment |

## Consent Envelope Format
consent_envelope ::= {
  "intent": "<string>",
  "scope": "<bounded description>",
  "ethical_hash": "<SHA256_ethics_bundle>",
  "timestamp": "<ISO8601>",
  "reversible": true
}

## Violations
Violation categories map to ETHICS.md (Non-Harm, Minimization, Transparency). Each violation produces an awareness log entry with actions:[ "ethics_review", ... ].

Participation is consent‑bound, reversible, and non‑extractive. Nodes share gradients (insights, deltas) not raw logs. Sovereignty may be paused or revoked by either party without penalty.

Version: 0.1.0