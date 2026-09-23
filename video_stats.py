import requests
import json

import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

api_key = os.getenv("api_key")
chanel_name = "MrBeast"

def get_channel_data():
    
    try:

        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={chanel_name}&key={api_key}"

        response = requests.get(url)

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
    
    
    
if __name__ == "__main__":
    get_channel_data()