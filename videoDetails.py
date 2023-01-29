def getName(video):
  name = video['snippet']['title'].replace(' ', '-') #replace spaces for hyphens (best practice)
  name = name.replace('"', '') #remove quotation, breaks the function
  name = name.replace('/', '') #remove slash, breaks the function
  return name