from application import app_instance

@app_instance.route('/')
@app_instance.route('/index')
def index():
    import io
    import os

    # Imports the Google Cloud client library
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    def transcribe_model_selection(speech_file, model= "video"): #default
        #storage_Uri
        """Transcribe the given audio file synchronously with
        the selected model."""
        from google.cloud import speech

        file_name = os.path.join(
            os.path.dirname(__file__),
            'resources',
            speech_file)

        client = speech.SpeechClient()

        audio_channel_count = 2 

        with open(file_name, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.types.RecognitionAudio(content=content)
        enable_separate_recognition_per_channel = True

        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=44100,
            language_code='en-US',
            model=model,
            audio_channel_count = audio_channel_count,
            enable_separate_recognition_per_channel = enable_separate_recognition_per_channel
            )

        #audio = {"uri": storage_uri} long

        #operation = client.long_running_recognize(config, audio) long

        #print(u"Waiting for operation to complete...") long
        #response = operation.result() long

        response = client.recognize(config, audio)

        for i, result in enumerate(response.results):
            alternative = result.alternatives[0]
            print('-' * 20)
            print('First alternative of result {}'.format(i))
            print(u'Transcript: {}'.format(alternative.transcript))
        return alternative.transcript

    return transcribe_model_selection('output_short.flac')
