import requests
import os
from bs4 import BeautifulSoup

#primary download link
pDownloadLink = "https://10downloader.com/download?v="

#yt link
ytLink="youtube.com/watch?v="

#path to paste
path="videos/"

# #testing
# import shutil 
# shutil.rmtree(path)
# os.mkdir(path)
# #end testing

def getName(name):
  name = name.replace(' ', '-') #replace spaces for hyphens (best practice)
  name = name.replace('"', '') #remove quotation, breaks the function
  name = name.replace('/', '') #remove slash, breaks the function
  return name

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

#download everything
def download(video): 
  #make new directory
  name=getName(video['snippet']['title'])
  id = video['snippet']['resourceId']['videoId']
  print("currently downloading " + name)
  try: 
    os.mkdir(path+name)
  except: 
    return {"name": name, "id": id, "status": 400, "description": "file already exists"}

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
  if not downloadUrl: {"name": name, "id": id, "status": 500, "description": "couldn't get download link"}
  download = requests.get(downloadUrl)
  open(path+name+"/video.mp4", "wb").write(download.content)
  return {"name": name, "id": id, "status": 200, "description": "download completed in "+path+"/"+name}