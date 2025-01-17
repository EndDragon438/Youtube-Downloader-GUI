import os

from yt_dlp import YoutubeDL

from PySide6.QtCore import QSize, QDir, QRunnable, QThreadPool
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QFileDialog,
    QLabel,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QCheckBox,
    QLineEdit,
    QDialog,
)

# class DownloadLogger(QLabel):
#     def debug(self, msg):
#         if msg.startswith('[debug] '):
#             pass
#         else:
#             print(msg)
#             self.setText(msg)
#     def info(self, msg):
#         pass
#     def warning(self, msg):
#         pass
#     def error(self, msg):
#         print(msg)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # print(help(YoutubeDL))

        self.threadpool = QThreadPool()

        self.setWindowTitle("yt-dlp GUI")
        self.setMinimumSize(QSize(400, 400))

        self.root = os.path.dirname(__file__)

        self.command = [
                    f'{self.root}/ffmpeg.exe',# 1 | ffmpeg location
                    '', # 5 | postprocessor
                    'bestvideo[height>=800]+bestaudio/best[height>=800]', # 6 | format (video/audio)
                    '', # 7 | recode
                    'True', # 8 | no playlist
                    f'{QDir.homePath()}/Downloads', # 9 | output location
                    '', # 10 | target link
                    ]

        mainLayout = QVBoxLayout()
        optionLayout = QGridLayout()


        # Selecting the output folder
        outputSelector = QPushButton("Select Output Location")
        outputSelector.pressed.connect(self.outputDialog)
        optionLayout.addWidget(outputSelector, 0, 0)

        # Selector for the format (Video/Audio)
        formatSelectorGroup = QButtonGroup(self)
        formatSelectorBox = QGroupBox()
        formatSelectorLayout = QVBoxLayout()

        formatSelectorVideo = QRadioButton("Download Video")
        formatSelectorVideo.setChecked(True)
        formatSelectorGroup.addButton(formatSelectorVideo, 0)
        formatSelectorLayout.addWidget(formatSelectorVideo)

        formatSelectorAudio = QRadioButton("Download Audio")
        formatSelectorGroup.addButton(formatSelectorAudio, 1)
        formatSelectorLayout.addWidget(formatSelectorAudio)

        formatSelectorGroup.idClicked.connect(self.selectFormat)
        formatSelectorBox.setLayout(formatSelectorLayout)
        optionLayout.addWidget(formatSelectorBox, 1, 0)

        # Playlist
        playlistButton = QCheckBox("Download playlist?")
        playlistButton.stateChanged.connect(self.setPlaylist)
        optionLayout.addWidget(playlistButton, 0, 1)

        # Recode
        self.recodeButton = QCheckBox("Recode to .mp4?")
        self.recodeButton.stateChanged.connect(self.setRecode)
        optionLayout.addWidget(self.recodeButton, 1, 1)

        # Widget for the options section
        optionWidget = QWidget()
        optionWidget.setLayout(optionLayout)
        mainLayout.addWidget(optionWidget)

        # Target link
        linkField = QLineEdit()
        linkField.setPlaceholderText("Enter target link")
        linkField.textChanged.connect(self.setLink)
        mainLayout.addWidget(linkField)

        # Execute the command
        runButton = QPushButton("Download")
        runButton.pressed.connect(self.download)
        mainLayout.addWidget(runButton)

        # Label to display the current command
        self.commandLabel = QLabel(str(self.command))
        self.commandLabel.setWordWrap(True)
        self.commandLabel.setBackgroundRole(QPalette.Base)
        self.commandLabel.setAutoFillBackground(True)
        self.commandLabel.setMargin(20)
        mainLayout.addWidget(self.commandLabel)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

    def outputDialog(self):
        self.command[5] = QFileDialog.getExistingDirectory(self, "Select Output Folder", QDir.homePath(), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        self.updateCommand()

    def selectFormat(self, id):
        match id:
            case 0:
                self.command[1] = [{'add_chapters': True,
                     'add_infojson': 'if_exists',
                     'add_metadata': True,
                     'key': 'FFmpegMetadata'},
                    {'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}]
                self.command[2] = 'bestvideo[height>=800]+bestaudio/best[height>=800]'
                self.recodeButton.setEnabled(True)
            case 1:
                self.command[1] = [{'key': 'FFmpegExtractAudio',
                     'nopostoverwrites': False,
                     'preferredcodec': 'mp3',
                     'preferredquality': '1'},
                    {'add_chapters': True,
                     'add_infojson': 'if_exists',
                     'add_metadata': True,
                     'key': 'FFmpegMetadata'},
                    {'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}]
                self.command[2] = 'bestaudio/best'
                self.command[3] = 'mp3'
                self.recodeButton.setChecked(False)
                self.recodeButton.setEnabled(False)
            case _:
                print(f'weird id: {id}')
        self.commandLabel.setText(str(self.command))

    def setPlaylist(self, value):
        match value:
            case 2:
                self.command[4] = 'False'
            case 0:
                self.command[4] = 'True'
            case _:
                print(f"weird value: {value}")
        self.updateCommand()

    def setRecode(self, value):
        match value:
            case 0:
                self.command[1] = [{'add_chapters': True,
                     'add_infojson': 'if_exists',
                     'add_metadata': True,
                     'key': 'FFmpegMetadata'},
                    {'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}]
                self.command[3] = ''
            case 2:
                self.command[1] = [{'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                    {'add_chapters': True,
                     'add_infojson': 'if_exists',
                     'add_metadata': True,
                     'key': 'FFmpegMetadata'},
                    {'key': 'FFmpegConcat',
                     'only_multi_video': True,
                     'when': 'playlist'}]
                self.command[3] = 'mp4'
            case _:
                print(f"weird value: {value}")
        self.updateCommand()

    def setLink(self, link):
        self.command[6] = link
        self.updateCommand()

    def updateCommand(self):
        # Update the preview label with the new command
        self.commandLabel.setText(str(self.command))

    def download(self):
        options = {
            'extract_flat': 'discard_in_playlist',
            'ffmpeg_location': self.command[0],
            'final_ext': self.command[3],
            'format': self.command[2],
            'fragment_retries': 10,
            'ignoreerrors': 'only_download',
            'noplaylist': self.command[4],
            'outtmpl': {'default': '%(title)s'},
            'paths': {'home': self.command[5]},
            'postprocessors': self.command[1],
            'retries': 10,
            'updatetime': False,
            # 'logger': Logger()
            'progress_hooks': [self.downloadHook]
        }

        if self.command[3] != '':
            options['final_ext'] = self.command[3]
        
        self.commandLabel.setText("if this is showing for a while, it's cause sometimes i don't get progress from ffmpeg cause that PR still isn't merged\nit's still doin things :3")

        # Multithreading!!
        downloader = Downloader()
        downloader.setOptions(options)
        downloader.setTarget(self.command[6])

        self.threadpool.start(downloader)

    def downloadHook(self, dict):
        print(f"\ndownloadHook called with {dict['status']}")
        try:
            match dict['status']:
                case 'downloading':
                    self.commandLabel.setText(f"{str('%.3f'%dict['elapsed'])} seconds at {str('%.3f'%(dict['speed'].round() / 1000))} kilobytes/second")
                case 'finished':
                    self.commandLabel.setText("Download Complete!")
        except:
            print("\nHook Failed")


class Downloader(QRunnable):
    def __init__(self):
        super().__init__()
        
        self.options = {}
        self.target = ''


    def setOptions(self, options):
        self.options = options

    def setTarget(self, target):
        self.target = target

    def run(self):
        with YoutubeDL(self.options) as ytdl:
            ytdl.download(self.target)

# This class is meant to display logs as yt-dlp is downloading the video, and then close itself.
# However, because of the exec() call the thread is taken up by the dialog box listening for events
# So all the log calls don't get through
# I don't feel like dealing with this right now so i'm just going to provide a version of the .exe with console enabled
class Logger(QDialog):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        self.logLine = QLabel("logging...")
        layout.addWidget(self.logLine)

        self.setLayout(layout)

        self.setWindowTitle("Logs")
        self.exec()

    def debug(self, msg):
        print(f"DEBUG: {msg}")
        if msg.find('[download]') > -1:
            self.logLine.setText(msg[10:])
        elif msg.find('Merger') > -1:
            self.close()
    def info(self, msg):
        print(f"INFO: {msg}")
        pass
    def warning(self, msg):
        print(f"WARN: {msg}")
        pass
    def error(self, msg):
        print(f"ERROR: {msg}")
        pass

app = QApplication([])

window = MainWindow()
window.show()

app.exec()
