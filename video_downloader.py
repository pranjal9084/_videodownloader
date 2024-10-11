import streamlit as st
import yt_dlp
import os
from tempfile import NamedTemporaryFile

# Streamlit app title
st.title("YouTube Video Downloader - Highest Resolution with yt-dlp")

# Input: YouTube video URL
video_url = st.text_input("Enter the YouTube video URL:")

# Function to handle yt-dlp progress and update the Streamlit progress bar
def progress_hook(d, progress_bar, status_text):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        percentage = downloaded_bytes / total_bytes if total_bytes else 0
        
        # Update the progress bar and status text
        progress_bar.progress(percentage)
        status_text.text(f"Downloading: {percentage * 100:.2f}%")
    
    elif d['status'] == 'finished':
        status_text.text("Download Complete!")

def download_video_with_ytdlp(url, temp_file, progress_bar, status_text):
    # Define yt-dlp options to download the highest resolution video in a single format
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download the best available format
        'outtmpl': temp_file.name,  # Save the video to the temp file
        'progress_hooks': [lambda d: progress_hook(d, progress_bar, status_text)],
        'noplaylist': True  # Prevent downloading playlists
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video
            ydl.download([url])
    except Exception as e:
        raise RuntimeError(f"An error occurred during the download: {e}")

# Button to download video
if st.button("Download Video"):
    if video_url:
        try:
            # Set up the progress bar and status text
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Create a temporary file to store the video
            with NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                # Download video using yt-dlp
                download_video_with_ytdlp(video_url, temp_file, progress_bar, status_text)
                
                # Read the video file to serve it to the user for download
                with open(temp_file.name, "rb") as file:
                    video_bytes = file.read()

                # Provide download button to download the video to local machine
                st.download_button(
                    label="Download Video to Local Machine",
                    data=video_bytes,
                    file_name="downloaded_video.mp4",
                    mime="video/mp4"
                )
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid YouTube URL.")
