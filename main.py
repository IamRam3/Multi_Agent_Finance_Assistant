from input_analyzer_agent import InputAnalyzerAgent
import os
from dotenv import load_dotenv
load_dotenv()
from api_agent import APIAgent
from tool_router_agent import ToolRouterAgent

query = "How is TSMC doing today? What about Samsung? Any news?"
InputAnalyzer = InputAnalyzerAgent(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="Gemma2-9b-It"
)
response = InputAnalyzer.analyze_input(
    query
)
print("=== Extracted Response ===")
print("Response: ", response)
# Compare this snippet from api_agent.py        

agent = APIAgent()
orchestrator = ToolRouterAgent(agent)
print("=== Orchestrated Response ===")
print("Response: ", orchestrator.orchestrate_response(response))

