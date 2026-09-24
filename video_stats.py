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
            data = response.json()
            
            with open("video_data.json", "w") as f:
                json.dump(data, f, indent=4)
            
            for item in data["items"]:
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)
            
            page_token = data.get("nextPageToken")
            if not page_token:
                break
        
        print(f"Total Video IDs: {len(video_ids)}")
        print(f"Video IDs: {video_ids}")
        return video_ids
        
        
    except requests.exceptions.RequestException as e:
        raise e
    

    
if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)