# AI-Powered SOC Automation Lab

A hands-on home-lab project integrating **Wazuh SIEM**, **n8n workflow automation**, and **Ollama local LLMs** to support security-alert triage and email notifications.

> **Status note:** This repository is a reusable project template. Update the validation checklist and screenshots to reflect what you have personally tested. Do not claim end-to-end AI analysis and email delivery are verified until you have tested a real Wazuh alert through every node.

## Project goals

- Collect and detect security events with Wazuh.
- Forward selected Wazuh alerts to an n8n Webhook.
- Send alert context to a locally hosted Ollama model for AI-assisted triage.
- Email the analysis to an analyst.
- Preserve the original alert and keep a human in the loop.

## Architecture

```text
Windows endpoint / configured logs
              |
              v
        Wazuh Agent
              |
              v
   Wazuh Manager (Ubuntu VM)
   rules -> alerts.json
              |
      custom integration
              |
              v
       n8n Webhook (Docker)
              |
              v
    HTTP Request -> Ollama API
              |
              v
      Send Email (SMTP)
```

Example lab topology:

- Wazuh manager: Ubuntu Server in VMware.
- VMware networking: NAT (VMnet8).
- n8n: Docker container on the Windows host, published on port `5678`.
- Ollama: local service on Windows, typically port `11434`.

Use your own hostnames and addresses. Do not publish private IPs unless you intentionally want them public.

## Components

| Component | Role |
|---|---|
| Wazuh | Collects telemetry, applies detection rules, generates alerts |
| n8n | Receives alert JSON and orchestrates workflow steps |
| Ollama | Runs a local language model for alert explanation |
| SMTP email node | Sends analyst notification |

## Suggested repository structure

```text
wazuh-n8n-ollama-soc-automation/
├── README.md
├── .gitignore
├── LICENSE
├── docs/
│   ├── architecture.md
│   ├── testing-checklist.md
│   └── linkedin-post.md
├── wazuh/
│   ├── README.md
│   └── local-integration-example.py
├── n8n/
│   ├── README.md
│   └── workflow-template.json
├── prompts/
│   └── soc-triage-system-prompt.txt
└── screenshots/
    └── README.md
```

## Workflow logic

1. Wazuh detects an event and creates an alert.
2. A Wazuh custom integration forwards selected alert JSON to the n8n production Webhook.
3. n8n passes the alert payload to Ollama using its HTTP API.
4. Ollama returns a text analysis.
5. n8n sends an email with alert details and the AI assessment.

**Important:** Merely creating a Webhook does not make n8n read Wazuh log files. Wazuh must be configured to send alerts to that endpoint.

## Ollama API example

Typical local API endpoint:

```text
POST http://host.docker.internal:11434/api/chat
```

Example JSON body (replace the model name with one installed locally):

```json
{
  "model": "llama3.2:3b",
  "messages": [
    {
      "role": "system",
      "content": "You are a SOC analyst assistant. Analyze only the supplied evidence. Identify suspicious indicators, explain uncertainty, and recommend investigation steps. Do not claim an attack is confirmed without sufficient evidence."
    },
    {
      "role": "user",
      "content": "Analyze this Wazuh alert JSON: {{ JSON.stringify($json) }}"
    }
  ],
  "stream": false
}
```

In n8n, ensure the expression is evaluated in the field rather than sent as literal text. The expression above assumes the HTTP Request node receives the alert JSON directly from the preceding node. If an upstream node changes the item structure, adjust the expression accordingly.

## n8n workflow outline

Recommended node sequence:

1. **Webhook** — `POST`, path `wazuh-alert`.
2. **IF** (optional) — filter on `rule.level` or other fields.
3. **HTTP Request** — `POST` to Ollama `/api/chat`.
4. **Send Email** — email the original alert summary and AI output.

When the HTTP Request node is immediately before Send Email, the AI response is usually available as `{{$json.message.content}}`. If you also need original alert fields, use a Merge node or reference the original Webhook node by its actual name in an expression, after ensuring that node is part of the same execution path.

## Wazuh integration notes

Wazuh supports custom integrations that can send alert data to external endpoints. Configure the integration on the Wazuh manager, select which alerts should be forwarded, and test using a controlled lab alert. See `wazuh/README.md` and validate the integration script against your installed Wazuh version before using it.

Do not overwrite existing configuration blindly. Back up `ossec.conf`, preserve current integrations, and validate service status after changes.

## Security considerations

- Keep the webhook private to your lab or protect it with authentication.
- Do not expose n8n or Ollama directly to the public internet.
- Use an SMTP app password or provider-supported credential; never commit passwords, API keys, tokens, or `.env` files.
- Treat alert fields as untrusted input. Logs can contain attacker-controlled strings and prompt-injection-like text.
- The model is advisory. Validate findings against original logs and other evidence.
- Begin with read-only triage. Do not automatically block accounts, isolate hosts, or delete files without approval and testing.
- Sanitize screenshots and exported workflows before publishing.

## Testing checklist

- [ ] Wazuh generates a controlled test alert.
- [ ] Alert arrives in the n8n Webhook execution.
- [ ] Ollama HTTP Request returns `message.content`.
- [ ] Email node sends a test email.
- [ ] A real Wazuh alert completes the entire workflow.
- [ ] Failure cases are checked (Ollama offline, SMTP failure, malformed alert).
- [ ] Secrets and private details are removed from public artifacts.

## Current project status

Update this section honestly before publishing:

- [x] Wazuh manager/dashboard available in Ubuntu VM.
- [x] n8n running in Docker.
- [x] Wazuh alert delivery to n8n verified (according to the project notes).
- [ ] Real alert successfully analyzed by Ollama end-to-end.
- [ ] Email notification verified for a real alert.
- [ ] Screenshots and workflow export sanitized and added.

## Screenshots

Add sanitized screenshots of:
1. Wazuh alert.
2. n8n workflow canvas.
3. Successful execution showing the Webhook and Ollama response.
4. Received test email (hide email addresses and sensitive content).

See `screenshots/README.md`.

## Disclaimer

For educational and authorized lab use only. AI output can be incorrect and is not a substitute for security investigation or incident-response procedures.
