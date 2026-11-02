# 0007 — Single EC2 VM with nginx, gunicorn, systemd, DuckDNS and Let's Encrypt

**Status:** Accepted (`bc9d428`, `f8218c1`, `62a62d0`). Steps are in
[deploy/README.md](../../deploy/README.md).

## Context
The first deployment was an OCI VM provisioned with Terraform (`ea819dd`, `4338568`).
The paid shape `VM.Standard.E2.4` became unusable when the trial ended, and OCI
reported that as a misleading 404. Research on 2 November 2026 found that
`4338568` explicitly documents this limit and changes the OCI configuration to
`VM.Standard.A1.Flex`. Later, `bc9d428` identifies the EC2 systemd unit as the
one running on the client host. The supported explanation is that the paid OCI
shape could not continue under the expired trial and EC2 became the deployment
target. The history does not prove this was the sole reason for choosing AWS;
indeed, an alternative OCI shape was attempted first.

## Decision
- Target: one Amazon Linux 2023 EC2 instance, with Gunicorn managed by systemd
  on `127.0.0.1:8000` behind nginx. Application port 8000 must be restricted.
  Current instance shape/memory and effective network controls need operator verification.
- TLS from Let's Encrypt for `triple-a-chatbot.duckdns.org`. Let's Encrypt won't issue
  a certificate for a bare IP or an `amazonaws.com` name, so a free DuckDNS name was
  used.
- Use a systemd timer to refresh DuckDNS when the host uses a changing public IP.
  The installed refresh schedule and Elastic IP allocation are unverified.
- Port 80 redirects to HTTPS unconditionally.

## Consequences

Source update, 1 November 2026: `deploy/chatbot.service` now binds to loopback to
match this design. This does not change the installed VM unit: the operator must
apply it and verify listener/firewall/nginx configuration before marking production
isolation complete. Historical memory figures are not a current inventory.
- A single host with no redundancy. A stop/start changes the IP until DuckDNS updates.
- `DJANGO_TRUST_PROXY_PROTO` is safe only while nginx is the only thing that can reach
  gunicorn.
- Source PDFs live in `/opt/chatbot/documents` on the host and must be restored by hand
  after a rebuild.
- The OCI Terraform was not carried into this repo. It is in the old repo under
  `oci-infra/`.

## Research sources

Repository history reviewed on 2 November 2026:

- [Original commit `4338568`](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/commit/4338568a135d2843265580c1ca272c14bac2f4c0)
- [Original commit `bc9d428`](https://github.com/sheharahewawasam/FIT-4002-CHATBOT/commit/bc9d4280ec8bb8a5b5ad40d35a8f2c2d21e45c29)
