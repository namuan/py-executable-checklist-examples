#!/usr/bin/env python3
"""
Downloads music from r/listentothis and saves them to a folder
"""
import json
import logging
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime
from pathlib import Path
from typing import List

import requests
import yt_dlp as youtube_dl
from py_executable_checklist.workflow import WorkflowBase, run_workflow


def get_json(url, params=None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    return requests.get(url, headers=headers, params=params)


def setup_logging(verbosity):
    logging_level = logging.WARNING
    if verbosity == 1:
        logging_level = logging.INFO
    elif verbosity >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(
        handlers=[
            logging.StreamHandler(),
        ],
        format="%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging_level,
    )
    logging.captureWarnings(capture=True)


# Workflow steps


class GatherJSONData(WorkflowBase):
    """
    Gather JSON data from the r/listentothis subreddit for the top songs of the past month.
    """

    def execute(self):
        # Send a GET request to the r/listentothis subreddit API
        response = get_json("https://www.reddit.com/r/listentothis/top.json", params={"t": "month"})

        # Parse the JSON data from the response
        data = json.loads(response.text)

        # Extract the list of URLs from the data
        urls = [item["data"]["url"] for item in data["data"]["children"]]

        # Return the list of URLs as output
        return {"urls": urls}


class CreateMonthlyFolder(WorkflowBase):
    """
    Create a file based on the name of the month in the local directory.
    """

    root_path: Path

    def execute(self):
        # Get the current month and year
        current_month = datetime.now().strftime("%B")
        current_year = datetime.now().year

        # Create the folder for the current month in the local directory
        folder_path = self.root_path / f"{current_year}-{current_month}"
        folder_path.mkdir(parents=True, exist_ok=True)

        return {"folder_name": folder_path.as_posix()}


class DownloadSongs(WorkflowBase):
    """
    For each URL, download the song in MP3 format and add it to the specified folder.
    """

    folder_name: str
    urls: List[str]

    def download_song(self, url, folder_name):
        ydl_opts = {
            "outtmpl": f"{folder_name}/%(title)s.%(ext)s",
            "format": "bestaudio/best",
            "extractaudio": True,
            "audioformat": "mp3",
            "noplaylist": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def execute(self):
        for url in self.urls:
            self.download_song(url, self.folder_name)


# Workflow definition


def workflow():
    return [
        GatherJSONData,
        CreateMonthlyFolder,
        DownloadSongs,
    ]


# Boilerplate


def parse_args():
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)

    parser.add_argument(
        "-p",
        "--root-path",
        type=Path,
        default=Path.cwd().joinpath(".temp"),
        help="Path to the directory where the file will be created",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        dest="verbose",
        help="Increase verbosity of logging output",
    )
    return parser.parse_args()


def main(args):
    setup_logging(args.verbose)
    context = args.__dict__
    run_workflow(context, workflow())


if __name__ == "__main__":
    args = parse_args()
    main(args)
