import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from agents import function_tool

from agents import Agent, WebSearchTool, trace, Runner, gen_trace_id, function_tool
from agents.model_settings import ModelSettings
from pydantic import BaseModel, Field
import os
import asyncio
import logging
from dotenv import load_dotenv
import resend

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

logger.info("Loading environment variables")
load_dotenv(override=True)
logger.info("Environment variables loaded")
# print out the environment variables
for key, value in os.environ.items():
    logger.info(f"{key}: {value}")


@function_tool
def send_email(recipient: str, subject: str, html_body: str):
    """
    Send an email with the given subject and HTML body using Resend API.
    Falls back to SMTP if Resend is not configured.

    Args:
        recipient: The email address to send to
        subject: The email subject line
        html_body: The email body content in HTML format
    """

    # Try Resend first (works on Hugging Face Spaces)
    resend_api_key = os.getenv("RESEND_API_KEY")
    if resend_api_key:
        try:
            resend.api_key = resend_api_key
            params = {
                "from": "onboarding@resend.dev",
                "to": recipient,
                "subject": subject,
                "html": html_body
            }
            r = resend.Emails.send(params)
            print(
                f"✅ Email sent successfully via Resend! ID: {r.get('id', 'N/A')}")
            return f"Email sent successfully via Resend to {recipient}"
        except Exception as e:
            error_msg = f"Resend email failed: {e}"
            print(f"⚠️  {error_msg}")
            # Continue to try SMTP fallback

    # Fallback to SMTP (for local development)
    from_email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if password and from_email:
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587, timeout=5) as server:
                server.starttls()
                server.login(from_email, password)
                server.send_message(msg)
                print("✅ Email sent successfully via Gmail SMTP!")
                return f"Email sent successfully via Gmail to {recipient}"
        except Exception as e:
            error_msg = f"SMTP email failed: {e}"
            print(f"⚠️  {error_msg}")

    # Both methods failed or no credentials configured
    print("⚠️  Email sending unavailable - no valid credentials configured")
    print("⚠️  Set RESEND_API_KEY for Hugging Face Spaces or GMAIL credentials for local use")
    return "⚠️ Email unavailable (no credentials configured). Report displayed below instead."


INSTRUCTIONS = """You are an email sending agent.

When you receive a message with format "Send this report to: [email]\n\nReport:\n[content]":
1. Extract the recipient email address from the message
2. Extract the report content
3. Create an appropriate subject line based on the report content
4. Convert the report into well-formatted HTML
5. Use the send_email tool with the recipient email, subject, and HTML body

Important:
- The recipient parameter should be the exact email address extracted from the input
- Make the HTML email beautiful and well-structured
- If email sending fails, that's okay - the user will still see the report"""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)


def get_email_agent():
    return email_agent


async def send_email_report(report: str):
    logger.info(f"Sending email report: {report}")
    result = await Runner.run(get_email_agent(), report)
    # logger.info(f"Email result: {result.final_output}")
    return result.final_output


async def main():
    report = """
    # Research Report: Latest AI Agent Frameworks in 2025

    # Overview
    Based on comprehensive research, here are the top AI agent frameworks:

    1. ** LangGraph ** - Advanced state management for agents
    2. ** CrewAI ** - Multi-agent orchestration platform
    3. ** AutoGen ** - Microsoft's agent framework
    
    ## Conclusion
    The AI agent ecosystem continues to evolve rapidly in 2025.
    """

    # report = "Latest AI Agent frameworks in 2025"
    result = await send_email_report(report)
    logger.info(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
