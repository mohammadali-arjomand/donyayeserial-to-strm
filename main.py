#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Requirements

import requests as req
from bs4 import BeautifulSoup as bs
import re
import time
import os
from urllib.parse import urljoin


# In[2]:


# Inputs

url = input("Enter DonyayeSerial URL (Default is Rick and Morty): ")
dir_name = input("Enter directory name [rick-and-morty]: ")
options = input("Enter options by lowercase english letters and numbers [softsub 720pbluray 720webdl]: ").split(" ")
seasons = input("Enter seasons like example [s01 s02 s03 s04 s05 s06]: ").split(" ")

if url == "":
    url = "https://dls5.iran-gamecenter-host.com/DonyayeSerial/series/Rick.and.Morty/"
if dir_name == "":
    dir_name = "rick-and-morty"
if options == [""]:
    options = ["softsub", "720pbluray", "720pwebdl"]
if seasons == [""]:
    seasons = ["s01", "s02", "s03", "s04", "s05", "s06"]


# In[3]:


# Functions

def read_urls(url):
    try:
        r = req.get(url)
    except:
        print("[X] Connection failed\nFinish.")
        exit()
    soup = bs(r.text, "html.parser")

    file_items = soup.select("td.n > a")

    episodes_urls = []
    for item in file_items:
        href = item.get("href")
        if href != "../":
            episodes_urls.append(href)

    return episodes_urls


# In[4]:


episodes = []

def go_recursive(url, options, seasons):
    print(f"[E] {len(episodes)} episode(s) found")
    #print(f"[S] Looking for {' '.join(seasons)}")
    print(f"[U] Analyzing {url}")
    links = read_urls(url)
    if len(links) == 0:
        return
    if links[0].endswith((".mkv", ".mp4")):
        for link in links:
            episodes.append(url + link)
        if len(seasons) > 0:
            go_recursive(urljoin(url, "../../"), options, seasons)
        else:
            return
    found = False
    for link in links:
        clean_link = link.lower()
        clean_link = re.sub(r'[^a-z0-9]', '', clean_link)
        if clean_link in (options + seasons):
            url += link
            if clean_link in seasons:
                seasons.remove(clean_link)
            found = True
            break
    if not found:
        url = urljoin(url, "../../")
    go_recursive(url, options, seasons)


# In[5]:


# Looking for URLs and creating the file
print("[ ] Starting ...")

if os.path.isdir(dir_name):
    print(f"[X] {dir_name} exists. Please use another directory name.\nFinish.")
    exit()
t1 = time.time()
go_recursive(url, options, seasons)

print("\n[ ] Creating files ...")

if not dir_name.endswith("/"):
    dir_name += "/"

os.mkdir(dir_name)
for e in episodes:
    file_path = dir_name + e.split("/")[-1] + ".strm"
    with open(file_path, "w") as f:
        f.write(e)
    print(f"[F] Created {file_path}")
t2 = time.time()
print(f"""
[ ] {len(episodes)} episode(s) found
[ ] The files were created at {dir_name}
[ ] Finished in {round(t2 - t1, 3)} seconds.""")


# In[ ]:




