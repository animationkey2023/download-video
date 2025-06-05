from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data['url']
    resolution = data.get('resolution', '360')
    video_id = str(uuid.uuid4())
    output_path = f'/tmp/{video_id}.mp4'

    # Format string: cari mp4 dengan resolusi setara atau di bawah yang diminta
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/best[height<={resolution}]',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file(output_path, as_attachment=True, download_name="video.mp4")
    except Exception as e:
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
