import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "សូមបញ្ចូល Link YouTube"}), 400

    try:
        temp_filename = f"video_{uuid.uuid4().hex}.mp4"
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': temp_filename,
            'quiet': True,
            'nocheckcertificate': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            
        return send_file(temp_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "YouTube Downloader Backend កំពុងដំណើរការ!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
