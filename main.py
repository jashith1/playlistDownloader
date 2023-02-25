from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
playlist = Playlist('https://www.youtube.com/playlist?list=PL278kIbxfIKdYE4kM_xlWt3GOwktUs_OJ')

import argparse
parser = argparse.ArgumentParser(description='download videos ig')
parser.add_argument('-p', '--plain', action='store_true', help='perform plain direct download')
args = parser.parse_args()

path = playlist.title + "/"

# testing
import shutil 
import os
shutil.rmtree(path)
os.mkdir(path)
print("starting")
# end testing

if not args.plain: 
  import requests

for url in playlist.video_urls:
 video=YouTube(url,on_progress_callback=on_progress)
 location = path if args.plain else path + video.title
 fileName = None if args.plain else "video.mp4"
 print("downloading " + video.title)
 video.streams.filter(progressive=True).order_by('resolution').desc().first().download(output_path=location, filename=fileName)
 if not args.plain: 
  img_data = requests.get(video.thumbnail_url).content
  with open(location+'/thumbnail.jpg', 'wb') as handler:
    handler.write(img_data)
 print("\n")

print("done :)")