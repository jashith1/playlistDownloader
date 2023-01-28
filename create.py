import requests
import os
from bs4 import BeautifulSoup

#apiKey
apiKey="my parents taught me never to upload my api key online, and i will listen to them"

#playlist
playlistId="PL278kIbxfIKeL7AvJIUlfav2TC_VradYu"
# playlistId="PL278kIbxfIKeQcBRwEzZGODa_t2YYlwzv"

#path to paste
path="videos/"

#api url
apiUrl = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&part=status&key="+apiKey+"&playlistId="+playlistId+"&pageToken="

#primary download link
pDownloadLink = "https://10downloader.com/download?v="

#yt link
ytLink="youtube.com/watch?v="

#fail list
fails = []

# #testing
# import shutil 
# shutil.rmtree(path)
# os.mkdir(path)
# #end testing

#helper methods
def handleFail(name, id, status, reason):
  failObject = {"name": name, "id": id, "status": status, "reason": reason}
  fails.append(failObject)

def getName(name):
  name = name.replace(' ', '-') #replace spaces for hyphens (best practice)
  name = name.replace('"', '') #remove quotation, breaks the function
  name = name.replace('/', '') #remove slash, breaks the function
  return name

def getThumbnail(urls):
  keys=['maxres', 'standard', 'high', 'medium', 'default']
  url = urls.get(next((key for key in keys if key in urls), None))['url']
  return url

def getVideoLink(url, name, id):
  html = requests.get(url).text
  # print(html)
  soup = BeautifulSoup(html, 'html.parser')
  if soup.select_one(".download-type h3").text != "Download Download Video with Sound": return handleFail(name, id, 500, "no download exists with sound")
  url = soup.select_one("tbody tr td a").get('href').replace("amp;", "")
  return url

#download everything
def download(video): 
  #make new directory
  name=getName(video['snippet']['title'])
  id = video['snippet']['resourceId']['videoId']
  print("currently downloading " + name)
  try: 
    os.mkdir(path+name)
  except: 
    return handleFail(name, id, 400, "file already exists")

  #create thumbnail image
  thumbnailUrl = getThumbnail(video['snippet']['thumbnails'])
  img_data = requests.get(thumbnailUrl).content
  with open(path+name+'/thumbnail.jpg', 'wb') as handler:
    handler.write(img_data)

  #write id.txt
  with open(path+name+"/id.txt", "w") as file:
    file.write(id)

  #download video
  downloadUrl = getVideoLink(pDownloadLink+ytLink+id, name, id) #direct download url
  if not downloadUrl: handleFail(name, id, 500, "couldn't get download url")
  download = requests.get(downloadUrl)
  # print(download)
  open(path+name+"/video.mp4", "wb").write(download.content)

#data call
def main(pageToken=''):
  response = requests.get(apiUrl+pageToken)
  data = response.json()
  for video in data['items']:
    if not video['status']["privacyStatus"] == "private": download(video)

  main(data['nextPageToken']) if data.get('nextPageToken') else print(fails)

main("EAAaB1BUOkNQOEI")