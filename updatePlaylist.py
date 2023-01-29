import playlistIterate
import os
import videoDetails
import downloadVideo

path="videos/"

def checkVideos(video):
  name = videoDetails.getName(video)
  if(os.path.isdir(path+name)): 
    print(name + " exists, moving on")
    return {"name": name, "id": id, "status": 200, "description": "file exists"}
  return downloadVideo.download(video)

playlistIterate.iterate(checkVideos)