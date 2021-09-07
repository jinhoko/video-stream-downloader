# main.py
import argparse
import requests
import os
from urllib import request
from shutil import which, rmtree

import subprocess
from tqdm import tqdm

META_FILENAME="index.m3u8"

parser = argparse.ArgumentParser(description='Download streaming video and convert to mp4.')
parser.add_argument('meta_link', metavar='LINK', type=str, nargs=1,
                    help='index.m3u8 type stream metadata')
parser.add_argument('output_path', metavar='OUTPUT_PATH', type=str, nargs=1,
                    help='an empty(or new) folder path to store converted output')

args = parser.parse_args()

# input defn
meta_link = args.meta_link[0]
output_path = args.output_path[0]

# input check
assert which("ffmpeg") is not None, "ffmpeg required"
assert meta_link.endswith(META_FILENAME), "wrong metadata path. it should end with "+META_FILENAME
try:
    if os.path.exists(output_path):
        if not os.path.isdir(output_path):
            raise Exception("is not directory")
        if len( os.listdir(output_path) ) > 1:
            raise Exception("directory not empty")
    else:
        os.mkdir(output_path)
except Exception as e:
    print(e)
    print("Wrong directory setting.. exiting")
    exit(1)
tmp_dir = output_path+"/tmp/"
os.mkdir(tmp_dir)

# receive metadata
meta_content = requests.get(meta_link).content.decode('utf-8')

# parse .ts list
ts_list = []
for line in meta_content.split('\n'):
    if ".ts" in line:
        ts_list.append(line)
print(f"{ len(ts_list) } subfiles found.")
assert len(ts_list) > 0, "No .ts files found"

# download
print("Download start.")
download_baseurl = meta_link.split(META_FILENAME)[0]
save_basepath = tmp_dir
for line in tqdm(ts_list):
    url = download_baseurl + line
    savepath = save_basepath + line
    request.urlretrieve(url, savepath)

print("Download complete.")

# merge ts files
print("Merging ts segments")
merged_path = tmp_dir+"merged.ts"
with open(merged_path, "wb") as f:
    for line in tqdm(ts_list):
        filepath = tmp_dir + line
        with open(filepath, "rb") as f_sub:
            content = f_sub.read()
            f.write(content)
            f_sub.close()
    f.close()

print("Merge done")

# convert to mp4
print("Converting to .mp4")
mp4_path = output_path+"/out.mp4"
subprocess.run(['ffmpeg', '-i', merged_path, mp4_path])
rmtree(tmp_dir)

print("Convert done.")
print(f"MP4 file saved to: {mp4_path}")

