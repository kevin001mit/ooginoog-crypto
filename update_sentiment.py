import os
import google.generativeai as genai
import json
from datetime import datetime

# 1. Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 2. The Prompt
# We ask Gemini to act as a financial analyst.
model = genai.GenerativeModel('gemini-2.5-flash')
prompt = """
You are a crypto expert. Write a very short, 3-sentence "Daily Market Vibe" analysis for Bitcoin and Ethereum. 
Is the market Feeling Bullish (Greed) or Bearish (Fear) today? 
End with a specific "Ooginoog Verdict": either 'BUY WATCH', 'HOLD', or 'CAUTION'.
Keep it professional but punchy.
"""

# 3. Generate
try:
    response = model.generate_content(prompt)
    text = response.text.strip()
    
    # 4. Save to JSON
    data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
        "analysis": text
    }
    
    # Write to a file that the HTML can read
    with open("sentiment.json", "w") as f:
        json.dump(data, f)
        
    print("Sentiment updated successfully.")

except Exception as e:
    print(f"Error: {e}")
