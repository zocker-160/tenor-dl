#! /usr/bin/env python3

import os
import json
import requests
import argparse

import logging
logging.basicConfig(level=logging.INFO)

from pyquery import PyQuery

def downloadURL(url: str, outLoc: str, urlOnly=False):
    #URL = "https://tenor.com/view/rage-work-pc-stressed-pissed-gif-15071896"   

    if urlOnly or outLoc == "-":
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)

    logger.info("fetching URL")

    res = requests.get(url)

    logger.info("parsing data")

    pq = PyQuery(res.text)
    jsonData = pq("#store-cache")

    if not jsonData:
        logger.critical("ERROR: failed to parse data")
        return

    data = json.loads(jsonData.html())

    id = url.split("-")[-1]
    results = data["gifs"]["byId"][id]["results"][0]
    name = results["h1_title"]
    url = results["media"][0]["gif"]["url"]

    logger.info("found gif: "+name)

    if urlOnly:
        print(url, end="")
        return

    logger.info("downloading gif...")

    gif = requests.get(url)

    logger.info("writing file")

    if outLoc == "-":
        print(gif.content, end="")
        return

    outPath = os.path.join(outLoc, name+".gif")

    with open(outPath, "wb") as f:
        f.write(gif.content)

    logger.info("done")


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
    global logger
    logger = logging.getLogger(":")

    CLI = parseArgs()

    downloadURL(
        url=CLI.URL,
        outLoc=CLI.output,
        urlOnly=CLI.urlonly
    )
