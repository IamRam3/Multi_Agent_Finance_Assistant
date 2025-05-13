#input_analyzer_agent requirements
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import re
import json

class InputAnalyzerAgent:
    def __init__(self, groq_api_key: str, model_name: str):
        self.groq_api_key = groq_api_key
        self.model_name = model_name
        if not self.groq_api_key:
            raise ValueError("Groq API key is required.")
        if not self.model_name:
            raise ValueError("Model name is required.")
        self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=model_name)

    def analyze_input(self, query: str) -> str:
        extract_prompt = PromptTemplate(
            input_variables=["query"],
            template="""
You are a financial input parser. Given a user query, extract:
1. Relevant stock tickers (use real tickers, e.g., TSM for TSMC, SSNLF for Samsung if possible).
2. The user intent: 'stock_data', 'earnings', 'news', or 'all'.
Example: "How is Apple doing today?" → tickers: ["AAPL"], intent: "stock_data"
User query: {query}
Respond in format JSON only"
""")
        extract_chain = LLMChain(llm=self.llm, prompt=extract_prompt)
        response = extract_chain.run(query)
        
                # Strip markdown and text around JSON
        try:
            # Extract JSON block using regex
            json_match = re.search(r"{[\s\S]*?}", response)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError(f"Failed to extract JSON: {response}")
        except Exception as e:
            raise ValueError(f"Invalid JSON format from model: {e}")

