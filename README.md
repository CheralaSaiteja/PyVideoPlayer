# PyVideoPlayer 

PyVideoPlayer is a simple video player implemented in Python using the tkinter and OpenCV libraries. It allows you to play video files and control playback using a graphical user interface.

## Prerequisites

Before running PyVideoPlayer, ensure you have the following prerequisites installed on your system:

- Python 3.x
- [Pillow](https://pillow.readthedocs.io/en/stable/) 
- [OpenCV](https://pypi.org/project/opencv-python/)
- Tkinter (usually included with Python)

## Getting Started
```bash
# clone the repository
git clone https://github.com/CheralaSaiteja/PyVideoPlayer.git

# cd into repository
cd PyVideoPlayer

# create and activate the environment
# on windows
python -m venev env
env\Scripts\activate
# on mac and linux
python3 -m venev env
source env/bin/activate 

#install dependencies
pip install -r requirements.txt

# run PyVideoPlayer
python3 PyVideoPlayer.py --video Video.mp4

# for help run
python3 PyVideoPlayer.py -h

# deactivate the environment
# on windows
env\Scripts\deactivate
# on mac and linux
deactivate
```
