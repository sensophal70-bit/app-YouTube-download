import os
import ssl
import certifi

# បិទការត្រួតពិនិត្យ SSL កម្រិតខ្ពស់បំផុតសម្រាប់ម៉ាស៊ីន Render
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
ssl._create_default_https_context = lambda: ctx

os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
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
            'nocheckcertificate': True,
            'legacyserverconnect': True # ជំនួយបន្ថែមពេលមានបញ្ហា SSL
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
