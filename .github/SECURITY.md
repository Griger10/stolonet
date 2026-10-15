# Security Policy

## Supported versions

Security fixes target the latest code on the default branch. Older releases and
forks do not have a separate security maintenance commitment.

## Reporting a vulnerability

Please report suspected security vulnerabilities of any severity privately to
[griger1011@gmail.com](mailto:griger1011@gmail.com). Use a subject such as
`[Stolonet Security] Short description`.

Do not open a public issue or pull request containing vulnerability details,
exploit code, credentials, or sensitive telemetry before a fix is available and
disclosure has been coordinated.

Include as much of the following as possible:

- Affected component (backend API, MQTT ingestion, frontend, simulator, or
  deployment configuration) and commit or version.
- A description of the vulnerability, its potential impact, and any required
  access or configuration.
- Minimal steps to reproduce, with a proof of concept if available.
- Relevant logs or screenshots with secrets and personal data removed.
- A suggested fix, if you have one.

If you are unsure whether an issue has security implications, use the private
reporting channel. Ordinary bugs without security impact can be reported through
public issues or pull requests.

The ESP32 firmware is maintained in the separate
[stolonet-node repository](https://github.com/Griger10/stolonet-node). Mention that
repository when reporting a firmware issue, and describe any impact on this
platform.

## Handling and disclosure

Reports are reviewed on a best-effort basis; there is no guaranteed response or
resolution time. The maintainer may ask for additional details to reproduce and
assess the issue, and coordinate a fix and public disclosure with the reporter.

Please keep vulnerability details private while a fix is being prepared and
agree on disclosure timing with the maintainer. Let the maintainer know whether
you would like to be credited in any public advisory.

## Responsible testing

Test only systems you own or have explicit permission to assess. Prefer a local
deployment with synthetic telemetry. Avoid disrupting services, publishing
messages to other people's devices, or accessing, modifying, or deleting their
data. If you encounter exposed credentials or private data, stop testing and
report the finding privately without including live secrets in the report.
