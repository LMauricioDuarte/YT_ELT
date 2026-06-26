import requests
import json

API_KEY = "AIzaSyCkNJArzCrpfPT0HvWX2ZyqqVGlmBwScXM"
CHANNEL_HANDLE = "MrBeast"
playlistId = "UUX6OQ3DkcsbYNE6H8uQQuVA"

#url = f"https://youtube.googleapis.com/youtube/v3/channels?part=statistics&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
#url = f"https://youtube.googleapis.com/youtube/v3/videos?part=statistics&id=Td5W-Ams63w&key={API_KEY}"
#url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&id=Td5W-Ams63w&key={API_KEY}"
#url = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
#url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId={playlistId}&key={API_KEY}"
url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=r9aWeGqp43s&key={API_KEY}"

#response = requests.get(url)

#data = response.json()

#print(json.dumps(data,indent=4))
#print(data['items'][0]['contentDetails'])


extracted_data = []

def batch_list(video_id_lst, batch_size):
    for video_id in range(0, len(video_id_lst), batch_size):
        yield video_id_lst[video_id: video_id + batch_size]
        print(video_id_lst[video_id: video_id + batch_size]) 
try:
    for batch in batch_list(['r9aWeGqp43s','xDuuM3ERr5Q'], 50):
        video_ids_str = ",".join(batch)
        #print(video_ids_str)

        url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

        response = requests.get(url)

        response.raise_for_status()

        data = response.json()

        for item in data.get('items', []):
            video_id = item['id']
            snippet = item['snippet']
            contentDetails = item['contentDetails']
            statistics = item['statistics']

            video_data = {
                "video_id": video_id,
                "title": snippet['title'],
                "publishedAt": snippet['publishedAt'],
                "duration": contentDetails['duration'],
                "viewCount": statistics.get('viewCount', None),
                "likeCount": statistics.get('likeCount', None),
                "commentCount": statistics.get('commentCount', None)
            }

            extracted_data.append(video_data)

    #print(extracted_data)

except requests.exceptions.RequestException as e:
    raise e