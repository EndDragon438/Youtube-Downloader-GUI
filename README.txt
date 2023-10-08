Welcome!

This folder contains information and software to allow you to download Youtube videos easily!




There are 2 options:

# Option One: yt-gui.exe

This .exe has all dependencies packaged into one file making it very easy to use. This could be blocked by some antivirus, in which case there is also...

# Option Two: yt-gui.py + dependencies

First off, you'll need some dependencies.

Dependency no.1: Python
Click this link (https://www.python.org/downloads/) and click the big yellow "Download Python" button. This will download a .exe file, open that file and click "Install Now"

Dependency no.2: Pip Installs

Start by opening up Command Prompt (press the Windows key and type "cmd" then press Enter)

In Command Prompt, copy paste these three lines:
```bash
pip install ffmpeg
pip install yt-dlp
pip install gooey
```
Now you're pretty much ready to go! Double click the yt-dlp.py file in this folder, and fill out the options!

In the GUI that opens up, there are several options. Here is what they do.

Output Folder: Here you can input where you want to download videos to, either by typing in a filepath or by pressing the "Browse" button and navigating to your destination folder.
Defaults: Enables the default options, don't turn this off!!
Do not DL Full Playlist: Enabled by default, this option makes it so when downloading a video you only download that video and none of the playlist it may be a part of. Disable this option to download YT playlists. (it will grab the playlist from a link to a video in the playlist, or the link to the playlist itself)
Download Audio: This makes it so you will download audio (mp3) files instead of video (mp4) files. Check this if you are downloading music! (if you want to DL both types, you'll have to run it twice)
Input YT Link: this is where you copy paste the link to the video you want to download! Accepts links to any YT platform, (eg. YT Music) and either video or playlist links!

If you're interested in changing the settings more, you'll have to open up yt-gui.py with a text editor and add modifiers to the "Defaults" option section.

Enjoy!!
- end