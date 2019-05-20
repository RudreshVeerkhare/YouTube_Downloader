#!/usr/bin/env python3

import gi
import os
from pytube import YouTube

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

home_path = os.path.expanduser('~')
cache_folder = os.path.join(home_path, "ytd_cache")
download_folder = os.path.join(home_path, "Downloads/ytd_downloads")
os.makedirs(cache_folder, exist_ok=True)
os.makedirs(download_folder, exist_ok=True)

file_size = 0

class Handler:
    def __init__(self):
        self.yt = None

    def check_url(self, entry):
        url = url_window_entry.get_text()
        if url == "":
            url_window_error_message.set_text("Please Enter Valid URL")
            return
        try:
            ytv = YouTube(url, on_progress_callback=fill_progress_bar, on_complete_callback=complete)
            download_window_title_label.set_text(ytv.title)
            img_path = download_image(ytv.thumbnail_url, ytv.title)

            self.yt = ytv.streams.filter(progressive=True)

            video_thumbnail.set_from_file(img_path)

            # list of all available resolutions
            res_list = [i.resolution for i in self.yt.all()]
            res_set = set(res_list)

            # list added to dropdown
            for i in res_set:
                download_window_dropdown.append_text(i)

            hide_url_window()

        except:
            url_window_error_message.set_text(
                "Please Enter Valid URL and Check Your internet connection"
            )
            return

    def start_download(self, button):
        quality = download_window_dropdown.get_active_text()
        if quality == "":
            return

        set_filesize(self.yt.filter(res=quality).first())
        hide_download_window()

        self.yt.filter(res=quality).first().download(download_folder)
        

    def to_url_window(self, button):
        hide_final_window()

    def close(self, *args):
        Gtk.main_quit()


def hide_url_window():
    download_window.show_all()
    url_window.hide()
    url_window_entry.set_text("")


def hide_download_window():
    final_window.show_all()
    final_window_continue.hide()
    final_window_exit.hide()
    download_window.hide()


def hide_final_window():
    final_window.hide()
    url_window_entry.set_text("")
    url_window.show_all()

def download_image(url, title):
    import urllib.request
    file_path = os.path.join(cache_folder, title)
    with urllib.request.urlopen(url) as responce:
        with open(file_path, 'wb') as f:
            f.write(responce.read())
    
    return file_path

def set_filesize(yt):

    global file_size
    file_size = yt.filesize

def fill_progress_bar(stream, chunk, file_handle, remaning):
    fraction = round(((file_size - remaning) / file_size), 2)
    progress_bar.set_fraction(fraction)
    while Gtk.events_pending():
        Gtk.main_iteration()

def complete(stream, file_handle):
    final_window_message.set_text("Download Complete")
    final_window_continue.show()
    final_window_exit.show()


builder = Gtk.Builder()
builder.add_from_file("test.glade")
builder.connect_signals(Handler())


url_window = builder.get_object("url_window")
download_window = builder.get_object("download_window")
final_window = builder.get_object("final_window")

# url_window widgets
url_window_image = builder.get_object("url_builder_image")
url_window_error_message = builder.get_object("url_window_error_message")
url_window_entry = builder.get_object("url_window_entry")

# download_window widgets
download_window_title_label = builder.get_object("download_window_title_label")
video_thumbnail = builder.get_object("video_thumbnail")
download_window_dropdown = builder.get_object("download_window_dropdown")
download_page_start_button = builder.get_object("download_page_start_button")

# final_window widgets
final_window_message = builder.get_object("final_window_message")
progress_bar = builder.get_object("progress_bar")
final_window_continue = builder.get_object("final_window_continue")
final_window_exit = builder.get_object("final_window_exit")

# show url_window
url_window.show_all()


Gtk.main()
