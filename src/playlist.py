from googleapiclient.discovery import build
import os
import json
import isodate
from datetime import timedelta


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))


class PlayList:
    api_key: str = os.getenv('YOUTUBE_API_KEY_FOR_E')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id):
        self.pl = self.youtube.playlistItems().list(playlistId=id,
                                                    part='snippet,contentDetails, status, id',
                                                    maxResults=50,
                                                    ).execute()
        self.title = self.youtube.playlists().list(id=id, part='snippet',).execute()['items'][0]['snippet']['localized']['title']
        self.url = f"https://www.youtube.com/playlist?list={id}"

    @property
    def total_duration(self):
        dur = timedelta(0)
        for item in self.pl['items']:
            video = self.youtube.videos().list(part='contentDetails',
                                           id=item['contentDetails']['videoId']
                                           ).execute()
            dur += isodate.parse_duration(video['items'][0]['contentDetails']['duration'])
        return dur

    def show_best_video(self):
        #Берем первое видео из плейлиста
        best_video = self.youtube.videos().list(part='statistics',
                                                id=self.pl['items'][0]['contentDetails']['videoId']
                                                ).execute()

        for item in self.pl['items']:
            #сравниваем с остальными, если очередное имеет больше лайков - оно становится новым лучшим
            maybe_best_video = self.youtube.videos().list(part='statistics',
                                               id=item['contentDetails']['videoId']
                                               ).execute()
            if maybe_best_video['items'][0]['statistics']['likeCount'] > best_video['items'][0]['statistics']['likeCount']:
                best_video = maybe_best_video

        return f"https://youtu.be/{best_video['items'][0]['id']}"
