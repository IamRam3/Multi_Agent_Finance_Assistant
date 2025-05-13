#api_agent requirements
import yfinance as yf
from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.agents import Tool
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any


class APIAgent:
    def __init__(self):
        self.news_tool = YahooFinanceNewsTool()

    def get_stock_data(self, ticker: str) -> Dict[str, Any]:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="2d")
            earnings = stock.earnings_dates

            return {
                "ticker": ticker,
                "latest_price": hist["Close"].iloc[-1],
                "prev_close": hist["Close"].iloc[-2],
                "earnings_date": earnings.index[-1] if not earnings.empty else None,
                "earnings_surprise": earnings["Surprise(%)"].iloc[-1] if not earnings.empty else None,
            }
        except Exception as e:
            return {"error": f"Failed to fetch stock data for {ticker}: {str(e)}"}

    def get_news(self, query: str, use_fallback=True) -> str:
        try:
            # Assume query is a ticker for primary method
            return self.news_tool.run(query)
        except Exception as e:
            if use_fallback:
                return self.scrape_yahoo_news(query)
            return f"NewsTool failed: {str(e)}"

    def scrape_yahoo_news(self, query: str) -> str:
        try:
            search_query = query.replace(" ", "+")
            url = f"https://finance.yahoo.com/lookup?s={search_query}"
            headers = {
                "User-Agent": "Mozilla/5.0"
            }
            response = requests.get(url, headers=headers)
            #print("response : ", response)
            print("--" * 20)
            soup = BeautifulSoup(response.text, "lxml")
            
            #print("soup : ", soup)
            print("--" * 20)

            headlines = soup.find_all("h3")
            print("headlines : ", headlines)
            print("--" * 20)
            top_news = [h.get_text(strip=True) for h in headlines[:5]]

            return "\n".join(top_news) if top_news else "No headlines found."
        except Exception as e:
            return f"Fallback scraping failed: {str(e)}"



if __name__ == "__main__":
    agent = APIAgent()

    print("=== TSMC Stock Data ===")
    print(agent.get_stock_data("TSM"))

    print("\n=== News via Ticker (TSM) ===")
    print(agent.get_news("TSM"))

    '''print("\n=== News via Keyword (fallback) ===")
    print(agent.get_news("TSMC earnings"))'''

