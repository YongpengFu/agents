"""
Quick test script to verify email sending works with Resend
"""
import os
from dotenv import load_dotenv
import resend

load_dotenv(override=True)


def test_resend_email():
    """Test sending email via Resend API"""

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
            "to": "yongpengfu0011@gmail.com",
            "subject": "Test Email from Deep Research App",
            "html": "<h1>Success!</h1><p>Your Resend email integration is working perfectly! 🎉</p>"
        }

        print("Sending test email...")
        r = resend.Emails.send(params)

        print(f"✅ Email sent successfully!")
        print(f"Email ID: {r.get('id', 'N/A')}")
        print(f"Check your inbox at yongpengfu0011@gmail.com")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Resend Email Integration")
    print("=" * 60)
    test_resend_email()
