"""
Quick test script to verify email sending works with Resend
"""
import os
from dotenv import load_dotenv
import resend

load_dotenv(override=True)


def test_resend_email(recipient_email=None):
    """Test sending email via Resend API"""

    if not recipient_email:
        recipient_email = input(
            "Enter your email address for testing: ").strip()
        if not recipient_email or "@" not in recipient_email:
            print("❌ Invalid email address")
            return False

    resend_api_key = os.getenv("RESEND_API_KEY")

    if not resend_api_key:
        print("❌ RESEND_API_KEY not found in environment variables")
        print("Please add it to your .env file")
        return False

    print(f"✅ Found Resend API key: {resend_api_key[:10]}...")

    try:
        resend.api_key = resend_api_key

        params = {
            "from": "onboarding@resend.dev",
            "to": recipient_email,
            "subject": "Test Email from Deep Research App",
            "html": "<h1>Success!</h1><p>Your Resend email integration is working perfectly! 🎉</p>"
        }

        print(f"Sending test email to {recipient_email}...")
        r = resend.Emails.send(params)

        print(f"✅ Email sent successfully!")
        print(f"Email ID: {r.get('id', 'N/A')}")
        print(f"Check your inbox at {recipient_email}")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Resend Email Integration")
    print("=" * 60)
    test_resend_email()
