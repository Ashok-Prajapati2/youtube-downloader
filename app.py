from flask import Flask, render_template, request, send_file, redirect, url_for, flash, jsonify
from flask_socketio import SocketIO, emit
import yt_dlp
import os
import re
import threading
import time

app = Flask(__name__)
app.secret_key = 'root' 
socketio = SocketIO(app)

DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

progress = {}

def progress_hook(d):
    """Hook to send progress updates to the client."""
    if d['status'] == 'downloading':
        percent = d['_percent_str']
        speed = d['_speed_str']
        eta = d['_eta_str']
        size = d.get('_total_bytes_str', 'Unknown size')
        downloaded = d.get('_downloaded_bytes_str', 'Unknown downloaded')

        progress.update({
            'percent': percent.strip(),
            'speed': speed.strip(),
            'eta': eta.strip(),
            'size': size,
            'downloaded': downloaded
        })
        socketio.emit('progress', progress)
        time.sleep(0.1)

def sanitize_filename(filename):
    """Sanitize filename to remove special characters and spaces."""
    filename = re.sub(r'[\/:*?"<>|]', '', filename)
    filename = re.sub(r'\s+', '', filename)
    filename = re.sub(r'[^\w\-.]', '', filename) 
    return filename

def get_yt_info(url):
    """Fetch video information using yt-dlp."""
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'continuedl': True,
        'noplaylist': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        raise RuntimeError(f"Failed to fetch video info: {str(e)}")

def download_video(url,video_itag,audio_itag):
    """Download video in a background thread."""
    global progress
    if video_itag == "null":
        format_option = f'{audio_itag}'
    else:
        format_option = f'{video_itag}+{audio_itag}'
    try:
        ydl_opts = {
            'format': format_option,
            'merge_output_format': 'mp4',
            'noplaylist': False,
            'continuedl': True,
            'progress_hooks': [progress_hook], 
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        progress['filename'] = filename
        socketio.emit('download_complete', {'filename': filename})
    except Exception as e:
        socketio.emit('error', {'message': str(e)})


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash('Please enter a valid YouTube URL.')
            return redirect(url_for('index'))

        try:
            info = get_yt_info(url)
            formats = info.get('formats', [])
            return render_template('select_quality.html', formats=formats, title=info.get('title'), url=url)
        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    
    url = request.form.get('url')
    video_itag = request.form.get('video_itag') 
    audio_itag = request.form.get('audio_itag')

    if not video_itag or not url or not audio_itag:
        flash('Invalid request. Please try again.')
        return redirect(url_for('index'))
    try:
        thread = threading.Thread(target=download_video, args=(url, video_itag ,audio_itag))
        thread.start()
        return render_template('progress.html',data=progress)


    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/complete', methods=['GET'])
def download_complete():
    filename = progress.get('filename')
    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    return 'File not found', 404

if __name__ == '__main__':
    socketio.run(app, debug=True)
