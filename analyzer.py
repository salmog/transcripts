import os
import json
from openai import OpenAI
from database import Session, TradeSetup, Video

# Ensure you export OPENAI_API_KEY="your_key" in your terminal
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

def analyze_transcript(transcript_text, video_id):
    prompt = """
    Analyze the following stock/finance transcript (may be English or Hebrew).
    Extract the following data into a JSON array of objects. 
    Rule: ALL TICKERS MUST BE IN ENGLISH CAPITAL LETTERS.
    If a field is not mentioned, return null.
    Fields per object:
    1. "ticker": Ticker symbol
    2. "sentiment": bullish, bearish, or neutral
    3. "stop_loss": Price level mentioned
    4. "entry_level": Price level mentioned
    5. "support": Price level mentioned
    6. "resistance": Price level mentioned
    7. "breakout": Price level mentioned
    8. "retest_bounce": Price level mentioned
    9. "catalyst_news": Specific event/news
    10. "full_setup_summary": Brief summary of the trade plan

    Transcript:
    """ + transcript_text[:15000] # Truncated for context limits

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        
        data = json.loads(response.choices[0].message.content)
        # Expected format: {"setups": [{...}, {...}]}
        
        session = Session()
        for setup in data.get('setups', []):
            new_setup = TradeSetup(
                video_id=video_id,
                ticker=setup.get('ticker', '').upper(),
                sentiment=setup.get('sentiment'),
                stop_loss=setup.get('stop_loss'),
                entry_level=setup.get('entry_level'),
                support=setup.get('support'),
                resistance=setup.get('resistance'),
                breakout=setup.get('breakout'),
                retest_bounce=setup.get('retest_bounce'),
                catalyst_news=setup.get('catalyst_news'),
                full_setup_summary=setup.get('full_setup_summary')
            )
            session.add(new_setup)
        session.commit()
        session.close()
    except Exception as e:
        print(f"Error analyzing {video_id}: {e}")
