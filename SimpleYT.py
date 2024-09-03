from download import download
import ttkbootstrap as ttk
import threading
import os

VIDEO_SAVE_DIRECTORY_NAME = "Video"
AUDIO_SAVE_DIRECTORY_NAME = "Audio"

CUR_DIR = os.getcwd()
VIDEO_SAVE_DIRECTORY = os.path.join(CUR_DIR, VIDEO_SAVE_DIRECTORY_NAME)
AUDIO_SAVE_DIRECTORY = os.path.join(CUR_DIR, AUDIO_SAVE_DIRECTORY_NAME)

app = ttk.Window(themename="darkly")

app_frame = ttk.Frame(app)
result_frame = ttk.Frame(app)
result_text_frame = ttk.Frame(result_frame)

''' WIDGETS '''
link_var = ttk.StringVar(app_frame, "YouTube link")
link_entry = ttk.Entry(app_frame, textvariable=link_var, width=80)
link_entry.pack(pady=10, padx=8)
link_entry.focus()

def link_entry_focus_in(event):
    link_entry["foreground"] = "white"
    link_var.set("")
link_entry.bind("<FocusIn>", link_entry_focus_in)

def link_entry_focus_out(event):
    link_entry["foreground"] = "grey"
    link_var.set("YouTube link" if link_var.get() == "" else link_var.get())
link_entry.bind("<FocusOut>", link_entry_focus_out)


audio_var, video_var = ttk.BooleanVar(app_frame, True), ttk.BooleanVar(app_frame, False)
ttk.Checkbutton(app_frame, text="Audio", variable=audio_var).pack(pady=5, padx=20, side="left")
ttk.Checkbutton(app_frame, text="Video", variable=video_var).pack(pady=5, padx=10, side="left")

def download_threading(): 
    t1=threading.Thread(target=download, args=(link_var, audio_var, video_var, copy_var,
                                               VIDEO_SAVE_DIRECTORY, AUDIO_SAVE_DIRECTORY, result))
    t1.start()
ttk.Button(app_frame, text="Download", command=download_threading).pack(pady=5, padx=20, side="right")

copy_var = ttk.IntVar(app_frame, 1)
ttk.Spinbox(app_frame, from_=1, to=10, textvariable=copy_var, width=6).pack(pady=5, side="right")

ttk.Label(app_frame, text="Copies: ").pack(pady=5, padx=5, side="right")

''' RESULT '''
result_label = ttk.Label(result_frame, text="Results:")
result_label.pack(side="left", padx=5)

result_var = ttk.StringVar(app)
result_text = ttk.Entry(result_text_frame, textvariable=result_var, width=70, background="Black", foreground="White")
result_text.pack()

def result(text="", color="white"):
    result_var.set(text)
    result_text['foreground'] = color


if __name__ == "__main__":
    app_frame.pack()
    result_frame.pack(pady=5)
    result_text_frame.pack(padx=5, pady=5, side="left")
    result()
    app.mainloop()
