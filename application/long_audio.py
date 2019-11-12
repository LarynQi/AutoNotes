from application import app_instance
from flask import render_template, request
@app_instance.route('/')
@app_instance.route('/home')

def index():
    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import speech_v1
    from google.cloud.speech_v1 import enums
    from google.cloud.speech_v1 import types

    def long_running_recognize(storage_uri):
        """
        Transcribe long audio file from Cloud Storage using asynchronous speech
        recognition

        Args:
          storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
        """

        client = speech_v1.SpeechClient()
        audio_channel_count = 2
        #storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

        # file_name = os.path.join(
        #     os.path.dirname(__file__),
        #     'resources',
        #     local_file_path)

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

        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            print(u"Transcript: {}".format(alternative.transcript))
        #return alternative.transcript
        return str(response.results)
    return long_running_recognize('gs://audio_cal/output_2.flac')
