import requests
import key
apiKey=key.apiKey

# playlistId="PL278kIbxfIKeQcBRwEzZGODa_t2YYlwzv"
playlistId="PL278kIbxfIKeL7AvJIUlfav2TC_VradYu"

apiUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&part=status&key="+apiKey+"&playlistId="+playlistId+"&pageToken="

fails = [] #fail list

def handleResponse(response):
  if response['status'] == 200: return
  failObject = {"name": response['name'], "id": response["id"], "status": response["status"], "description": response["description"]}
  print(fails)
  fails.append(failObject)

def iterate(task, pageToken=''):
  response = requests.get(apiUrl+pageToken)
  data = response.json()
  for video in data['items']:
    if not video['status']["privacyStatus"] == "private": handleResponse(task(video))
    else: handleResponse({"name": "Private Video", "id": video['snippet']['resourceId']['videoId'], "status": 400, "description": "private video"})

  iterate(task, data['nextPageToken'])  if data.get('nextPageToken') else print(fails)
