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
def send_email(subject: str, html_body: str):
    """
    Send an email with the given subject and HTML body.

    Args:
        subject: The email subject line
        html_body: The email body content in HTML format
    """
    from_email = os.getenv("GMAIL_EMAIL")
    password = os.getenv("GMAIL_APP_PASSWORD")

    if not password:
        print("❌ Error: GMAIL_APP_PASSWORD not found in environment variables")
        return "Error: Email credentials not configured"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = "yongpengfu0011@gmail.com"
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587, timeout=5) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            print("✅ Email sent successfully!")
            return "Email sent successfully"
    except Exception as e:
        error_msg = f"Email sending failed: {e}"
        print(f"⚠️  {error_msg}")
        print("⚠️  Note: Email sending may not work on Hugging Face Spaces (SMTP blocked)")
        # Don't fail - just return a warning so the report is still displayed
        return "⚠️ Email unavailable on this platform (SMTP blocked). Report displayed below instead."


INSTRUCTIONS = """You are an email sending agent.
When given a report, you should:
1. Try to send it as a well-formatted HTML email using the send_email tool
2. If email sending fails (e.g., on restricted platforms), that's okay - the user will still see the report

Always attempt to use your send_email tool, but don't worry if it fails."""

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

    report = "Latest AI Agent frameworks in 2025"
    result = await send_email_report(report)
    logger.info(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
