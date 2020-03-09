#!/bin/python

import instaloader
import datetime
import os
import glob


now = datetime.datetime.now()
hastag = "#mickeyfeio" + str(now.year)


# Aqui ele usa a lib externa 'instaloader' para baixar asimagens do instagram
# baseado na hastag
# #####################################################
# Get instance
L = instaloader.Instaloader()

for post in L.get_hashtag_posts('mickeyfeio' + str(now.year)):
    # post is an instance of instaloader.Post
    L.download_post(post, target=hastag)

# #####################################################


# Aqui ele deleta a lista de arquivos desnecessários
fileListTxt = glob.glob(hastag + "/*.txt")
fileListXz = glob.glob(hastag + "/*.xz")
fileListJson = glob.glob(hastag + "/*.json")

fileList = fileListTxt + fileListXz + fileListJson

# Iterate over the list of filepaths & remove each file.
for filePath in fileList:
    try:
        os.remove(filePath)
    except:
        print("Error while deleting file : ", filePath)
