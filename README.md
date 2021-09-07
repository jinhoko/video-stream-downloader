# video-stream-downloader

## Introduction

Download ([HLS](https://en.wikipedia.org/wiki/HTTP_Live_Streaming)) streaming video and converts to mp4. It requires `.m3u8` metadata named with `index.m3u8`. 

## Requirements
- [ffmpeg](https://ffmpeg.org/download.html) installed on system
- python libraries
  - requests
  - urllib
  - tqdm

## Usage
```
python3 M3U8_LINK OUTPUT_FOLDER_PATH
```
Example:
```
python3 http://example.cdn.com/content.mp4/index.m3u8 /home/me/target_folder
```