import cv2
import numpy as np
from pathlib import Path
import os

class VideoProcessor:
    def __init__(self, video_path):
        """Initialize the video processor with a path to a MOV file.
        
        Args:
            video_path (str): Path to the MOV video file
        """
        self.video_path = Path(video_path)
        self.cap = cv2.VideoCapture(str(video_path))
        
        if not self.cap.isOpened():
            raise ValueError(f"Error opening video file: {video_path}")
            
        # Get video properties
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    def get_video_info(self):
        """Return basic information about the video."""
        return {
            'fps': self.fps,
            'frame_count': self.frame_count,
            'width': self.width,
            'height': self.height,
            'duration': self.frame_count / self.fps
        }
    
    def extract_frames_every_second(self, output_directory):
        """Extract one frame for every second of video."""
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        
        saved_frames = []
        
        # Calculate frames per second
        frames_per_second = int(self.fps)
        total_seconds = int(self.frame_count / self.fps)
        
        for second in range(total_seconds):
            # Calculate the frame number for this second
            frame_number = int(second * frames_per_second)
            
            # Set frame position
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            ret, frame = self.cap.read()
            
            if ret:
                # Generate filename with timestamp
                secs = second % 60
                timestamp = f"{secs:05.2f}"
                
                filename = f"frame_{timestamp}.jpg"
                output_path = os.path.join(output_directory, filename)
                
                # Save frame
                cv2.imwrite(output_path, frame)
                saved_frames.append(output_path)
        
        return saved_frames
    
    def process_frames(self, process_func=None, output_path=None, start_frame=0, end_frame=None):
        """Process video frames with an optional processing function.
        
        Args:
            process_func (callable, optional): Function to process each frame
            output_path (str, optional): Path to save processed video
            start_frame (int): First frame to process
            end_frame (int, optional): Last frame to process
        """
        if end_frame is None:
            end_frame = self.frame_count
            
        # Set up video writer if output path is provided
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Seek to start frame
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        
        frames_processed = 0
        while self.cap.isOpened() and frames_processed < (end_frame - start_frame):
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Apply processing function if provided
            if process_func:
                frame = process_func(frame)
            
            if output_path:
                out.write(frame)
                
            frames_processed += 1
            
        if output_path:
            out.release()
    
    def extract_frame(self, frame_number):
        """Extract a specific frame from the video.
        
        Args:
            frame_number (int): Frame number to extract
            
        Returns:
            numpy.ndarray: The extracted frame
        """
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = self.cap.read()
        if not ret:
            raise ValueError(f"Could not extract frame {frame_number}")
        return frame
    
    def save_frame(self, frame, output_path):
        """Save a frame to disk.
        
        Args:
            frame (numpy.ndarray): Frame to save
            output_path (str): Path to save the frame
        """
        cv2.imwrite(output_path, frame)
    
    def __del__(self):
        """Release video capture when object is destroyed."""
        self.cap.release()


# # Create a VideoProcessor instance
# processor = VideoProcessor("hart_intercivic.MOV")

# # Extract frames (one per second) to a directory
# output_dir = "extracted_frames"
# saved_frames = processor.extract_frames_every_second(output_dir)

# print(f"Extracted {len(saved_frames)} frames")