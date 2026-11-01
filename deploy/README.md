# Deploying to the client EC2 VM

Deployment procedure for Amazon Linux 2023, reviewed 1 November 2026.
The public HTTPS sign-in page and authenticated dashboard were observed; installed
units, instance inventory, network controls and renewal jobs were not inspected.
Use the operator-confirmed hostname instead of historical IP addresses.
See [handover status](../docs/handover-status.md) for unverified operational facts.

Layout on the VM:

    /opt/chatbot/.venv          virtualenv (python3.12)
    /opt/chatbot/app            this repository
    /opt/chatbot/app/mvp_demo   Django project, working directory of the service

## 1. System packages

    sudo dnf install -y python3.12 python3.12-pip git

Amazon Linux 2023 ships Python 3.9, which is too old: Django 6.0 requires 3.12+.

## 2. Code

    sudo mkdir -p /opt/chatbot && sudo chown -R ec2-user:ec2-user /opt/chatbot
    git clone --depth 1 -b <branch> https://github.com/sheharahewawasam/Triple-A-Super_Chatbot.git /opt/chatbot/app

## 3. Dependencies

Install torch from the CPU index FIRST. The default PyPI wheel on Linux bundles
CUDA and costs roughly 2.5GB, which will not fit; installing it first also stops
sentence-transformers pulling the CUDA build in as a dependency.

    python3.12 -m venv /opt/chatbot/.venv
    /opt/chatbot/.venv/bin/pip install --upgrade pip
    /opt/chatbot/.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
    /opt/chatbot/.venv/bin/pip install -r /opt/chatbot/app/mvp_demo/requirements.txt

## 4. Configuration

`secrets.env` is not in the repository. Create it from
`mvp_demo/secrets.env.template` (or copy the real one) at
`/opt/chatbot/app/mvp_demo/secrets.env` and `chmod 600` it. Required:

    PINECONE_API_KEY, PINECONE_INDEX_NAME
    DJANGO_SECRET_KEY
    DJANGO_DEBUG=False
    DJANGO_ALLOWED_HOSTS=<the VM's hostname or IP>

Optional overrides: `OLLAMA_URL`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT_SECONDS`,
`DJANGO_CORS_ORIGINS`.

`DJANGO_ALLOWED_HOSTS` must be set: with `DEBUG=False` and no value the app
accepts no hosts at all, by design, so a misconfigured deploy fails loudly
rather than answering on any hostname.

## 5. Database

    cd /opt/chatbot/app/mvp_demo
    /opt/chatbot/.venv/bin/python manage.py migrate

Migrations create the schema and seed advisers/funds. New adviser accounts have
unusable passwords until individually provisioned:

    /opt/chatbot/.venv/bin/python manage.py changepassword <username>

Existing migrated databases are unchanged: update each account separately.
The SQLite file is created locally and must be included in a coordinated backup.

## 6. Service

    sudo cp /opt/chatbot/app/deploy/chatbot.service /etc/systemd/system/
    sudo touch /var/log/chatbot-access.log /var/log/chatbot-error.log
    sudo chown ec2-user:ec2-user /var/log/chatbot-*.log
    sudo systemctl daemon-reload && sudo systemctl enable --now chatbot

Check with `systemctl status chatbot` and `journalctl -u chatbot -n 50`.

## 7. Language model

Install/start Ollama and pull the configured answer model. Check available RAM,
disk and actual runtime versions on the target host; old capacity notes do not
establish current installation status. Chat requires model inference even when
sign-in and other endpoints are working.

    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull qwen3:1.7b

## Source PDFs and access

Place authorised source PDFs outside the checkout, normally in
`/opt/chatbot/documents`, and set `SOURCE_DOCUMENT_DIRS` accordingly. The application
serves citations through signed grants at `/api/source/`; a working link requires
the corresponding local PDF. Never expose the source directory as public static files.
Use [backup and restore](../docs/backup-and-restore.md) before replacing a host.

Use the configured HTTPS hostname, normally `triple-a-chatbot.duckdns.org`.
For authorised diagnostics through SSH, forward to the loopback application port:

    ssh -i <key>.pem -N -L 8080:localhost:8000 ec2-user@<host>

Then open http://localhost:8080. Do not open port 8000 publicly to make this work.
The committed service uses one Gunicorn worker and binds to `127.0.0.1:8000`;
confirm the effective installed unit and firewall rules. Each process loads its
own model resources. Capacity and latency must be measured on the actual host;
see [evaluation](../docs/evaluation.md) for dated results. Log rotation and backup
execution still require operator confirmation.

## 8. TLS

Use a hostname and a valid certificate for browser access. The public HTTPS page
loaded without a certificate warning during the 1 November check; that does not
verify certificate renewal. The steps below configure or rebuild TLS rather than
describe an unfinished current installation. Use a client-controlled hostname or
the established DuckDNS name accepted by the certificate automation.

### 8a. A name that resolves here

Either a subdomain of a domain the client controls (an A record to this
instance's public IP), or a free DuckDNS subdomain.

For DuckDNS: create the subdomain at https://www.duckdns.org, then keep it
current, because an EC2 public IP that is not Elastic changes on stop/start and
a stale record breaks both the site and certificate renewal:

    sudo install -m 700 -o ec2-user -g ec2-user \
        /opt/chatbot/app/deploy/duckdns-update.sh /opt/chatbot/duckdns-update.sh
    printf 'DUCKDNS_DOMAIN=yourname\nDUCKDNS_TOKEN=your-token\n' > /opt/chatbot/duckdns.env
    chmod 600 /opt/chatbot/duckdns.env
    /opt/chatbot/duckdns-update.sh && echo updated
    sudo systemctl edit --force --full chatbot-duckdns.service

Use this unit (the protected environment file supplies the token):

    [Unit]
    Description=Refresh chatbot DuckDNS address
    [Service]
    Type=oneshot
    User=ec2-user
    EnvironmentFile=/opt/chatbot/duckdns.env
    ExecStart=/opt/chatbot/duckdns-update.sh

Create `chatbot-duckdns.timer` with `sudo systemctl edit --force --full chatbot-duckdns.timer`:

    [Unit]
    Description=Refresh chatbot DuckDNS periodically
    [Timer]
    OnBootSec=1min
    OnUnitActiveSec=5min
    [Install]
    WantedBy=timers.target

Then enable it and inspect the result:

    sudo touch /var/log/duckdns.log
    sudo chown ec2-user:ec2-user /var/log/duckdns.log
    sudo systemctl daemon-reload
    sudo systemctl enable --now chatbot-duckdns.timer
    systemctl list-timers chatbot-duckdns.timer

This is a proposed setup procedure; the installed refresh schedule has not been verified.

`DUCKDNS_DOMAIN` is the subdomain only - `yourname`, not `yourname.duckdns.org`.

### 8b. The certificate

Wait until the name resolves to this instance, then:

    sudo /opt/chatbot/app/deploy/enable-tls.sh yourname.duckdns.org you@example.com

That installs certbot, names the nginx server blocks (certbot matches on
`server_name`, and they ship as `_`), requests the certificate, adds the
80 -> 443 redirect, enables the renewal timer, and sets the four environment
variables below before restarting the service.

### 8c. Why Django needs changing too

nginx terminates TLS, so Django receives a plain HTTP request even when the
browser used HTTPS. Left alone, `request.is_secure()` is False and Django
rejects the browser's `https://` Origin on every POST - sign-in fails with a
CSRF error over HTTPS while working perfectly over HTTP. Four variables in
`secrets.env` fix it, all set by the script:

    DJANGO_TRUST_PROXY_PROTO=true              # trust nginx's X-Forwarded-Proto
    DJANGO_CSRF_TRUSTED_ORIGINS=https://<host> # Origin is compared with scheme
    DJANGO_SECURE_COOKIES=true                 # session/CSRF cookies HTTPS-only
    DJANGO_ALLOWED_HOSTS=...,<host>            # the new name

`DJANGO_TRUST_PROXY_PROTO` is safe only when network isolation ensures that only
nginx can reach Gunicorn. The source template binds to loopback; verify the
effective installed unit and security-group rules. If
gunicorn were ever exposed directly, a client could send the header itself and
claim to be secure.

Leave all four unset for local development - the defaults keep plain HTTP
working.

### 8d. The bare IP

certbot writes its redirect as `if ($host = <name>)`, which only fires when the
Host header matches the certificate. That same block is also the default server
for port 80, so a request to `http://<ip>/` fell straight through it and was
served unencrypted - the whole application, sign-in included. The port 80 block
here redirects unconditionally instead. Renewal is unaffected: Let's Encrypt
follows redirects when fetching the HTTP-01 challenge, which should be checked with `certbot renew --dry-run` on the target host.

### 8e. Verifying

    curl -sS -o /dev/null -w '%{http_code}\n' https://<host>/           # 200, no -k
    curl -sS -o /dev/null -w '%{http_code} %{redirect_url}\n' http://<host>/   # 301 to https
    sudo certbot certificates                                           # expiry
    systemctl list-timers certbot-renew.timer

Then sign in through a real browser: a padlock with no warning, and the login
POST succeeding, is what confirms 8c is right.

HSTS is deliberately not enabled. Browsers cache it for months, so it is
painful to unwind if the hostname changes - worth adding once the name is
final.

## 9. CI/CD (GitHub Actions)

Three workflows in `.github/workflows/`:

| Workflow | Runs on | What it checks |
|---|---|---|
| `tests.yml` | pushes except main; PRs into main; reusable call from deploy workflow | system checks, migration consistency, all 37 rag_api tests |
| `retrieval.yml` | PRs to `main` that touch chunking or retrieval; or by hand | `eval_retrieval.py` against live Pinecone: fails below 8/10 |
| `deploy.yml` | every push to `main`; or by hand | the unit tests, then deploys to this VM |

The unit tests run with `RAG_OFFLINE=1`, which stops `rag_api/resources.py`
loading Pinecone and the models. No test uses them, and without the switch CI
would need a live key and ~1.4GB of downloads just to import the views.

`workflow_dispatch` ("Run workflow" in the Actions tab) only appears once the
workflow file is on `main`.

### 9a. Retrieval recall

Add repository secrets `PINECONE_API_KEY` and `PINECONE_INDEX_NAME` under
Settings > Secrets and variables > Actions.

### 9b. Deployment

The deploy job is gated by `DEPLOY_ENABLED=true`; current enablement and
production-environment approvals remain unverified. `deploy/remote-deploy.sh` is piped to the VM over SSH. It
refuses if tracked files on the VM have been edited by hand. Otherwise it checks
out the exact commit that was tested, runs `pip install -r` and `migrate`,
restarts `chatbot`, and waits up to 5 minutes for `/api/auth/me/` to answer. If
the service does not come back it restores the previous code; packages and
migrations are not rolled back.

1. **A key for GitHub only.** Do not upload `RAG_Server.pem`. A separate key can
   be revoked without locking anybody out:

       ssh-keygen -t ed25519 -N "" -C github-actions-deploy -f chatbot-deploy
       ssh -i <key>.pem ec2-user@<host> 'cat >> ~/.ssh/authorized_keys' < chatbot-deploy.pub

2. **The host key**, so the runner can verify it is talking to this VM:

       ssh-keyscan -t ed25519 triple-a-chatbot.duckdns.org

3. **Settings > Environments > New environment `production`.** Add yourself
   under Required reviewers to approve each deploy by hand. Then add these
   environment secrets:

   | Secret | Value |
   |---|---|
   | `VM_HOST` | `triple-a-chatbot.duckdns.org` (the DuckDNS name follows IP changes) |
   | `VM_SSH_KEY` | the whole of `chatbot-deploy`, the private half |
   | `VM_KNOWN_HOSTS` | the `ssh-keyscan` output line |

4. **Settings > Secrets and variables > Actions > Variables:**
   `DEPLOY_ENABLED` = `true`.

5. **Port 22 must be reachable from GitHub's runners.** Their addresses change
   with every run. If the security group only allows SSH from your own IP, the
   deploy step times out at "Deploy". Use an approved runner-access rule
   or a suitably restricted self-hosted runner. Confirm the chosen network policy with the account owner.

Changes to `deploy/chatbot.service` or the nginx config are not applied
automatically; install those by hand as in sections 6 and 8.
