# 🎬 DonyayeSerial to STRM (DS2STRM)
Scraping DonyayeSerial DataCenters to create `.strm` file

## 🤔 How does it work?
DS2STRM Scraps DataCenters of [donyayeserial.com](https://donyayeserial.com) to create `.strm.` file. Then you can import these files to Streaming softwares (e.g. `VLC Player`, `MX Player`, `KM Player`, `Kodi`, `Infuse`, etc.) 💪🏼

## 🤩 How to use?
To use DS2STRM Script you should find any URL of the series (e.g. [Rick and Morty](https://dls5.iran-gamecenter-host.com/DonyayeSerial/series/Rick.and.Morty/Soft.Sub/S01/720p.BluRay/)). Then open [CLI](https://github.com/mohammadali-arjomand/donyayeserial-to-strm/releases/download/v1.0.0/CLI.exe) or [GUI](https://github.com/mohammadali-arjomand/donyayeserial-to-strm/releases/download/v1.0.0/GUI.exe) edition of Script (Graphical is recommended) and enter the url. After Analyzing a directory/folder will be created next to your script file (e.g. `rick-and-morty/`). You can import this directory/folder to any Streaming software 🎥

## 🔨 How to run source?
To run source you should first download and install [Python3](https://www.python.org/downloads/).

Then run this command:
```bash
python -m pip install requests beautifulsoup4
```
or 
```bash
python3 -m pip install requests beautifulsoup4
```
And then you can run `gui.py` or `main.py`

## 📃 To Do
- Finding URLs automatically by name or IMDb ID
- Creating easier options to choose quality
- Improve Error handling (especially in GUI)

# 🤝🏼 Contribute
Intrested in DS2STRM? [Create an Issue](https://github.com/mohammadali-arjomand/donyayeserial-to-strm/issues/new) and explain your ideas! 🚀

# ⚖️ License
MIT License
Copyright (c) 2025 MohammadAli Arjomand [(more details)](https://github.com/mohammadali-arjomand/donyayeserial-to-strm/blob/main/LICENSE)