#!/usr/bin/env python

#TODO: Add auto name detection

import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import requests as req
from bs4 import BeautifulSoup as bs
import re, time, os, sys
from urllib.parse import urljoin
import subprocess

ENTRY_WIDTH = 100
LOG_AREA_WIDTH = 100

win = tk.Tk()
win.title("DonyayeSerial to STRM")
win.geometry("900x600")
win.minsize(400, 400)

def clear_log():
    log_area.config(state="normal")
    log_area.delete(1.0, tk.END)
    log_area.config(state="disabled")

def read_urls(url):
    try:
        r = req.get(url)
    except:
        err("Connection failed")
    soup = bs(r.text, "html.parser")

    file_items = soup.select("td.n > a")

    episodes_urls = []
    for item in file_items:
        href = item.get("href")
        if href != "../":
            episodes_urls.append(href)

    return episodes_urls

def open_dir(name):
    path = os.path.abspath(name)

    if sys.platform.startswith("win"):
        os.startfile(path)
    elif sys.platform.startswith("darwin"):
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])

def prin(line):
    log_area.config(state="normal")
    log_area.insert(tk.END, f"{line}\n")
    log_area.config(state="disabled")
    log_area.see(tk.END)
    print(line)
    win.update()

def err(message, close=True):
    messagebox.showerror("Error", message)
    if close:
        exit()

# def analyze(url, dir_name, opt, seas):
#     prin(url)
def analyze(url, dir_name, opt, seas):
    clear_log()

    options = opt.split(" ")
    seasons = seas.split(" ")

    episodes = []

    def go_recursive(url, options, seasons):
        prin(f"[E] {len(episodes)} episode(s) found")
        prin(f"[U] Analyzing {url}")
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

    prin("[ ] Starting ...")

    if os.path.isdir(dir_name):
        err(f"{dir_name} exists. Please use another directory name.")
    t1 = time.time()
    go_recursive(url, options, seasons)

    prin("\n[ ] Creating files ...")

    if not dir_name.endswith("/"):
        dir_name += "/"

    os.mkdir(dir_name)
    for e in episodes:
        file_path = dir_name + e.split("/")[-1] + ".strm"
        with open(file_path, "w") as f:
            f.write(e)
        prin(f"[F] Created {file_path}")
    t2 = time.time()
    prin(f"""
[ ] {len(episodes)} episode(s) found
[ ] The files were created at {dir_name}
[ ] Finished in {round(t2 - t1, 3)} seconds.""")
    open_dir(dir_name)
    prin("[ ] Opening File Manager ...")

def load_all_seasons():
    clear_log()

    prin("[ ] Looking for seasons")
    url = url_entry.get()
    options = opt_entry.get()

    if url == "" or options == "":
        err("URL and Options are required", False)
        return
    
    def search(url):
        links = read_urls(url)
        if links[0] == "s01":
            return links
        for link in links:
            clean_link = link.lower()
            clean_link = re.sub(r'[^a-z0-9]', '', clean_link)
            if clean_link in options:
                return read_urls(urljoin(url, link))
    
    def force_search(url):
        seasons = search(url)
        if seasons == None:
            return force_search(urljoin(url, "../"))
        else:
            return seasons
    try:
        seasons = force_search(url)
    except:
        seasons = []
    prin(f"[ ] {len(seasons)} season(s) found")
    seas_entry.delete(0, tk.END)
    for i in range(len(seasons)):
        seasons[i] = seasons[i].replace("/", "")
        seasons[i] = seasons[i].lower()
        if i < len(seasons)-1:
            seasons[i] += " "
        seas_entry.insert(tk.END, seasons[i])
    
tk.Label(win, text="Enter Any URL of your series:").pack()

url_entry = tk.Entry(win, width=ENTRY_WIDTH)
url_entry.insert(0, "https://dls5.iran-gamecenter-host.com/DonyayeSerial/series/Rick.and.Morty/")
url_entry.pack()


tk.Label(win, text="Enter Directory Name:").pack()

dir_entry = tk.Entry(win, width=ENTRY_WIDTH)
dir_entry.insert(0, "rick-and-morty")
dir_entry.pack()


tk.Label(win, text="Enter Options:").pack()

opt_entry = tk.Entry(win, width=ENTRY_WIDTH)
opt_entry.insert(0, "softsub 720pdvdrip 720pbluray 720pwebdl")
opt_entry.pack()


tk.Label(win, text="Enter Seasons:").pack()

seas_frm = tk.Frame(win)
seas_frm.pack()

seas_entry = tk.Entry(seas_frm, width=ENTRY_WIDTH-11)
seas_entry.insert(0, "s01")
seas_entry.grid(row=0, column=0)

tk.Button(seas_frm, text="All Seasons", command=load_all_seasons).grid(row=0, column=1)

tk.Button(win, text="Analyze", command=lambda:analyze(url_entry.get(), dir_entry.get(), opt_entry.get(), seas_entry.get())).pack()

log_area = ScrolledText(win, wrap=tk.WORD, height=20, width=LOG_AREA_WIDTH)
log_area.config(state="disabled")
log_area.pack()

tk.Label(win, text="THIS IS A VERY SIMPLE GUI FOR DS2STRM SCRIPT").pack()

win.mainloop()
