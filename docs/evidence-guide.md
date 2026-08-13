# Evidence preservation and data handling

## Principles

Preserve enough evidence to reconstruct consequential behaviour independently of the agent. Final model output alone is not a trace. Evidence should establish what the system was instructed to do, what it could technically do, what it attempted, what authorization decision occurred, what tools and identities acted, what target observed, and how containment and recovery were enforced.

MQ-AICIR stores evidence metadata and controlled references. It is not an evidence vault. Never put a live credential, private key, bearer token, session cookie, secret prompt value, or unnecessary personal information in the JSON record.

## Supported evidence types

- agent traces;
- prompts and system prompts;
- tool calls and tool responses;
- network, IAM, cloud, and application logs;
- model version;
- system configuration and policy version;
- a description of credentials available to the agent, without secret values;
- affected files;
- screenshots and forensic images;
- human communications and incident tickets; and
- other organization-defined evidence.

Each object records an ID, type, description, location, optional digest, collection time, collector, custody events, and whether the reference or artifact is redacted.

## Collection order

Collection priorities depend on the system, but responders should generally:

1. preserve volatile agent context, orchestration state, pending tool calls, workload identity, active network connections, and runtime configuration;
2. prevent log expiry and destructive autoscaling while maintaining safe containment;
3. snapshot relevant policy, model, tool, connector, and environment versions;
4. obtain independent target, IAM, network, and cloud-control-plane records;
5. document human approvals, alerts, stop decisions, and effective enforcement;
6. record files, external resources, scheduled actions, identities, and third-party artifacts created or changed; and
7. hash preserved artifacts using organization-approved tooling.

Containment can alter evidence. Document the tradeoff and prioritize safety, affected-party protection, and legal obligations over forensic purity.

## Evidence references

Use a controlled URI, case-system identifier, or vault path that authorized responders can resolve. A location such as `evidence://MQ-2026-0042/network-log` is preferable to embedding the log payload. Do not place secret-bearing query strings in a URI.

Digests should include the algorithm, for example `sha256:<hex>`. A digest supports integrity checking but does not establish provenance or custody by itself.

Timeline and corrective-action evidence references must identify evidence objects in the same record. Unknown references fail model validation.

## Chain of custody

Custody events record a timezone-aware timestamp, actor, action, and optional notes. Organization procedures should also cover original media, acquisition tooling, time synchronization, evidence seals, access history, immutable storage, transfer receipts, and legal hold.

## Redaction

Report generation applies conservative patterns for common API keys, bearer tokens, private-key blocks, password assignments, and known credential prefixes. HTML output is autoescaped. Custom patterns can be added at report time.

Redaction has limits:

- a secret may not match a known pattern;
- context can remain sensitive after the token is removed;
- hashes, file paths, hostnames, model prompts, and third-party identities can be sensitive;
- custom regular expressions require trusted administrator review; and
- the safest report is one that never received unnecessary secret material.

Review every report before distribution. Record redaction of source evidence, but do not treat automatic report redaction as an evidence-handling control.

## Handling and privacy

Choose `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, or `RESTRICTED` when the record is created, then reassess as facts change. Define distribution and retention using applicable contracts, records policy, privacy obligations, litigation hold, affected-party needs, and secure deletion requirements.

Collect only information necessary for response and assurance. Segregate health, biometric, employment, children's, fundamental-rights, and other sensitive personal information. Do not make the local UI externally reachable: it binds to loopback and provides no authentication.

## Notification caution

Regulatory notification requirements depend on jurisdiction, system classification, contractual obligations, and applicable law. This framework assists classification but does not provide legal advice.

Notification fields record assessment status and recipients; they do not calculate deadlines or send notices. Coordinate with legal counsel, privacy, security, affected-system owners, communications, insurers, contractual partners, and regulators as applicable.

