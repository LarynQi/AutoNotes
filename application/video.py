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

    def transcribe_model_selection(speech_file, model=video):
        """Transcribe the given audio file synchronously with
        the selected model."""
        from google.cloud import speech
        client = speech.SpeechClient()

        with open(speech_file, 'rb') as audio_file:
            content = audio_file.read()

        audio = speech.types.RecognitionAudio(content=content)

        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            language_code='en-US',
            model=model)

        response = client.recognize(config, audio)

        for i, result in enumerate(response.results):
            alternative = result.alternatives[0]
            print('-' * 20)
            print('First alternative of result {}'.format(i))
            print(u'Transcript: {}'.format(alternative.transcript))
    return transcribe_model_selection()