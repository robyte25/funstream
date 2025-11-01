from flask import Flask, request, send_file, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

# === HTML direkt aus Hauptordner laden ===
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "Kein YouTube-Link angegeben"}), 400

    try:
        filename = "video.mp4"

        ydl_opts = {
            'outtmpl': filename,
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

@app.route('/robots.txt')
def robots_txt():
    return "User-agent: *\nAllow: /\n", 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
