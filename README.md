<img width="1600" height="837" alt="First page" src="https://github.com/user-attachments/assets/1a91a311-a615-40b0-adee-ab4843d8520e" />
# n8n Personal Assistant Web App

A Streamlit-based personal assistant UI connected to an n8n webhook workflow.

## What this project does

- Chat interface for assistant-style interactions
- Sends user messages to an n8n webhook
- Displays AI/workflow response in the app
- Includes a simple webhook test script (`test_webhook.py`)

## Tech stack

- Python
- Streamlit
- Requests
- n8n (local or hosted)

## Step-by-step setup

### 1. Clone the repository

```bash
git clone https://github.com/PrinceVerma04/n8n-automation.git
cd n8n-automation
```

### 2. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install streamlit requests
```

### 4. Start n8n

Run n8n locally (default is port `5678`) and make sure your workflow is active.

### 5. Configure webhook URL and timeout

This app reads:

- `N8N_WEBHOOK_URL`
- `N8N_REQUEST_TIMEOUT` (seconds)

Example:

```bash
export N8N_WEBHOOK_URL="http://127.0.0.1:5678/webhook/<your-webhook-id>"
export N8N_REQUEST_TIMEOUT=60
```

### 6. Run the Streamlit app

```bash
streamlit run app.py
```

Open the local URL shown in terminal (usually `http://localhost:8501`).

### 7. Send a test message

Type a message in the chat input and verify:

- request reaches n8n webhook
- response returns in valid JSON format (`output` key expected)

## Optional webhook test (CLI)

Edit webhook URL/message in `test_webhook.py`, then run:

```bash
python test_webhook.py
```

## Current known issue

- Calendar event scheduling is not working properly yet.
- This will be fixed in a future update.
- Overall assistant workflow and chat experience are working well.

## Common errors and fixes

### `Failed to call webhook` / timeout

- Confirm n8n is running
- Confirm `N8N_WEBHOOK_URL` is correct
- Increase timeout:

```bash
export N8N_REQUEST_TIMEOUT=90
```

### Docker/local host issue

If app is inside Docker, `localhost` points to container itself. Use `host.docker.internal` or host IP.

## Project files

- `app.py` -> main Streamlit app
- `test_webhook.py` -> webhook connectivity/debug test
- `.gitignore` -> ignored local artifacts

## Learning reference

This project is inspired by CampusX (Nitish Sir) playlist:

`Complete n8n Masterclass [Updated for 2026]: Build Real-World Automations and AI Agents from Scratch`

## Next targets

- Schedule meetings by student roll number
- Task assignment and tracking for classroom workflows
- Update class test sheets automatically
- Summarize notes/PDFs

