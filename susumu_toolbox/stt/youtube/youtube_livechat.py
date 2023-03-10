import datetime
import re

import dateutil.parser
import requests

# noinspection PyMethodMayBeStatic, PyShadowingNames
from susumu_toolbox.utility.config import Config


# pip install python-dateutil


class YouTubeLiveChatMessage:
    _custom_emoji_pattern = re.compile(r":[a-zA-Z0-9_]+:")

    def __init__(self, item):
        # displayMessageはスパチャの場合は、'¥価格 from 名前: "メッセージ"'という形式になっている。
        # item["snippet"]["type"]によってもっと処理を分けるべき？
        self.original_message = item["snippet"]["displayMessage"]
        self.name = item["authorDetails"]["displayName"]
        self.datetime_utc = self.parse_utc_datetime_str(item["snippet"]["publishedAt"])
        self.message = self._delete_custom_emoji(self.original_message)

    def parse_utc_datetime_str(self, datetime_str: str) -> datetime.datetime:
        return dateutil.parser.parse(datetime_str)

    def _delete_custom_emoji(self, text: str) -> str:
        return self._custom_emoji_pattern.sub("", text)


# noinspection PyMethodMayBeStatic
class YouTubeLiveChat:
    # もっと設計をしっかりするなら youtube_livechat_messages や pytchatを参考にする？
    def __init__(self, config: Config):
        self._next_page_token = None
        self._api_key = config.get_youtube_api_key()
        self._youtube_url = config.get_youtube_live_url()
        self._chat_id = None
        self._video_id = None

    def _get_video_id(self):
        video_id = self._youtube_url.replace('https://www.youtube.com/watch?v=', '')
        return video_id

    def _get_chat_id(self):
        url = 'https://www.googleapis.com/youtube/v3/videos'
        params = {
            'key': self._api_key,
            'id': self._video_id,
            'part': 'liveStreamingDetails'
        }
        data = requests.get(url, params=params).json()

        details = data['items'][0]['liveStreamingDetails']
        if 'activeLiveChatId' in details.keys():
            return details['activeLiveChatId']
        return None

    def fetch_messages(self):
        if self._video_id is None:
            self._video_id = self._get_video_id()
        if self._chat_id is None:
            self._chat_id = self._get_chat_id()

        params = {
            'key': self._api_key,
            'liveChatId': self._chat_id,
            'part': 'id, snippet, authorDetails'
        }
        if self._next_page_token:
            params['pageToken'] = self._next_page_token

        # API仕様は https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list 参照
        # itemsの仕様は https://developers.google.com/youtube/v3/live/docs/liveChatMessages 参照
        url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
        result = requests.get(url, params=params).json()

        messages = []
        if "items" not in result.keys():
            return messages
        for item in result['items']:
            messages.append(YouTubeLiveChatMessage(item))

        self._next_page_token = result['nextPageToken']
        return messages
