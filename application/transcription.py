import os
import urllib.request
from application import app_instance
from flask import Flask, flash, request, redirect, render_template, Response
from werkzeug.utils import secure_filename
import io
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types
import subprocess
import shutil

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

app_instance.secret_key = "secret key"
app_instance.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['mp3', 'mp4', 'wav', 'flac'])

def long_running_recognize(filename):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
        storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    print(filename)
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    mp4path = os.path.join(THIS_FOLDER, filename)
    subprocess.call(['ffmpeg', '-i', mp4path, 'audio_file.flac'])
    filepath = os.path.join(THIS_FOLDER, 'audio_file.flac')
    subprocess.call(['gsutil', 'cp', 'audio_file.flac', 'gs://audio_cal'])
    storage_uri = "gs://audio_cal/audio_file.flac"

    client = speech_v1.SpeechClient()
    audio_channel_count = 1

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
        "audio_channel_count": audio_channel_count,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    stringResult = ""
    original = ""
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript))
        msg = (str(alternative.transcript))
        original += msg
        
        #fix unwarranted leading spaces
        if msg[0] == " ":
            msg = msg[1:]

        #if first word is "and," remove it"
        if (msg[0] == "a" or msg[0] == "A") and msg[1] == "n" and msg[2] == "d":
            msg = msg[3:]
            msg = msg[0].upper() + msg[1:]
            stringResult += "•" + msg + "\n \n"
        else:
            msg = msg[0].upper() + msg[1:]
            stringResult += "• " + msg + "\n \n"
        
    os.remove(mp4path)
    os.remove("audio_file.flac")
    subprocess.call(['gsutil', 'rm', 'gs://audio_cal/**'])

    #return alternative.transcript
    textfilepath = os.path.join(THIS_FOLDER, 'text_file.txt')
    with open(textfilepath, "w") as f:
        print(stringResult, file=f)
    return original


def sample_recognize(local_file_path):
    client = speech_v1.SpeechClient()
    audio_channel_count = 2
    
    file_name = os.path.join(os.path.dirname(__file__), 'resources', local_file_path)

    lnaguage_code = "en-US"

    sample_rate_hertz = 44100

    encoding = enums.RecognitionConfig.AudioEncoding.flac
    config = {
        "language code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "audio_channel_count": audio_channel_count
    }
    with io.open(file.name, "rb") as f:
        content = f.read()
    audio = {"content": content}
    response = client.recognize(config, audio)

    for result in response.results:
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
    return alternative.transcript

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app_instance.route('/')
def upload_form():
    #return sample_recognize('output_short.flac')
    return render_template('upload.html')

@app_instance.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app_instance.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            #return sample_recognize('output_short.flac')
            long_running_recognize(file.filename)
            return redirect('/')
        else:
            flash('Allowed file types are mp3, mp4, wav, flac')
            return redirect(request.url)
if __name__ == "__main__":
    app_instance.run()

@app_instance.route('/download')
def download():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'text_file.txt')
    file = open(my_file, "r")
    returnfile = file.read().encode("utf-8")
    file.close()
    return Response(returnfile, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=Notes!.txt"})