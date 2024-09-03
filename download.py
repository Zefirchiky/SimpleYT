from pytube import YouTube
from shutil import copy2
import os


def download(link_var, audio_var, video_var, copy_var,
    VIDEO_SAVE_DIRECTORY, AUDIO_SAVE_DIRECTORY, result) -> None: 
    """
    Downloads YouTube video or audio from given link.

    Args:
        link_var (ttk.StringVar): The link to the YouTube video.
        audio_var (ttk.BooleanVar): If True, the audio will be downloaded.
        video_var (ttk.BooleanVar): If True, the video will be downloaded.
        copy_var (ttk.IntVar): The number of copies to make of the downloaded file.

    Returns:
        None
    """
    result(f"Processing {f"{link_var.get()}"}")
    video = YouTube(link_var.get())
    is_video = video_var.get()
    is_audio = audio_var.get()

    if video is None:
        # If the link is invalid, show an error message
        return

    if video.author in video.title: filename = f'{video.title}.mp4'
    else: filename = f'{video.author} - {video.title}.mp4'
    filename = filename.replace('|', '&').replace('\"', '\'').replace('\\', '-').replace('/', '&').replace('?', '')
    filename_dir = filename.replace(' ', '')
    video_file_dir = os.path.join(VIDEO_SAVE_DIRECTORY, filename)
    audio_file_dir = os.path.join(AUDIO_SAVE_DIRECTORY, filename)

    if is_video:
        # Get the highest resolution video
        vid = video.streams.get_highest_resolution()
        if vid is None:
            # If no video is found, show an error message
            result(f"Failed to download video ({filename}): {"No video found"}", 'Red')
            return
        try:
            # Download the video
            vid.download(VIDEO_SAVE_DIRECTORY, filename=filename_dir)
        except Exception as a:
            result(f"Failed to download video ({filename}): {f"{a}"}", 'Red')
            return 
        # Replace the downloaded video with the correct name
        os.replace(f"{VIDEO_SAVE_DIRECTORY}/{filename_dir}", video_file_dir)
        # Create copies of the video
        for i in range(copy_var.get() - 1):
            name, ext = os.path.splitext(video_file_dir)
            name = name + f' ({i + 2})' + ext
            copy2(video_file_dir, name)
        
    if is_audio:
        # Get the audio with the highest quality
        audio = video.streams.filter(only_audio = True).first()
        if audio is None:
            # If no audio is found, show an error message
            result(f"Failed to download audio ({filename}): {"No audio found"}", 'Red')
            return
        try:
            # Download the audio
            audio.download(AUDIO_SAVE_DIRECTORY, filename=filename_dir)
        except Exception as a:
            result(f"Failed to download audio ({filename}): {f"{a}"}", 'Red')
            return
        # Replace the downloaded audio with the correct name
        os.replace(f"{AUDIO_SAVE_DIRECTORY}/{filename_dir}", audio_file_dir)
        # Create copies of the audio
        for i in range(copy_var.get() - 1):
            name, ext = os.path.splitext(audio_file_dir)
            name = name + f' ({i + 2})' + ext
            copy2(audio_file_dir, name)

    result(f"Downloaded {filename}", 'Green')