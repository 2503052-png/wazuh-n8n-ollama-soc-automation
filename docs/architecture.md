# Architecture

## Data flow

1. Endpoint telemetry is collected by Wazuh agents or configured log sources.
2. Wazuh manager decodes events and evaluates detection rules.
3. Matching alerts are selected for forwarding by a custom integration.
4. n8n receives the alert as JSON through its Webhook node.
5. n8n optionally filters alerts and calls the Ollama chat API.
6. The AI result and relevant original fields are sent to the configured analyst mailbox.

## Lab networking

In this lab, Wazuh is on Ubuntu Server in VMware NAT and n8n is a Docker container on the Windows host. A VMnet8 host address can allow the Ubuntu VM to reach a host-published n8n port. The exact address depends on local VMware configuration.

Within Docker, `localhost` refers to the container itself. `host.docker.internal` is commonly used by Docker Desktop containers to reach a service on the host. Verify that Ollama is reachable from the n8n container before testing the workflow.

## Trust boundaries

- Wazuh alert payloads are untrusted input.
- Ollama's output is advisory and may be inaccurate.
- Email delivery may disclose security information; use a mailbox you control.
- Keep the webhook, n8n editor, and Ollama API off the public internet unless protected appropriately.
