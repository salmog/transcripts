import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi
from database import Session, Channel, Video
import datetime

def get_latest_videos(channel_url):
    ydl_opts = {
        'extract_flat': True,
        'playlist_end': 5, # Check last 5 videos
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        return info.get('entries', [])

def download_transcript(video_id):
    try:
        # Tries Hebrew and English
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['he', 'en'])
        return " ".join([t['text'] for t in transcript_list])
    except Exception as e:
        return None

def scan_channels():
    session = Session()
    channels = session.query(Channel).all()
    
    for channel in channels:
        print(f"Scanning channel: {channel.name or channel.channel_url}")
        videos = get_latest_videos(channel.channel_url)
        
        for vid in videos:
            if not vid: continue
            vid_id = vid.get('id')
            
            # Check if video already exists
            if not session.query(Video).filter_by(video_id=vid_id).first():
                transcript = download_transcript(vid_id)
                if transcript:
                    new_video = Video(
                        video_id=vid_id,
                        channel_id=channel.id,
                        title=vid.get('title'),
                        published_at=datetime.datetime.now(), # Simplified
                        transcript=transcript
                    )
                    session.add(new_video)
                    session.commit()
                    # Trigger LLM analysis here in full pipeline
                    print(f"Downloaded transcript for {vid_id}")
    session.close()
