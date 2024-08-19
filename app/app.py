from flask import Flask, render_template, request, redirect, url_for
import os
import mysql.connector
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from textblob import TextBlob
from datetime import datetime
import pandas as pd
import subprocess 
import sys  

app = Flask(__name__)

def record_and_analyze_audio():
    print("Recording...")
    fs = 44100  
    duration = 5
    audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    print("Processing...")
    write("output.wav", fs, audio_data)
    transcript = "Recording not transcribed in this example" 
    analysis = TextBlob(transcript)
    voice_sentiment = analysis.sentiment.polarity
    return transcript, voice_sentiment

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_metrics (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transcript TEXT,
            sentiment FLOAT,
            talked_time INT,
            microphone_used VARCHAR(255),
            speaker_used VARCHAR(255),
            timestamp DATETIME,
            session_metadata TEXT
        );
    """)
    conn.commit()
# Save data to SQL
def insert_data(conn, transcript, sentiment, talked_time, microphone_used, speaker_used, timestamp, session_metadata):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_metrics 
        (transcript, sentiment, talked_time, microphone_used, speaker_used, timestamp, session_metadata)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (transcript, sentiment, talked_time, microphone_used, speaker_used, timestamp, session_metadata))
    conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_recording():
    conn = mysql.connector.connect(
        host="db",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    create_table(conn)
    transcript, sentiment = record_and_analyze_audio()
    talked_time = len(transcript.split())
    microphone_used = "Default Microphone"
    speaker_used = "Default Speaker"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_metadata = "Session Data"

    # Save data to CSV file
    data = {
        "transcript": [transcript],
        "sentiment": [sentiment],
        "talked_time": [talked_time],
        "microphone_used": [microphone_used],
        "speaker_used": [speaker_used],
        "timestamp": [timestamp],
        "session_metadata": [session_metadata],
    }
    df = pd.DataFrame(data)
    csv_file = "/app/data/user_metrics.csv"
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False)

    insert_data(conn, transcript, sentiment, talked_time, microphone_used, speaker_used, timestamp, session_metadata)
    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_recording():

    return redirect(url_for('index'))

@app.route('/shutdown', methods=['POST'])
@app.route('/shutdown', methods=['POST'])
def shutdown():

    conn = mysql.connector.connect(
        host="db",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    create_table(conn)
    transcript, sentiment = record_and_analyze_audio()
    talked_time = len(transcript.split())
    microphone_used = "Default Microphone"
    speaker_used = "Default Speaker"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session_metadata = "Session Data"

    # Save data to CSV file
    data = {
        "transcript": [transcript],
        "sentiment": [sentiment],
        "talked_time": [talked_time],
        "microphone_used": [microphone_used],
        "speaker_used": [speaker_used],
        "timestamp": [timestamp],
        "session_metadata": [session_metadata],
    }
    df = pd.DataFrame(data)
    csv_file = "/app/data/user_metrics.csv"
    if os.path.exists(csv_file):
        df.to_csv(csv_file, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file, mode='w', header=True, index=False)

    insert_data(conn, transcript, sentiment, talked_time, microphone_used, speaker_used, timestamp, session_metadata)

    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

    sys.exit(0)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
