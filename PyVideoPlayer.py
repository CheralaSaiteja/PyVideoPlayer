import tkinter as tk
from tkinter import ttk
import cv2
import argparse
import os
from PIL import Image, ImageTk

class PyVideoPlayer:
    def __init__(self, root, video_path, seek_amount=10):
        self.root = root
        self.root.title("Video Player")
        
        # Create a frame for control buttons
        button_frame = tk.Frame(root)
        button_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Video control buttons
        self.backward_button = tk.Button(button_frame, text="<<", command=self.seek_backward)
        self.play_pause_button = tk.Button(button_frame, text="Play", command=self.toggle_play_pause)
        self.forward_button = tk.Button(button_frame, text=">>", command=self.seek_forward)

        # Pack buttons with padding on the sides
        self.backward_button.grid(row=0, column=0, padx=10)  # Add horizontal padding
        self.play_pause_button.grid(row=0, column=1, padx=10)  # Add horizontal padding
        self.forward_button.grid(row=0, column=2, padx=10)  # Add horizontal padding

        # Check if the video file exists
        if not os.path.isfile(video_path):
            self.show_error("Video file not found.")
            return

        # Initialize is_playing
        self.is_playing = False

        # OpenCV variables
        self.cap = cv2.VideoCapture(video_path)

        # Create video display canvas
        self.canvas = tk.Canvas(root)
        self.canvas.pack(expand=True, fill='both')

        # Seek amount in seconds
        self.seek_amount = seek_amount

        # Create a timer to periodically update the progress bar and video frame
        self.update_video()

        # Create a progress bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(side=tk.TOP, padx=10, pady=10)  # Add vertical padding

    def toggle_play_pause(self, event=None):
        if self.is_playing:
            self.pause()
        else:
            self.play()

    def play(self):
        if not self.is_playing:
            self.is_playing = True
            self.play_pause_button.config(text="Pause")
            self.update_video()

    def update_video(self):
        if self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2image)
                self.photo = ImageTk.PhotoImage(image=pil_image)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

                total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
                current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
                if total_frames > 0:
                    progress = (current_frame / total_frames) * 100
                    self.progress_bar["value"] = progress
                self.root.after(30, self.update_video)  # Update video frame and progress bar every 30ms
            else:
                self.is_playing = False
                self.play_pause_button.config(text="Play")
                self.cap.release()

    def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.play_pause_button.config(text="Play")

    def seek_forward(self):
        current_position = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        new_position = current_position + int(self.seek_amount * self.cap.get(cv2.CAP_PROP_FPS))
        
        if new_position < total_frames:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_position)


    def seek_backward(self):
        current_position = self.cap.get(cv2.CAP_PROP_POS_MSEC)
        new_position = max(current_position - (self.seek_amount * 1000), 0)  # Convert seconds to milliseconds
        self.cap.set(cv2.CAP_PROP_POS_MSEC, new_position)

    def show_error(self, message):
        error_label = tk.Label(self.root, text=message, fg="red")
        error_label.pack()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple Video Player")
    parser.add_argument("--seek_amount", type=int, default=10, help="Initial seek amount in seconds (default: 10)")
    parser.add_argument("--video", required=True, help="Path to the video file")
    args = parser.parse_args()

    root = tk.Tk()
    app = PyVideoPlayer(root, args.video, args.seek_amount)
    
    # Get video frame size and update window size
    frame_width = app.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = app.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    root.geometry(f"{int(frame_width)}x{int(frame_height) + 100}")  # Add extra space for controls
    
    root.mainloop()
