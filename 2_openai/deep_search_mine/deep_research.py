import gradio as gr
from research_manager import ResearchManager
from dotenv import load_dotenv

load_dotenv(override=True)


async def run(query: str):
    """Run the research manager and yield progress updates"""
    async for chunk in ResearchManager().run(query):
        yield chunk


with gr.Blocks() as ui:
    gr.Markdown("# Deep Research Agent")
    gr.Markdown("_Powered by OpenAI Agents & Resend Email_")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    run_button = gr.Button("Run Research", variant="primary")
    report = gr.Markdown(label="Report")
    run_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)
ui.launch(inbrowser=True)
