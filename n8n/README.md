# n8n workflow setup

## Recommended nodes

`Webhook -> (optional IF filter) -> HTTP Request (Ollama) -> Send Email`

### Webhook

- Method: `POST`
- Path: `wazuh-alert`
- Use the Production URL for an active/published workflow.
- Secure the endpoint before use outside a private lab.

### HTTP Request (Ollama)

- Method: `POST`
- URL: `http://host.docker.internal:11434/api/chat`
- Body content type: JSON
- Response should include `message.content`.
- Replace `llama3.2:3b` with a model actually installed on your machine.

Example request body is in `../README.md`.

### Send Email

- Configure SMTP credentials using n8n's credential manager.
- For Gmail SMTP, use the provider's supported authentication method; with Gmail this commonly means an App Password with 2-Step Verification enabled.
- Do not put passwords in node fields as plain text or export them to GitHub.
- If the Send Email node directly follows Ollama's HTTP Request, the AI response is commonly `{{$json.message.content}}`.
- To include both the original alert and AI output, use a Merge node or safely reference the Webhook node's data from the same execution.

## Importable starter workflow

`workflow-template.json` is a sanitized starter template with placeholders. Review and configure it in your own n8n instance before activating it. Do not assume it contains your personal credentials or your exact existing workflow.
