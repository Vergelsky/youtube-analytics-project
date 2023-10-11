import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import isodate
import json

load_dotenv()


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY_FOR_E')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Экземпляр инициализируется id канала. Остальные данные подтягиваются по API.
        channel_id - id канала
        title - название канала
        about - описание канала
        url - ссылка на канал
        subs - количество подписчиков
        video_count - количество видео
        views - общее количество просмотров
        """
        self.info = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.channel_id = channel_id
        self.title = self.info["items"][0]["snippet"]["title"]
        self.about = self.info["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subs = self.info["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.info["items"][0]["statistics"]["videoCount"]
        self.views = self.info["items"][0]["statistics"]["viewCount"]

    @classmethod
    def get_service(cls):
        return cls.youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.info, indent=2))

    def to_json(self, json_file):
        info_dict = {"channel_id": self.channel_id,
                   "title": self.title,
                   "about": self.about,
                   "url": self.url,
                   "subs": self.subs,
                   "video_count": self.video_count,
                   "views": self.views}
        with open(json_file, "w") as file:
            json.dump(info_dict, file)
