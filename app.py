from flask import Flask, render_template, request, Response, send_file
import json
import time

app = Flask(__name__)

# A simple list to store notifications in memory for this session
notifications = []

def event_stream():
    """Generator for Server-Sent Events"""
    while True:
        if notifications:
            # Send the latest notification and clear the queue
            yield f"data: {json.dumps(notifications.pop(0))}\n\n"
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    # ElevenLabs 'post_call_transcription' contains the transcript
    if data and 'data' in data:
        msg = {
            "id": data['data'].get('conversation_id'),
            "summary": data['data'].get('transcript_summary', 'New Call Received'),
            "time": time.strftime('%H:%M:%S')
        }
        notifications.append(msg)
    return "OK", 200

@app.route('/stream')
def stream():
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
