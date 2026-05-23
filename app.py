import streamlit as st
import pandas as pd
from database import Session, Channel, TradeSetup, Video

st.set_page_config(page_title="Trading Transcript AI", layout="wide")

st.title("YouTube Trading Transcript Analyzer")

session = Session()

# 1. Manage Channels
st.header("Configured YouTube Channels")
with st.expander("How to add a channel"):
    st.write("Go to the YouTube channel's homepage (e.g., `https://www.youtube.com/@ChannelName`), copy the URL, and paste it below.")

new_channel = st.text_input("Add new YouTube Channel URL:")
if st.button("Add Channel"):
    if new_channel:
        try:
            session.add(Channel(channel_url=new_channel, name=new_channel.split('@')[-1] if '@' in new_channel else new_channel))
            session.commit()
            st.success("Added successfully!")
        except Exception as e:
            session.rollback()
            st.error("Channel might already exist or invalid URL.")

# Display existing channels
channels = session.query(Channel).all()
if channels:
    st.write("Currently monitoring:")
    for c in channels:
        st.write(f"- {c.name} ({c.channel_url})")

st.divider()

# 2. Display Extracted Data
st.header("Extracted Trading Setups")
setups = session.query(TradeSetup).all()

if setups:
    df = pd.DataFrame([{
        "Ticker": s.ticker,
        "Sentiment": s.sentiment,
        "Entry": s.entry_level,
        "Stop Loss": s.stop_loss,
        "Support": s.support,
        "Resistance": s.resistance,
        "Breakout": s.breakout,
        "Retest": s.retest_bounce,
        "Catalyst": s.catalyst_news,
        "Plan": s.full_setup_summary
    } for s in setups])
    
    st.dataframe(df, use_container_width=True)
else:
    st.info("No setups extracted yet. Ensure the scheduler is running and channels are added.")

session.close()
