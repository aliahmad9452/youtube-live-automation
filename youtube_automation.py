import json, requests, time
from datetime import datetime, timezone

API_KEY = "AIzaSyCvfdD83DZapuYVaanGw5Lqj4LNq3SNHtU"
CHANNEL_ID = "UCWHpL9Vm9toVlZ4hIMmqwCA"  # Example

def get_latest_videos():
    url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=30"
    response = requests.get(url).json()
    video_ids = [item["id"]["videoId"] for item in response["items"] if item["id"]["kind"] == "youtube#video"]
    return video_ids

def get_durations(video_ids):
    url = f"https://www.googleapis.com/youtube/v3/videos?key={API_KEY}&id={','.join(video_ids)}&part=contentDetails"
    response = requests.get(url).json()
    
    def parse_duration(dur):
        import isodate
        return int(isodate.parse_duration(dur).total_seconds())

    return [parse_duration(item["contentDetails"]["duration"]) for item in response["items"]]

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

videos = get_latest_videos()
durations = get_durations(videos)
create_playlist_json(videos, durations)
print("playlist.json created successfully!")
