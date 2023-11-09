from googleapiclient.discovery import build
import os


class Video:
    api_key: str = os.getenv('YOUTUBE_API_KEY_FOR_E')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        try:
            self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id).execute()
            if not self.video_response["items"]:
                raise ValueError("Передан неверный ID видео")
        except ValueError:
            self.title = None
            self.view_count = None
            self.like_count = None
            self.video_url = None
        else:
            self.title: str = self.video_response['items'][0]['snippet']['title']
            self.view_count: int = self.video_response['items'][0]['statistics']['viewCount']
            self.like_count: int = self.video_response['items'][0]['statistics']['likeCount']
            self.video_url: str = f"https://youtu.be/{self.video_response['etag']}"

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, pl_id):
        super().__init__(video_id)
        self.pl_id = pl_id


