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

# For email (choose one):
# Option 1: Resend API (recommended, works everywhere)
RESEND_API_KEY=your-resend-api-key

# Option 2: Gmail SMTP (local only, doesn't work on HF Spaces)
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-gmail-app-password
```

3. Run the app:

```bash
python deep_research.py
```

## Deployment to Hugging Face Spaces

✅ **Email Now Works on Hugging Face Spaces!** We use Resend API which works via HTTP instead of SMTP.

### Option 1: Using Gradio CLI

```bash
uv run gradio deploy
```

When prompted, enter these secrets:

- `OPENAI_API_KEY`: Your OpenAI API key
- `RESEND_API_KEY`: Your Resend API key (get free key at https://resend.com)

### Option 2: Manual Deployment

1. Create a new Space on Hugging Face
2. Upload all Python files
3. Upload `requirements.txt`
4. In Settings → Repository secrets, add:
   - `OPENAI_API_KEY`
   - `RESEND_API_KEY`

## How to Get Resend API Key (Recommended)

1. Go to https://resend.com and sign up (free tier available)
2. Verify your email
3. Go to API Keys section
4. Click "Create API Key"
5. Copy the API key (starts with `re_`)
6. Add it to your `.env` file or Hugging Face Secrets

**Free tier includes:**

- 100 emails/day
- 3,000 emails/month
- Perfect for demos and personal projects!

## How to Get Gmail App Password (For Local Use - Optional)

If you prefer to use Gmail SMTP locally instead of Resend:

1. Go to Google Account: https://myaccount.google.com/
2. Security → 2-Step Verification (must be enabled)
3. App Passwords → Create new app password
4. Copy the generated 16-character password
5. Use this password (not your regular Gmail password)

**Note:** The app will automatically try Resend first, then fall back to Gmail SMTP if available.

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
- Resend API (email delivery - works on all platforms)
- Gmail SMTP (email delivery fallback for local use)
