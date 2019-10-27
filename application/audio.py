from application import app_instance
from flask import render_template, request

@app_instance.route('/')
@app_instance.route('/index')
@app_instance.route('/handle_data', methods =['POST'])
def handle_data():
    import io
    import os

    from google.cloud import speech_v1
    from google.cloud.speech_v1 import enums
    from google.cloud.speech_v1 import types

    #return request.form['projectFilepath']
    #project = request.form['projectFilepath']
    #return render_template('hacks.html')
    def sample_recognize(local_file_path):
        """
        Transcribe a short audio file using synchronous speech recognition

        Args:
        local_file_path Path to local audio file, e.g. /path/audio.wav
        """

        client = speech_v1.SpeechClient()
        audio_channel_count = 2

        file_name = os.path.join(
            os.path.dirname(__file__),
            'resources',
            local_file_path)

        # The language of the supplied audio
        language_code = "en-US"

        # Sample rate in Hertz of the audio data sent
        sample_rate_hertz = 44100

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.FLAC
        config = {
            "language_code": language_code,
            "sample_rate_hertz": sample_rate_hertz,
            "encoding": encoding,
            "audio_channel_count": audio_channel_count
        }


        with io.open(file_name, "rb") as f:
            content = f.read()
        audio = {"content": content}
        #return str(audio)

        response = client.recognize(config, audio)
        #return str(response.results)

        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
        return alternative.transcript
    #return "Hello, World hehe!"
    return sample_recognize('output_short.flac')
