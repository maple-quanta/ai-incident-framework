# Security and sensitive-data handling

MQ-AICIR records can be more sensitive than ordinary application logs. They may describe credentials, exploitable boundaries, affected parties, investigative hypotheses, or legal assessments.

- Never place a live token, password, private key, session cookie, or secret value in an incident record.
- Preserve evidence in a controlled evidence system and store a reference plus digest in MQ-AICIR.
- Apply least privilege, encryption, retention, legal hold, and secure deletion appropriate to the handling marking.
- Review generated reports before distribution. Automatic redaction is defense in depth, not a substitute for data minimization.
- The local UI binds to loopback only and has no authentication. Do not expose it through a reverse proxy or bind it to an external interface.
- Treat custom regular expressions and rules as trusted administrator configuration. Severity YAML never executes expressions or code.
- Report suspected vulnerabilities privately to Maple Quanta through the security contact published on `maplequanta.ca`; do not include real client evidence in a public issue.

The synthetic examples contain no live credentials, systems, organizations, or incident facts.

