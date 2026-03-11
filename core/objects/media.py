from pydantic import BaseModel

class PhotoAttachmentPayload(BaseModel):
    photo_id: int
    token: str
    url: str

class VideoUrls(BaseModel):
    mp4_1080: str = None
    mp4_720: str = None
    mp4_480: str = None
    mp4_360: str = None
    mp4_240: str = None
    mp4_114: str = None
    hls: str = None

class Video(BaseModel):
    token: str
    urls: VideoUrls = None
    thumbnail: PhotoAttachmentPayload = None
    width: int
    height: int
    duration: int