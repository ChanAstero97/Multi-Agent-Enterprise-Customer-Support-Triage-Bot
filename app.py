import traceback
from loguru import logger
import gradio as gr
import time
import os

# Try to import run_agent from the project's main_agent module.
# We do this inside a function so the app can still start even if the import fails;
# errors will be logged and surfaced to users.
try:
    from project.main_agent import run_agent  # type: ignore
    _RUN_AGENT_AVAILABLE = True
except Exception as e:
    run_agent = None  # type: ignore
    _RUN_AGENT_AVAILABLE = False
    logger.add("spaces_app.log", level="ERROR", serialize=True)
    logger.error("Failed to import run_agent: {}", e)

# Configure JSON structured logging to file
logger.remove()
logger.add("spaces_app.log", rotation="10 MB", serialize=True, level="INFO")

# Helper: read last N lines from the log file for live display
def read_logs(max_lines=500):
    log_path = "spaces_app.log"
    if not os.path.exists(log_path):
        return "No logs yet."
    try:
        with open(log_path, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            # Read last ~64KB for safety
            block_size = 65536
            if size > block_size:
                f.seek(-block_size, os.SEEK_END)
            else:
                f.seek(0, os.SEEK_SET)
            data = f.read().decode(errors="replace")
        lines = data.strip().splitlines()[-max_lines:]
        # Show last entries (JSON per line)
        return "\\n".join(lines)
    except Exception as e:
        return f"Error reading log file: {e}\\n{traceback.format_exc()}"

# Core interaction: call run_agent and maintain session state
def submit(user_input, chat_history):
    """
    user_input: str - new user text
    chat_history: list of dicts [{\"role\":\"user\"/\"assistant\", \"text\": \"...\"}]
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    entry = {"role": "user", "text": user_input, "time": timestamp}
    if chat_history is None:
        chat_history = []
    chat_history.append(entry)

    logger.info("received_input", user_input=user_input, timestamp=timestamp)

    if not _RUN_AGENT_AVAILABLE:
        err_msg = ("Error: run_agent() is not available in project.main_agent. "
                   "Make sure your repository exposes project/main_agent.py with a run_agent(user_input: str) function.")
        logger.error("run_agent_missing", detail=err_msg)
        assistant_text = err_msg
    else:
        try:
            # Call the project's run_agent function
            assistant_text = run_agent(user_input)
            logger.info("agent_response", response=str(assistant_text), timestamp=time.strftime("%Y-%m-%dT%H:%M:%S%z"))
        except Exception as e:
            logger.exception("agent_call_failed")
            assistant_text = ("Agent invocation failed with an exception. "
                              "Check spaces_app.log for details.\\n\\n" + str(e) + "\\n" + traceback.format_exc())

    timestamp2 = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    chat_history.append({"role": "assistant", "text": assistant_text, "time": timestamp2})

    # Update logs readout
    logs = read_logs()
    # Prepare markdown transcript (no chat bubbles) - simple role + message stack
    md_lines = ["## Conversation"]
    for turn in chat_history:
        role = turn.get("role", "user")
        when = turn.get("time", "")
        text = turn.get("text", "")
        md_lines.append(f"**{role.upper()} ({when})**:\\n\\n{text}\\n---")
    transcript_md = "\\n".join(md_lines)

    return transcript_md, chat_history, logs

def refresh_logs():
    return read_logs()

# Build Gradio UI
with gr.Blocks(title="Universal Multi-Agent Runner (Generic)") as demo:
    gr.Markdown(\"\"\"
    # Universal Hugging Face Multi-Agent Runner
    This interface loads a public GitHub repository that exposes a **`project/main_agent.py`** with a **`run_agent(user_input: str)`** function.
    Enter prompts below and the app will call `run_agent` and display the response. All interactions are logged to `spaces_app.log` (JSON lines).
    \"\"\")

    with gr.Row():
        with gr.Column(scale=3):
            user_input = gr.Textbox(label="User input", placeholder="Type your prompt here...", lines=4)
            submit_btn = gr.Button("Submit")
            clear_btn = gr.Button("Clear Conversation")

        with gr.Column(scale=2):
            logs_panel = gr.Accordion("Logs (collapsible, live)", open=False)
            with logs_panel:
                logs_text = gr.Textbox(label="Live logs (last entries)", value=read_logs(), interactive=False, lines=20)
            notes = gr.Markdown("**Notes:** Logs are written to `spaces_app.log` in JSON format.")

    # Conversation output (Markdown-based; no chat bubbles)
    transcript = gr.Markdown("## Conversation\\n_No messages yet._")

    # Session state to hold chat history (list of dicts)
    state = gr.State([])

    # Wire up actions
    submit_btn.click(fn=submit, inputs=[user_input, state], outputs=[transcript, state, logs_text])
    clear_btn.click(lambda: ("## Conversation\\n_No messages yet._", [], read_logs()), inputs=[], outputs=[transcript, state, logs_text])
    # Refresh logs button (also allow manual refresh by clicking the logs area)
    logs_text.change(fn=refresh_logs, inputs=[], outputs=logs_text)

# Auto-launch gradio (required by the user's deployment spec)
demo.launch(server_name="0.0.0.0", server_port=7860)
