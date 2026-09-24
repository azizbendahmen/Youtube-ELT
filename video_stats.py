import requests
import json

import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

api_key = os.getenv("api_key")
chanel_name = "MrBeast"

max_results = 50


def get_playlist_id():
    
    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={chanel_name}&key={api_key}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        print(response)
        data = response.json()

        with open("channel_data.json", "w") as f:
            json.dump( data , f, indent=4)
            
        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(f"Channel Playlist ID: {channel_playlistId}")
        
        return channel_playlistId
        
    except requests.exceptions.RequestException as e:
        raise e
    



def get_video_ids(playlistId):
    
    video_ids = []
    page_token = None
    
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key={api_key}"
    
    try:
        
        while True:
            url = base_url
            if page_token:
                url += f"&pageToken={page_token}"
            
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            with open("video_data.json", "w") as f:
                json.dump(data, f, indent=4)
            
            for item in data["items"]:
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        
        
        return video_ids
        
        
    except requests.exceptions.RequestException as e:
        raise e


def extract_video_stats(video_ids):
    video_stats = []

    def batch_list(video_id_list, batch_size):
        for i in range(0, len(video_id_list), batch_size):
            yield video_id_list[i : i + batch_size]

    try:
        for batch in batch_list(video_ids, max_results):
            video_id_str = ",".join(batch)

            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_id_str}&key={api_key}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            with open("video_stats_data.json", "w") as f:
                json.dump(data, f, indent=4)

            for item in data["items"]:
                video_id = item["id"]
                snippet = item["snippet"]
                content_details = item["contentDetails"]
                stats = item["statistics"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "published_at": snippet["publishedAt"],
                    "duration": content_details["duration"],
                    "view_count": stats.get("viewCount", None),
                    "like_count": stats.get("likeCount", None),
                    "comment_count": stats.get("commentCount", None)
                }
                video_stats.append(video_data)

        print(f"extracted video stats: {video_stats}")
        return video_stats

    except requests.exceptions.RequestException as e:
        raise e

if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    extract_video_stats(video_ids)