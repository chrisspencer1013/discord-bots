import uuid
import requests
import random
import logging
import json
import shutil
import os.path
from urllib.parse import urlparse

from util import StringEnum

REQUEST_ID = str(uuid.uuid4())


class Timeframes(StringEnum):
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"
    ALL = "all"


class SortTypes(StringEnum):
    CONTROVERSIAL = "controversial"
    BEST = "best"
    HOT = "hot"
    NEW = "new"
    RANDOM = "random"
    RISING = "rising"
    TOP = "top"


class DefaultRedditArgs:
    SORT = SortTypes.TOP
    LIMIT = 20
    TIMEFRAME = Timeframes.MONTH


def _get_image_urls_from_subreddit(subreddit, sort, limit, timeframe):
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={timeframe}"

    response = requests.get(
        url,
        headers={"user-agent": REQUEST_ID},
    )

    response_dict = json.loads(response.content)

    image_urls = []
    for res in response_dict["data"]["children"]:
        # post hint indicates if its image or vid
        # if its not there, its likely a gallery or text post
        post_hint = res["data"].get("post_hint")

        if post_hint == "image":
            image_urls.append(res["data"]["url"])
        elif post_hint == "hosted:video":
            media = res["data"]["media"]
            if "reddit_video" in media.keys():
                video_url = media["reddit_video"]["fallback_url"]
                image_urls.append(video_url)
    return image_urls


def _get_filename_from_url(url):
    x = urlparse(url)
    return os.path.basename(x.path)


def _get_file_extension_from_url(url):
    # returns with .
    x = urlparse(url)
    _, extension = os.path.splitext(x.path)
    return extension


def _save_image_from_url(url, topic, keep_name=False):
    if not os.path.isdir(topic):
        os.mkdir(topic)

    if keep_name:
        file_name = f"{topic}/{_get_filename_from_url(url)}"
    else:
        file_name = f"{topic}/{uuid.uuid4()}{_get_file_extension_from_url(url)}"

    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, "wb") as f:
            shutil.copyfileobj(res.raw, f)
        logging.info(f"image downloaded successfully: {file_name}")
        return True
    else:
        logging.info(f"{res.status_code} - error downloading image: {file_name}")
        return False


def _cache_subreddit_images_to_file(subreddit, topic, sort, limit, timeframe):
    image_urls = _get_image_urls_from_subreddit(
        subreddit=subreddit,
        sort=sort,
        limit=limit,
        timeframe=timeframe,
    )

    for image_url in image_urls:
        _save_image_from_url(image_url, topic)


def update_all():
    # basically using command names as topics for any of the image post commands
    # don't feel like setting up a json/config for this, but that could be an option
    # this structure should allow for expansion to twitter or other sources
    updates = [
        {
            "topic": "ambimal",
            "subreddits": [
                {"name": "ShibaInu"},
                {"name": "rarepuppers"},
                {"name": "dogswithjobs"},
                {"name": "whatswrongwithyourdog"},
                {"name": "dogsonroofs"},
                {"name": "corgi"},
                {"name": "wigglebutts"},
                {
                    "name": "blop",
                    "timeframe": Timeframes.YEAR,
                },
                {
                    "name": "doggles",
                    "limit": 10,
                    "timeframe": Timeframes.YEAR,
                },
                {
                    "name": "blurrypicturesofdogs",
                    "limit": 10,
                    "timeframe": Timeframes.YEAR,
                },
            ],
        },
    ]
    for update in updates:
        topic = update["topic"]

        subreddits = update.get("subreddits")
        for subreddit in subreddits:
            subreddit_name = subreddit["name"]  # not optional, the rest are
            sort = subreddit.get("sort", DefaultRedditArgs.SORT)
            limit = subreddit.get("limit", DefaultRedditArgs.LIMIT)
            timeframe = subreddit.get("timeframe", DefaultRedditArgs.TIMEFRAME)

            _cache_subreddit_images_to_file(
                subreddit=subreddit_name,
                topic=topic,
                sort=sort,
                limit=limit,
                timeframe=timeframe,
            )


def get_random_image_path(topic):
    files = os.listdir(topic)

    return f"{topic}/{random.choice(files)}"
