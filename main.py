from pytube import Playlist
import pyperclip
import sys
import os
import re

playlist_url_pattern = r"(https?://)?(www\.)?(music\.)?youtube\.com/.*list=([a-zA-Z0-9_\-]+)|youtu\.be/([a-zA-Z0-9_\-]+)"


def playlist_url_valid(playlist_url: str):
    """
    This function checks that a given string is a YouTube playlist URL.
    """
    return re.search(playlist_url_pattern, playlist_url)


def organize(working_dir: str, playlist_url: str, valid_exts, debug: bool = True):
    debug_log = []
    playlist = Playlist(playlist_url)

    video_ids = []
    for video in playlist.videos:
        video_ids.append(video.video_id)

    files = os.listdir(working_dir)

    for filename in files:
        old_file_path = os.path.join(working_dir, filename)
        if not os.path.isfile(old_file_path):
            continue

        file_ext = ""
        if filename.count(".") > 0:
            file_ext = filename.split(".")[-1].lower()

        if file_ext in valid_exts:
            video_id, video_title = re.sub(" +", " ", filename).split(" ", 1)
            if video_title.startswith("-"):
                video_title = video_title.replace("-", "", 1).strip()
            if video_id in video_ids:
                video_index = str(video_ids.index(video_id) + 1)
                if len(video_index) == 1:
                    video_index = "0" + video_index
                new_filename = f"{video_index} {video_title}"
            else:
                continue
            debug_log.append(filename + " --> " + new_filename)
            os.rename(old_file_path, os.path.join(working_dir, new_filename))

    if debug:
        if len(debug_log) > 0:
            print("Modified the following files")
            print("\n".join(debug_log))
        else:
            print("No changes were made!")


def main(working_dir: str = os.getcwd()):
    valid_exts = ("mp3", "m4a", "opus", "mkv", "mp4")

    if len(sys.argv) > 1:
        playlist_url = sys.argv[1]
    else:
        playlist_url = pyperclip.paste()
    while not playlist_url_valid(playlist_url):
        print("Invalid playlist URL: ", playlist_url)
        playlist_url = input("Paste a URL: ").strip()

    print("Selected playlist URL is: ", playlist_url)
    organize(working_dir, playlist_url, valid_exts)


if __name__ == '__main__':
    main()
