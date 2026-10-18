from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
# អនុញ្ញាតឱ្យ Frontend ពីគ្រប់ Domain អាចហៅមកកាន់ Backend នេះបាន
CORS(app)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "សូមបញ្ចូល Link YouTube"}), 400

    try:
        # បង្កើតឈ្មោះ file បណ្តោះអាសន្ន ដើម្បីកុំឱ្យជាន់គ្នានៅពេលមានអ្នកទាញយកច្រើនក្នុងពេលតែមួយ
        temp_filename = f"video_{uuid.uuid4().hex}.mp4"
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': temp_filename,
            'quiet': True,
            'nocheckcertificate': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=True)
            
        # បញ្ជូនវីដេអូទៅកាន់ Browser ដើម្បី Save
        return send_file(temp_filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# សម្រាប់តេស្តថាតើ Server ដើរឬអត់ពេលចូលមើលតាម Link
@app.route('/', methods=['GET'])
def home():
    return "YouTube Downloader Backend កំពុងដំណើរការដោយជោគជ័យ!"

if __name__ == '__main__':
    # Cloud Server ភាគច្រើនប្រើ Port ដែលផ្តល់ដោយ Environment Variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
