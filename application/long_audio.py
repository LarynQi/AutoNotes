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

    def find_word(message, word):
        for i in range(len(message)):
            if message[i] == word[0]:
                for j in range(1, len(word)):
                    if i + j > len(message):
                        break
                    if message[i + j] == word[j]:
                        if j == len(word) - 1:
                            return True
                    else:
                        break
        return False
            

    def long_running_recognize(storage_uri):
        """
        Transcribe long audio file from Cloud Storage using asynchronous speech
        recognition

        Args:
          storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
        """

        client = speech_v1.SpeechClient()
        audio_channel_count = 1
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
            
            
        #return alternative.transcript
        with open("/Users/larynqi/desktop/uploads/blank.txt", "w") as f:
            print(stringResult, file=f)
        return original
    return long_running_recognize('gs://audio_cal/61a_test.flac')
