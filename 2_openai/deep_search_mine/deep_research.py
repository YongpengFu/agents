import gradio as gr
from research_manager import ResearchManager
from dotenv import load_dotenv

load_dotenv(override=True)


async def run(query: str, email: str):
    """Run the research manager and yield progress updates"""
    # Validate email only if provided
    if email and email.strip():
        if "@" not in email:
            yield "⚠️ Invalid email format. Please enter a valid email or leave blank to skip email."
            return
        email = email.strip()
    else:
        email = None  # No email provided

    async for chunk in ResearchManager().run(query, email):
        yield chunk


with gr.Blocks(theme=gr.themes.Default(primary_hue="blue")) as ui:
    gr.Markdown("# 🔬 Deep Research Agent")
    gr.Markdown(
        "_AI-powered research assistant with optional email delivery_")

    with gr.Row():
        with gr.Column(scale=2):
            query_textbox = gr.Textbox(
                label="Research Topic",
                placeholder="e.g., Latest trends in AI agents 2025",
                lines=2
            )
        with gr.Column(scale=1):
            email_textbox = gr.Textbox(
                label="Your Email (Optional)",
                placeholder="Leave blank to view report here only",
                value=""
            )

    run_button = gr.Button("🚀 Run Research", variant="primary", size="lg")

    gr.Markdown("---")
    report = gr.Markdown(label="Research Progress & Report")

    run_button.click(
        fn=run,
        inputs=[query_textbox, email_textbox],
        outputs=report
    )

ui.launch(inbrowser=True)
