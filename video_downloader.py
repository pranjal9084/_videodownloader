import streamlit as st
import yt_dlp
import os

# Streamlit app title
st.title("YouTube Video Downloader - Highest Resolution with yt-dlp")

# Input: YouTube video URL
video_url = st.text_input("Enter the YouTube video URL:")

# Input: Folder path for saving the downloaded video
folder_path = st.text_input("Enter the folder path where you want to save the video:", "Downloads/")

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

def download_video_with_ytdlp(url, folder, progress_bar, status_text):
    # Ensure the folder exists, create if it doesn't
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Define yt-dlp options to download the highest resolution video in a single format
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download the best available format
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),  # Save the video in the chosen folder
        'progress_hooks': [lambda d: progress_hook(d, progress_bar, status_text)],
        'noplaylist': True  # Prevent downloading playlists
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download the video and extract video info
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'downloaded_video')  # Default title if extraction fails
            
            # Start downloading
            ydl.download([url])
        
        return video_title
    except Exception as e:
        raise RuntimeError(f"An error occurred during the download: {e}")

# Button to download video
if st.button("Download Video"):
    if video_url and folder_path:
        try:
            # Set up the progress bar and status text
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Download video using yt-dlp
            video_title = download_video_with_ytdlp(video_url, folder_path, progress_bar, status_text)
            st.success(f"Downloaded: {video_title}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter both a valid YouTube URL and a folder path.")
