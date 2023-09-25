from pytube import YouTube
from pydub import AudioSegment
from io import BytesIO
import requests
import re
import asyncio


def convert_link(input_link):
    # Define regular expressions to match private video and Shorts link patterns
    video_private_pattern = re.compile(r"^https:\/\/youtu\.be\/([^?]+)\?si=([^&]+)")
    video_public_pattern = re.compile(r"^https:\/\/www\.youtube\.com\/watch\?v=([^&]+)")
    shorts_private_pattern = re.compile(
        r"^https:\/\/youtube\.com\/shorts\/([^?]+)\?si=([^&]+)"
    )
    shorts_public_pattern = re.compile(r"^https:\/\/www\.youtube\.com\/shorts\/([^&]+)")

    # Check if the input link matches any of the patterns and convert it to a public link
    if video_private_pattern.match(input_link):
        video_id = video_private_pattern.match(input_link).group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    elif video_public_pattern.match(input_link):
        return input_link
    elif shorts_private_pattern.match(input_link):
        shorts_id = shorts_private_pattern.match(input_link).group(1)
        return f"https://www.youtube.com/shorts/{shorts_id}"
    elif shorts_public_pattern.match(input_link):
        return input_link
    else:
        return None


def video_infos(url):
    url = convert_link(url)
    yt = YouTube(url)
    all_streams = yt.streams
    video_streams = all_streams.filter(
        file_extension="mp4", progressive=True, type="video"
    )
    audio = all_streams.filter(only_audio=True, file_extension="webm").first()
    resolutions = [video.resolution for video in video_streams if video.resolution]
    if audio:
        if audio.filesize_mb < 35:
            resolutions.append("mp3")
    return {
        "title": yt.title,
        "thumbnail": yt.thumbnail_url,
        "resolutions": resolutions,
    }


def get_video(url, res, extension):
    url = convert_link(url)
    yt = YouTube(url)
    streams = yt.streams.filter(
        res=res, file_extension=extension, progressive=True, type="video"
    )
    video = streams.first()
    return video


def get_audio(url, extension):
    url = convert_link(url)
    yt = YouTube(url)
    streams = yt.streams.filter(only_audio=True, file_extension=extension)
    audio_stream = streams.first()
    return audio_stream


def convert_webm_chunk_to_mp3(chunk):
    chunk = BytesIO(chunk)
    audio_segment = AudioSegment.from_file(chunk, format="webm")
    mp3_buffer = BytesIO()
    mp3_chunk = audio_segment.export(mp3_buffer, format="mp3")
    return mp3_buffer.getvalue()
