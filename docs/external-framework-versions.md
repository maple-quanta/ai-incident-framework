# External framework versions used by MQ-AICIR 1.0

Primary sources were checked on **12 August 2026**. Crosswalks are informative and do not claim compliance or exact legal equivalence.

| Framework | Version/date used | Status and implementation note | Primary source |
|---|---|---|---|
| Linux Foundation / Open Secure AI Alliance Shared AI Findings Exchange (SAFE) | RFC proposal, checked 12 August 2026; no stable version stated | **Draft / RFC / evolving.** MQ-AICIR maps proposal sections by title and does not invent identifiers or treat proposed timelines as legal deadlines. | [OpenSecureAIAlliance RFC proposal](https://github.com/OpenSecureAIAlliance/RFCs/blob/main/rfc-safe-proposal.md) |
| MITRE ATLAS | Content `v2026.07`, released 7 August 2026 | Living knowledge base. The release states 16 tactics, 101 techniques, 77 sub-techniques, 37 mitigations, and 68 case studies. MQ-AICIR pins technique identifiers used in its mapping to this content release. | [MITRE ATLAS data release v2026.07](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.07) |
| NIST SP 800-61 | Revision 3, final, April 2025 | Supersedes Rev. 2. It is an incident-response CSF 2.0 Community Profile. | [NIST SP 800-61 Rev. 3 final](https://csrc.nist.gov/pubs/sp/800/61/r3/final) |
| NIST AI RMF | AI RMF 1.0, 26 January 2023 | Voluntary framework with GOVERN, MAP, MEASURE, and MANAGE. NIST noted an AI RMF revision effort in 2026; MQ-AICIR 1.0 continues to map to the latest final 1.0 rather than a work in progress. | [NIST AI RMF 1.0 announcement](https://www.nist.gov/news-events/news/2023/01/nist-risk-management-framework-aims-improve-trustworthiness-artificial), [NIST AI standards update](https://www.nist.gov/artificial-intelligence/ai-standards) |
| OECD AI incident/hazard terminology | “Defining AI incidents and related terms,” 6 May 2024 | Distinguishes actual-harm incidents from potential-harm hazards and allows jurisdictional flexibility. | [OECD.AI publication page](https://oecd.ai/en/ai-publications/defining-ai-incidents-and-related-terms) |

## Verification policy

- Re-check sources before each MQ-AICIR release and record the date.
- Do not upgrade mappings automatically when a living framework changes.
- Preserve the version associated with historical incident references.
- Mark an entry `verification required` and omit its identifier when the primary source cannot be verified.
- Legal and regulatory mappings require qualified jurisdiction-specific review beyond this technical crosswalk.

