# Testing Checklist

Record date, result, and notes for each test.

| Test | Expected result | Status |
|---|---|---|
| Send sample POST to n8n test Webhook | Webhook captures JSON | Pending/Update |
| Send alert from Wazuh integration | Production Webhook receives alert | Pending/Update |
| Call Ollama `/api/tags` from Windows | Installed model list returned | Pending/Update |
| Call Ollama from n8n container | HTTP Request succeeds | Pending/Update |
| Run real alert through Ollama | `message.content` contains analysis | Pending/Update |
| Send test email | Message received in inbox | Pending/Update |
| Full end-to-end test | Real alert -> AI analysis -> email | Pending/Update |
| Failure test: Ollama unavailable | Workflow failure handled visibly | Pending/Update |
| Failure test: SMTP credentials invalid | Email error visible; alert retained | Pending/Update |

Replace Pending/Update with actual results. Do not mark a test successful unless you ran it.
