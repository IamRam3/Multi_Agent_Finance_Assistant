#tool_router_agent requirements
import json

class ToolRouterAgent:
    def __init__(self, api_agent ):
        self.api_agent = api_agent

    def orchestrate_response(self, parsed: dict) -> str:
        try:
            tickers = parsed.get("tickers", [])
            intent = parsed.get("intent", "all")

            messages = []

            for ticker in tickers:
                if intent in ["stock_data", "all"]:
                    stock = self.api_agent.get_stock_data(ticker)
                    if "error" not in stock:
                        messages.append(f"{ticker} is trading at {stock['latest_price']} USD.")
                        if stock.get("earnings_surprise"):
                            messages.append(f"Earnings surprise: {stock['earnings_surprise']}%")

                if intent in ["news", "earnings", "all"]:
                    news = self.api_agent.get_news(ticker)
                    messages.append(f"News for {ticker}:\n{news}\n")

            return "\n".join(messages)

        except Exception as e:
            return f"Failed to orchestrate response: {str(e)}"


'''def orchestrate_response(parsed_json: str, api_agent) -> str:
    try:
        parsed = json.loads(parsed_json)
        tickers = parsed.get("tickers", [])
        intent = parsed.get("intent", "all")

        messages = []

        for ticker in tickers:
            if intent in ["stock_data", "all"]:
                stock = api_agent.get_stock_data(ticker)
                if "error" not in stock:
                    messages.append(f"{ticker} is trading at {stock['latest_price']} USD.")
                    if stock.get("earnings_surprise"):
                        messages.append(f"Earnings surprise: {stock['earnings_surprise']}%")

            if intent in ["news", "earnings", "all"]:
                news = api_agent.get_news(ticker)
                messages.append(f"News for {ticker}:\n{news}\n")

        return "\n".join(messages)

    except Exception as e:
        return f"Failed to orchestrate response: {str(e)}"


from api_agent import APIAgent
json_response = '{"tickers": ["TSM", "SSNLF"], "intent": "all"}'

print(json_response)

api_agent = APIAgent()
response = orchestrate_response(json_response, api_agent)
print("\n🧠 Response:\n", response)'''