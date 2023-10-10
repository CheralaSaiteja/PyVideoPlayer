import tkinter as tk
import cv2
import argparse
import os
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root, video_path, seek_amount=10):
        self.root = root
        self.root.title("Video Player")
        
        # Set the minimum window size to 720p
        self.root.minsize(1280, 720)

        # Frame to contain buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)  # Add vertical padding

        # Video control buttons
        self.backward_button = tk.Button(button_frame, text="<<", command=self.backward)
        self.play_pause_button = tk.Button(button_frame, text="Play", command=self.toggle_play_pause)
        self.forward_button = tk.Button(button_frame, text=">>", command=self.forward)

        # Pack buttons with padding on the sides
        self.backward_button.pack(side="left", padx=10)  # Add horizontal padding
        self.play_pause_button.pack(side="left", padx=10)  # Add horizontal padding
        self.forward_button.pack(side="left", padx=10)  # Add horizontal padding

        # Check if the video file exists
        if not os.path.isfile(video_path):
            self.show_error("Video file not found.")
            return

        # OpenCV variables
        self.cap = cv2.VideoCapture(video_path)
        self.is_playing = False

        # Create video display canvas
        self.canvas = tk.Canvas(root, width=self.cap.get(3), height=self.cap.get(4))
        self.canvas.pack()

        # Seek amount in seconds
        self.seek_amount = seek_amount

        # Bind key presses for fine control and play/pause
        root.bind("<space>", self.toggle_play_pause)

        # Set up periodic video frame updating
        self.update_video_frame()

    def toggle_play_pause(self, event=None):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def play(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_pause_button.config(text="Pause")
            self.update_video_frame()

    def update_video_frame(self):
        if self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2image)
                self.photo = ImageTk.PhotoImage(image=pil_image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
                self.root.after(30, self.update_video_frame)  # Update video frame every 30ms
            else:
                self.is_playing = False
                self.play_pause_button.config(text="Play")
                self.cap.release()

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play_pause_button.config(text="Play")

    def forward(self):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = current_position + (self.seek_amount * 1000)  # Convert seconds to milliseconds
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def backward(self):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = max(current_position - (self.seek_amount * 1000), 0)  # Convert seconds to milliseconds
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def decrease_seek_amount(self, event):
        self.seek_amount -= 1

    def increase_seek_amount(self, event):
        self.seek_amount += 1

    def show_error(self, message):
        error_label = tk.Label(self.root, text=message, fg="red")
        error_label.pack()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Video Player")
    parser.add_argument("--seek_amount", type=int, default=10, help="Initial seek amount in seconds (default: 10)")
    parser.add_argument("--video", required=True, help="Path to the video file")
    args = parser.parse_args()

    root = tk.Tk()
    app = VideoPlayer(root, args.video, args.seek_amount)
    root.mainloop()
