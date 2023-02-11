import requests
import os
from bs4 import BeautifulSoup
# import typer;
import key;
apiKey=key.apiKey

#primary download link
pDownloadLink = "https://10downloader.com/download?v="

#yt link
ytLink="youtube.com/watch?v="

#path to paste
path="videos/"


playlistId="PL278kIbxfIKdYE4kM_xlWt3GOwktUs_OJ"
# playlistId="PL278kIbxfIKeL7AvJIUlfav2TC_VradYu"

apiUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&part=status&key="+apiKey+"&playlistId="+playlistId+"&pageToken="


#testing
# import shutil 
# shutil.rmtree(path)
# os.mkdir(path)
# print("starting")
#end testing

def handleResponse(response):
  if response['status'] == 200: return response
  print(response)
  return response

def getVideoDetails(video): 
  def getName(name):
    name = name.replace(' ', '-') #replace spaces for hyphens (best practice)
    name = name.replace('"', '') #remove quotation, breaks the function
    name = name.replace('/', '') #remove slash, breaks the function
    return name
  
  def getId(video):
    return video['snippet']['resourceId']['videoId']

  def getThumbnail(urls):
    keys=['maxres', 'standard', 'high', 'medium', 'default'] #order of priority for thumbnail image
    url = urls.get(next((key for key in keys if key in urls), None))['url']
    return url

  def getVideoLink(url, name, id):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    if soup.select_one(".download-type h3").text != "Download Download Video with Sound": return {"name": name, "id": id, "status": 500, "description": "no download exists with sound"}
    url = soup.select_one("tbody tr td a").get('href').replace("amp;", "")
    return url
  
  name = getName(video['snippet']['title'])
  id =  getId(video)

  return [name, id, getThumbnail(video['snippet']['thumbnails']), getVideoLink(pDownloadLink+ytLink+id, name, id)]

#download video
def downloadVideo(video): 
  #get details
  [name, id, thumbnailUrl, downloadUrl] = getVideoDetails(video)

  #make new directory
  print("currently downloading " + name)
  try: 
    os.mkdir(path+name)
  except: 
    return {"name": name, "id": id, "status": 400, "description": "file already exists"}

  #create thumbnail image
  img_data = requests.get(thumbnailUrl).content
  with open(path+name+'/thumbnail.jpg', 'wb') as handler:
    handler.write(img_data)

  #write id.txt
  with open(path+name+"/id.txt", "w") as file:
    file.write(id)

  #download video
  if not downloadUrl: return handleResponse({"name": name, "id": id, "status": 500, "description": "couldn't get download link"})
  download = requests.get(downloadUrl)
  open(path+name+"/video.mp4", "wb").write(download.content)
  print("done")
  return handleResponse({"name": name, "id": id, "status": 200, "description": "download completed in "+path+"/"+name})

def playlistIterate(task, fails=[], pageToken=''):
  response = requests.get(apiUrl+pageToken)
  data = response.json()
  for video in data['items']:
    if not video['status']["privacyStatus"] == "private": 
      response = task(video)
      if(response["status"] != 200): fails.append(response)
    else: handleResponse({"name": "Private Video", "id": video['snippet']['resourceId']['videoId'], "status": 400, "description": "private video"})

  playlistIterate(task, fails, data['nextPageToken'])  if data.get('nextPageToken') else print(fails)

def updateVideos(video):
  name = getVideoDetails(video)[0]
  if(os.path.isdir(path+name)): 
    print(name + " exists, moving on")
    return handleResponse({"name": name, "id": id, "status": 200, "description": "condition satisfied"})
  return downloadVideo(video)

def updatePlaylist():
  playlistIterate(updateVideos)

def downloadPlaylist():
  playlistIterate(downloadVideo)
# downloadPlaylist()
updatePlaylist()
# if __name__ == "__main__":
#     typer.run(main)