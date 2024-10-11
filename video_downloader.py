import streamlit as st
import yt_dlp
import os

# Streamlit app title
st.title("YouTube Video Downloader - Highest Resolution with yt-dlp")

# Input: YouTube video URL
video_url = st.text_input("Enter the YouTube video URL:")

# Folder for temporary downloads on the server
TEMP_FOLDER = "temp_videos"

# Ensure the folder exists
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

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
    # Define yt-dlp options to download the highest resolution video
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
    if video_url:
        try:
            # Set up the progress bar and status text
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Download video using yt-dlp
            video_title = download_video_with_ytdlp(video_url, TEMP_FOLDER, progress_bar, status_text)
            
            video_path = os.path.join(TEMP_FOLDER, f"{video_title}.mp4")
            
            # Open the downloaded video for user download
            with open(video_path, 'rb') as video_file:
                video_bytes = video_file.read()
                st.download_button(
                    label=f"Download {video_title}",
                    data=video_bytes,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4"
                )
            
            # After download, delete the video file from the server
            os.remove(video_path)
            st.success(f"{video_title} has been downloaded and deleted from the server.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a valid YouTube URL.")
