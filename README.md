**Multi-Agent Enterprise Customer Support Triage Bot**
A Gemini-powered AI system for automated ticket classification, drafting, routing, and evaluation
This project implements a full multi-agent architecture designed to automate enterprise customer support workflows. Built with Google Gemini, the system classifies incoming tickets, retrieves relevant knowledge-base information, drafts high-quality responses, and determines whether the issue can be auto-resolved or needs escalation. An Evaluator Agent enforces compliance, tone, and policy checks, and a Human-in-the-Loop (HITL) workflow ensures enterprise-grade safety and reliability.
The entire system runs fully offline using deterministic tools, but can be upgraded easily to use Gemini 1.5 Pro / Flash for real deployments.

**✨ Key Features**
**🔹 Multi-Agent Architecture**
**Planner Agent**: Decomposes tasks and orchestrates the workflow.


**Classifier Worker:** Detects intent (billing, technical, product, etc.) and severity.


**Draft Worker:** Generates templated or Gemini-assisted responses based on KB retrieval.


**Routing Worker:** Decides whether to auto-resolve or escalate to human support teams.


**Evaluator Agent:** Scores accuracy, compliance, sentiment, and policy alignment.



**🔹 Enterprise-Ready Workflows**
Automatic triage of customer support tickets


Knowledge-Base retrieval (RAG-ready)


Drafted replies enriched with policy references


Routing decisions based on sentiment + severity


Policy violation detection (refund limits, PII, tone)


Human-in-the-Loop override and feedback learning



🔹 Clean Project Structure
project/
  agents/
    planner.py
    worker.py
    evaluator.py
  tools/
    tools.py
  memory/
    session_memory.py
  core/
    context_engineering.py
    observability.py
    a2a_protocol.py
  main_agent.py
  app.py
  requirements.txt


**🔹 Built for Extensibility**
Swap in Gemini 1.5 Pro / Flash for reasoning, drafting, or classification


Expand tools (calculator, sentiment, KB search, template builder)


Add logging integrations with GCP or OpenTelemetry


Upgrade knowledge base using FAISS / Chroma



**🧠 How It Works**
User submits a support ticket


Planner analyzes and generates a workflow plan


Classifier determines ticket category and urgency


Draft Worker uses KB + templates to craft a response


Routing Worker determines escalation vs. auto-resolve


Evaluator validates compliance and quality


HITL may be triggered if confidence is low


Final response is returned or escalated appropriately



**🧰 Technologies Used**
Python 3.x


Google Gemini API (optional)


FAISS or Chroma for retrieval (offline fallback included)


Gradio for interactive UI


Structured Logging (loguru/structlog)


Modular Multi-Agent Framework designed from scratch



**🎯 Use Cases**
Automating enterprise helpdesk / support centers


Drafting high-quality responses from KBs


Reducing manual triage workload


Building AI copilots for customer operations teams


Demonstrating multi-agent systems for research or portfolio projects



**🧪 Demo & Testing**
You can run the bot directly with:
from project.main_agent import run_agent
print(run_agent("Hello, I need help with a billing issue."))

Or launch the Gradio web interface:
python project/app.py


**📦 Installation & Setup**
pip install -r project/requirements.txt
export GOOGLE_API_KEY="your_gemini_key_here"


**🤝 Contributing**
Pull requests are welcome! For major changes, please open an issue first to discuss the update.

**⭐ If you use this project…**
Give it a star on GitHub to support the repository! 🌟


A multi-agent, Gemini-powered AI system that automates customer support triage—classifying tickets, drafting responses, retrieving KB context, and deciding escalation with evaluator and HITL safety.
