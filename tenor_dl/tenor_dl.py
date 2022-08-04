#! /usr/bin/env python3

import os
import json
import requests
import argparse

from pyquery import PyQuery

def downloadURL(url: str, outLoc: str, urlOnly=False):
    #URL = "https://tenor.com/view/rage-work-pc-stressed-pissed-gif-15071896"

    print("fetching URL")

    res = requests.get(url)

    print("parsing data")

    pq = PyQuery(res.text)
    jsonData = pq("#store-cache")

    if not jsonData:
        print("ERROR: failed to parse data")
        return

    data = json.loads(jsonData.html())

    id = url.split("-")[-1]
    results = data["gifs"]["byId"][id]["results"][0]
    name = results["h1_title"]
    url = results["media"][0]["gif"]["url"]

    print("found gif:", name)

    if urlOnly:
        print("GIF direct link:", url)
        return

    print("downloading gif...")

    gif = requests.get(url)

    print("writing file")

    if outLoc == "-":
        print(gif.content)
        return

    outPath = os.path.join(outLoc, name+".gif")

    with open(outPath, "wb") as f:
        f.write(gif.content)

    print("done")


def parseArgs():
    parser = argparse.ArgumentParser(
        description="simple script to download gifs from tenor.com")

    parser.add_argument(
        "URL", type=str, help="tenor.com URL to download the gif from")
    parser.add_argument(
        "-o", "--output", type=str, default=".", dest="output",
        help="output path or use \"-\" for STDOUT"
    )
    parser.add_argument(
        "-u", "--urlonly", action="store_true", default=False, dest="urlonly",
        help="only print direct link to gif and exit"
    )

    return parser.parse_args()

def main():
    CLI = parseArgs()

    downloadURL(
        url=CLI.URL,
        outLoc=CLI.output,
        urlOnly=CLI.urlonly
    )
