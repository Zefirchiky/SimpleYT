from pytube import YouTube
from shutil import copy2
import ttkbootstrap as ttk
import threading
import asyncio
import os

VIDEO_SAVE_DIRECTORY_NAME = "Video"
AUDIO_SAVE_DIRECTORY_NAME = "Audio"

CUR_DIR = os.getcwd()
VIDEO_SAVE_DIRECTORY = os.path.join(CUR_DIR, VIDEO_SAVE_DIRECTORY_NAME)
AUDIO_SAVE_DIRECTORY = os.path.join(CUR_DIR, AUDIO_SAVE_DIRECTORY_NAME)

app = ttk.Window(themename="darkly")

app_frame = ttk.Frame(app)

link_var = ttk.StringVar(app_frame, "YouTube link")
ttk.Entry(app_frame, textvariable=link_var, width=100).pack(pady=10)

audio_var, video_var = ttk.BooleanVar(app_frame, True), ttk.BooleanVar(app_frame, False)
ttk.Checkbutton(app_frame, text="Audio", variable=audio_var).pack(pady=5, padx=20, side="left")
ttk.Checkbutton(app_frame, text="Video", variable=video_var).pack(pady=5, padx=15, side="left")

copy_var = ttk.IntVar(app_frame, 1)
ttk.Button(app_frame, text="Download", command=lambda: asyncio.run(download(link_var, audio_var, video_var, copy_var))).pack(pady=5, padx=20, side="right")

ttk.Spinbox(app_frame, from_=1, to=10, textvariable=copy_var).pack(pady=5, side="right")

ttk.Label(app_frame, text="Copies: ").pack(pady=5, padx=5, side="right")

result_frame = ttk.Frame(app)

async def download(link_var, audio_var, video_var, copy_var) -> None: 
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
    video = YouTube(link_var.get())
    is_video = video_var.get()
    is_audio = audio_var.get()

    if video is None:
        # If the link is invalid, show an error message
        fail_video = ttk.Label(result_frame, text="Failed to download video:\nInvalid link", foreground="red")
        fail_video.pack(pady=5)
        fail_video.after(3000, fail_video.destroy)
        return

    if video.author in video.title: filename = f'{video.title}.mp4'
    else: filename = f'{video.author} - {video.title}.mp4'
    filename = filename.replace('|', '&').replace('\"', '\'').replace('\\', '-').replace('/', '&').replace('?', '')
    filename_dir = filename.replace(' ', '')
    video_file_dir = os.path.join(CUR_DIR, VIDEO_SAVE_DIRECTORY, filename)
    audio_file_dir = os.path.join(CUR_DIR, AUDIO_SAVE_DIRECTORY, filename)

    if is_video:
        # Get the highest resolution video
        vid = video.streams.get_highest_resolution()
        if vid is None:
            # If no video is found, show an error message
            fail_video = ttk.Label(result_frame, text="Failed to download video:\nNo video found", foreground="red")
            fail_video.pack(pady=5)
            fail_video.after(3000, fail_video.destroy)
            return
        try:
            # Download the video
            vid.download(VIDEO_SAVE_DIRECTORY, filename=filename_dir)
        except Exception as a:
            # If an error occurs during download, show an error message
            fail_video = ttk.Label(result_frame, text=f"Failed to download video:\n{a}", foreground="red")
            fail_video.pack(pady=5)
            fail_video.after(3000, fail_video.destroy)
            return 
        # Replace the downloaded video with the correct name
        os.replace(f"{VIDEO_SAVE_DIRECTORY}/{filename_dir}", video_file_dir)
        # Create copies of the video
        for i in range(copy_var.get() - 1):
            name, ext = os.path.splitext(video_file_dir)
            name = name + f' ({i + 2})' + ext
            copy2(video_file_dir, name)
        # Show a success message
        ok_video = ttk.Label(result_frame, text=f"Video was downloaded successfully:\n{video_file_dir}", foreground="green")
        ok_video.pack(pady=5, side="bottom")
        ok_video.after(3000, ok_video.destroy)
        
    if is_audio:
        # Get the audio with the highest quality
        audio = video.streams.filter(only_audio = True).first()
        if audio is None:
            # If no audio is found, show an error message
            fail_audio = ttk.Label(result_frame, text="Failed to download audio:\nNo audio found", foreground="red")
            fail_audio.pack(pady=5)
            fail_audio.after(3000, fail_audio.destroy)
            return
        try:
            # Download the audio
            audio.download(AUDIO_SAVE_DIRECTORY, filename=filename_dir)
        except Exception as a:
            # If an error occurs during download, show an error message
            fail_audio = ttk.Label(result_frame, text=f"Failed to download audio:\n{a}", foreground="red")
            fail_audio.pack(pady=5)
            fail_audio.after(3000, fail_audio.destroy)
            return
        # Replace the downloaded audio with the correct name
        os.replace(f"{AUDIO_SAVE_DIRECTORY}/{filename_dir}", audio_file_dir)
        # Create copies of the audio
        for i in range(copy_var.get() - 1):
            name, ext = os.path.splitext(audio_file_dir)
            name = name + f' ({i + 2})' + ext
            copy2(audio_file_dir, name)
        # Show a success message
        ok_audio = ttk.Label(result_frame, text=f"Audio was downloaded successfully:\n{audio_file_dir}", foreground="green")
        ok_audio.pack(pady=5, side="bottom")
        ok_audio.after(3000, ok_audio.destroy)
    

if __name__ == "__main__":
    app_frame.pack()
    result_frame.pack()
    app.mainloop()
