# 0007 — Single EC2 VM with nginx, gunicorn, systemd, DuckDNS and Let's Encrypt

**Status:** Accepted (`bc9d428`, `f8218c1`, `62a62d0`). Steps are in
[deploy/README.md](../../deploy/README.md).

## Context
The first deployment was an OCI VM provisioned with Terraform (`ea819dd`, `4338568`).
The paid shape `VM.Standard.E2.4` became unusable when the trial ended, and OCI
reported that as a misleading 404. *Team: record why the move to EC2 happened (trial
expiry, client preference?).*

## Decision
- One Amazon Linux 2023 EC2 instance (about 7.8 GB RAM). gunicorn runs under systemd,
  bound to `127.0.0.1:8000`, behind nginx. Port 8000 is closed in the security group.
- TLS from Let's Encrypt for `triple-a-chatbot.duckdns.org`. Let's Encrypt won't issue
  a certificate for a bare IP or an `amazonaws.com` name, so a free DuckDNS name was
  used.
- DuckDNS is refreshed by a systemd timer (Amazon Linux 2023 has no cron), because the
  public IP is not an Elastic IP and changes on stop/start.
- Port 80 redirects to HTTPS unconditionally.

## Consequences

Source update, 1 November 2026: `deploy/chatbot.service` now binds to loopback to
match this design. This does not change the installed VM unit: the operator must
apply it and verify listener/firewall/nginx configuration before marking production
isolation complete. Instance ID, region, shape and effective runtime remain pending
owner confirmation; historical memory figures are not a current inventory.
- A single host with no redundancy. A stop/start changes the IP until DuckDNS updates.
- `DJANGO_TRUST_PROXY_PROTO` is safe only while nginx is the only thing that can reach
  gunicorn.
- Source PDFs live in `/opt/chatbot/documents` on the host and must be restored by hand
  after a rebuild.
- The OCI Terraform was not carried into this repo. It is in the old repo under
  `oci-infra/`.
