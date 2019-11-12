import os
#import magic
import urllib.request
from application import app_instance
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import io
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud.speech_v1 import types

UPLOAD_FOLDER = '/Users/larynqi/desktop/uploads'

app_instance.secret_key = "secret key"
app_instance.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'flac'])

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
    return sample_recognize('output_short.flac')
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
            return sample_recognize('output_short.flac')
            return redirect('/')
        else:
            flash('Allowed file types are txt,pdf, png, jpg, jpeg, gif, flac')
            return redirect(request.url)
if __name__ == "__main__":
    app_instance.run()

# @app_instance.route('/handle_data', methods =['POST'])
# # def handle():
# #     return 'handle'
# def handle_data():
#     import io

#     from google.cloud import speech_v1
#     from google.cloud.speech_v1 import enums
#     from google.cloud.speech_v1 import types

#     #return request.form['projectFilepath']
#     #project = request.form['projectFilepath']
#     if request.method == 'POST':
#         print(hi)
#     # if request.form.get('audiofile'):
#     #     projectpath = request.form.get('audiofile')
#     #     return sample_recognize(projectpath)

#     return render_template('hacks.html')
#     def sample_recognize(local_file_path):
#         """
#         Transcribe a short audio file using synchronous speech recognition
#         Args:
#         local_file_path Path to local audio file, e.g. /path/audio.wav
#         """

#         client = speech_v1.SpeechClient()
#         audio_channel_count = 2 #needs to be pushed

#         file_name = os.path.join(
#             os.path.dirname(__file__),
#             'resources',
#             local_file_path)

#         # The language of the supplied audio
#         language_code = "en-US"

#         # Sample rate in Hertz of the audio data sent
#         sample_rate_hertz = 44100

#         # Encoding of audio data sent. This sample sets this explicitly.
#         # This field is optional for FLAC and WAV audio formats.
#         encoding = enums.RecognitionConfig.AudioEncoding.FLAC
#         config = {
#             "language_code": language_code,
#             "sample_rate_hertz": sample_rate_hertz,
#             "encoding": encoding,
#             "audio_channel_count": audio_channel_count
#         }


#         with io.open(file_name, "rb") as f:
#             content = f.read()
#         audio = {"content": content}
#         #return str(audio)

#         response = client.recognize(config, audio)
#         #return str(response.results)

#         for result in response.results:
#             # First alternative is the most probable result
#             alternative = result.alternatives[0]
#             print(u"Transcript: {}".format(alternative.transcript))
#         return alternative.transcript
#     #return "Hello, World hehe!"
#     return sample_recognize('output_short.flac')
# from application import app_instance
# from flask import render_template, flash, request, redirect, url_for, send_from_directory
# from werkzeug.utils import secure_filename
# import os

# UPLOAD_FOLDER = '/Users/larynqi/uploads'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}

# app_instance.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app_instance.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app_instance.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
    # return render_template('hacks.html')

# @app_instance.route('/Users/larynqi/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app_instance.config['UPLOAD_FOLDER'],
#                                filename)
#@app_instance.route('/')
# def test():
#     return '/'
# @app_instance.route('/home')
# # def home():
# #     return 'home'