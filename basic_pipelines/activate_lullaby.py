# When called will activate a lullaby / song / melody


# Add to install.sh
# sudo apt update
# sudo apt install mpg321
# mpg321 /home/hailo/Downloads/brahmsx27-lullaby-160672.mp3
# curl -L "https://drive.usercontent.google.com/uc?id=1Myk5VzIQWYDbjp-zYiFjUwQn15HQyuPU&export=download" -o brahms-lullaby.mp3 
# mpg321 brahms-lullaby.mp3
import requests
import tempfile
import os
from playsound import playsound
import atexit
import signal
import sys

temp_file_path = None

def cleanup():
    global temp_file_path
    if temp_file_path and os.path.exists(temp_file_path):
        print("Cleaning up temporary file...")
        os.remove(temp_file_path)

def download_mp3(url):
    global temp_file_path

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file_path = temp_file.name

        # Register cleanup function
        atexit.register(cleanup)

        # Download the MP3 file
        print("Downloading the MP3 file...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Write the content to the temp file
        for chunk in response.iter_content(chunk_size=1024):
            temp_file.write(chunk)

    print(f"File downloaded to {temp_file_path}")
    return temp_file_path

def play_mp3(mp3_file_path):
    try:
        # Play the MP3 file
        print("Playing the MP3 file...")
        playsound(mp3_file_path)
    except Exception as e:
        print(f"An error occurred while playing the file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <mp3_file_path_or_url>")
        sys.exit(1)

    input_path_or_url = sys.argv[1]

    if input_path_or_url.startswith("http://") or input_path_or_url.startswith("https://"):
        mp3_file_path = download_mp3(input_path_or_url)
    else:
        mp3_file_path = input_path_or_url

    try:
        play_mp3(mp3_file_path)
    finally:
        cleanup()