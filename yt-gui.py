'''
GUI wrapper for yt-dlp

Future:
Seperate window/tab for config editor

Notes:
yt-dlp.exe is in C:\ProgramFiles\Python310\Scripts (for updates etc.)
yt-dlp -U (via cmd to update)


--audio-format mp3 --audio-quality 1 --no-mtime --format bestvideo+bestaudio/best -f mp4       (Defaults)




Seems like it wants to DL vid no matter what, so commenting out this option.
    yt_dlp.add_argument('--no-keep-video',
                        default=True,
                        metavar='Do not download Video',
                        widget='CheckBox')

'''

# Standard Modules/Packages
import os
from pprint import pprint


# Third-Party Modules/Packages
from gooey import Gooey, GooeyParser


# @Gooey(target="ffmpeg", program_name='Frame Extraction v1.0', suppress_gooey_flag=True) 
@Gooey(target="yt-dlp", program_name='YT-DLP GUI', suppress_gooey_flag=True) 
def main():
    parser = GooeyParser(description="GUI for yt-dlp: a downloader for youtube videos")
    yt_dlp = parser.add_argument_group('')
    yt_dlp.add_argument('-P',
                        metavar='Output Folder',
                        help='Folder you want to output to.',
                        widget='DirChooser')
    yt_dlp.add_argument('--audio-format mp3 --audio-quality 1 --no-mtime --format bestvideo+bestaudio/best -f mp4 ',
                        default=True,
                        metavar='Defaults',
                        widget='CheckBox')
    yt_dlp.add_argument('--no-playlist ',
                        default=True,
                        metavar='Do not DL Full playlist',
                        widget='CheckBox')
    yt_dlp.add_argument('--extract-audio ',
                        default=False,
                        metavar='Download audio',
                        widget='CheckBox')

    yt_dlp.add_argument('URL',
                        metavar='Input YT Link',
                        help='What YT link to download',
                        widget='TextField'
                        )
    parser.parse_args()

if __name__ == '__main__':
    main()