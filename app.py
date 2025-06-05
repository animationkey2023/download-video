from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    video_id = str(uuid.uuid4())
    output_path = f'/tmp/{video_id}.mp4'

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return send_file(output_path, as_attachment=True, download_name="video.mp4")

if __name__ == '__main__':
    app.run(debug=True)
