import os
import json
import requests
import time
from datetime import datetime, timezone
import isodate

API_KEY = os.getenv("YT_API_KEY")  
CHANNEL_ID = "UC2eKzfI-pVWYLPzb_oRZ1Wg"

def get_latest_videos():
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=30"
    response = requests.get(url).json()
    video_ids = [item["id"]["videoId"] for item in response["items"] if item["id"]["kind"] == "youtube#video"]
    return video_ids

def get_durations(video_ids):
    url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={','.join(video_ids)}&part=contentDetails"
    response = requests.get(url).json()

    return [int(isodate.parse_duration(item["contentDetails"]["duration"]).total_seconds()) for item in response["items"]]

def create_playlist_json(video_ids, durations):
    total = sum(durations)
    now = int(time.time()) % total

    data = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "videos": video_ids,
        "durations": durations,
        "total_duration": total,
        "current_position": now
    }

    with open("playlist.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    videos = get_latest_videos()
    durations = get_durations(videos)
    create_playlist_json(videos, durations)
    print("playlist.json created successfully!")
