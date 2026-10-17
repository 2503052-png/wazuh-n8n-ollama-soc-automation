# Wazuh manager integration notes

This folder documents the Wazuh-to-n8n integration. Wazuh custom integrations commonly run on the manager and receive alert data, then send selected alerts to an external service.

## Before changing configuration

1. Back up `/var/ossec/etc/ossec.conf`.
2. Confirm your installed Wazuh version and review its matching official custom-integration documentation.
3. Decide which alert levels/rules should be forwarded to avoid sending excessive noise.
4. Protect the receiving Webhook with authentication or network restrictions before using outside an isolated lab.
5. Test with a controlled alert and review `/var/ossec/logs/ossec.log` for integration errors.

## Example endpoint

Use your actual reachable host address, not `localhost` from Ubuntu. In this lab, the Windows host's VMnet8 address was used to reach n8n's published port. Example only:

`http://<WINDOWS_VMNET8_IP>:5678/webhook/wazuh-alert`

Do not commit local IPs if you consider them sensitive.

## Example integration script

`local-integration-example.py` is an illustrative starting point, not a drop-in replacement for Wazuh's required integration interface. Validate arguments and payload format against your installed Wazuh version before use. It intentionally reads the alert JSON path provided by the Wazuh integration mechanism and uses a configurable URL; it does not embed secrets.
