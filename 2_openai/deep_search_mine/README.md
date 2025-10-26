---
title: deep_research
app_file: deep_research.py
sdk: gradio
sdk_version: 5.34.2
---

# Deep Research Agent

An AI-powered research assistant that performs web searches, writes comprehensive reports, and sends them via email.

## Features

- **Intelligent Planning**: Uses AI to plan relevant web searches
- **Concurrent Searching**: Performs multiple searches in parallel
- **Report Writing**: Synthesizes findings into a comprehensive report
- **Email Delivery**: Sends the report via Gmail

## Local Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your credentials:

```
OPENAI_API_KEY=your-openai-key-here
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
```

3. Run the app:

```bash
python deep_research.py
```

## Deployment to Hugging Face Spaces

⚠️ **Important**: Email functionality does not work on Hugging Face Spaces because SMTP ports are blocked for security. The app will still generate and display reports, but emails won't be sent.

For full email functionality, run the app locally or deploy to a platform that allows SMTP (like AWS, GCP, or your own server).

### Option 1: Using Gradio CLI

```bash
uv run gradio deploy
```

When prompted, enter these secrets:

- `OPENAI_API_KEY`: Your OpenAI API key
- `GMAIL_EMAIL`: Your Gmail address (optional, email won't work on HF Spaces)
- `GMAIL_APP_PASSWORD`: Your Gmail app password (optional, email won't work on HF Spaces)

### Option 2: Manual Deployment

1. Create a new Space on Hugging Face
2. Upload all Python files
3. Upload `requirements.txt`
4. In Settings → Repository secrets, add:
   - `OPENAI_API_KEY`
   - `GMAIL_EMAIL`
   - `GMAIL_APP_PASSWORD`

## How to Get Gmail App Password (For Local Use)

1. Go to Google Account: https://myaccount.google.com/
2. Security → 2-Step Verification (must be enabled)
3. App Passwords → Create new app password
4. Copy the generated 16-character password
5. Use this password (not your regular Gmail password)

## Email on Hugging Face Spaces - Alternative Solutions

Since SMTP is blocked on Hugging Face Spaces, you have these options:

### Option 1: Accept No Email (Current)

- Report is displayed in the UI
- Users can copy/paste or download the report

### Option 2: Use HTTP-Based Email API

Replace Gmail SMTP with services that work via HTTP API:

- **Resend** (https://resend.com) - Modern email API
- **SendGrid** (https://sendgrid.com) - Popular email service
- **Mailgun** (https://mailgun.com) - Developer-focused

Example with Resend:

```python
import httpx

async def send_email_via_api(subject: str, html_body: str):
    api_key = os.getenv("RESEND_API_KEY")
    response = await httpx.post(
        "https://api.resend.com/emails",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "from": "research@yourdomain.com",
            "to": "yongpengfu0011@gmail.com",
            "subject": subject,
            "html": html_body
        }
    )
    return response.status_code == 200
```

### Option 3: Deploy Elsewhere

Deploy to platforms that allow SMTP:

- **Railway** (https://railway.app)
- **Render** (https://render.com)
- **AWS/GCP** with proper security groups
- **Your own VPS**

## Usage

1. Enter your research query in the text box
2. Click "Run" or press Enter
3. Watch the progress updates
4. The final report will be displayed and emailed to you

## Architecture

- **PlannerAgent**: Analyzes query and plans web searches
- **SearchAgent**: Executes web searches concurrently
- **WriterAgent**: Synthesizes research into a comprehensive report
- **EmailAgent**: Formats and sends the report via email
- **ResearchManager**: Orchestrates the entire workflow

## Technology Stack

- OpenAI Agents SDK
- Gradio (UI)
- Python asyncio (concurrent execution)
- Gmail SMTP (email delivery)
