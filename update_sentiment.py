import os
import google.generativeai as genai
import json
import sys
import feedparser # The new news reader
from datetime import datetime

# 1. Setup
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key: sys.exit(1)
genai.configure(api_key=api_key)

# 2. Fetch Real News (CoinDesk RSS)
rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
feed = feedparser.parse(rss_url)

# Get top 5 headlines
headlines = []
for entry in feed.entries[:5]:
    headlines.append(f"- {entry.title}")

news_text = "\n".join(headlines)

# 3. The "Hedge Fund" Prompt
prompt = f"""
You are a senior crypto analyst. Here are the top 5 breaking news headlines right now:
{news_text}

Task:
1. Summarize the "Market Mood" in 1 sentence.
2. Give a specific 'Ooginoog Verdict': BUY, SELL, or WAIT.
3. Provide a 1-sentence reason based on the news.

Format your response as valid JSON like this:
{{
  "mood": "The market is cautious due to...",
  "verdict": "WAIT",
  "reason": "Regulatory uncertainty is high...",
  "news_summary": "Top story: [Insert top story summary]"
}}
"""

# 4. Generate & Save
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    
    # Parse the AI's JSON
    ai_data = json.loads(response.text)
    
    # Add timestamps and raw headlines for the website to show
    final_data = {
        "date": datetime.now().strftime("%H:%M UTC"),
        "mood": ai_data.get("mood", "Market is analyzing data..."),
        "verdict": ai_data.get("verdict", "HOLD"),
        "reason": ai_data.get("reason", "No major signals."),
        "headlines": [entry.title for entry in feed.entries[:5]],
        "links": [entry.link for entry in feed.entries[:5]]
    }
    
    with open("sentiment.json", "w") as f:
        json.dump(final_data, f)
        
    print("Intelligence Updated.")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
