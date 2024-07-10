from flask import Flask, request, jsonify, render_template, send_file
import speech_recognition as sr
import os
import librosa
import numpy as np
import nltk
from gtts import gTTS
import soundfile as sf

app = Flask(__name__)

# Download the necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speech-to-text')
def speech_to_text():
    return render_template('speech_to_text.html')

def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    pos_tags = nltk.pos_tag(tokens)
    prosody = prosody_analysis(tokens, pos_tags)
    return tokens, pos_tags, prosody

def prosody_analysis(tokens, pos_tags):
    prosody_features = [(token, {'stress': 1}) for token in tokens]
    return prosody_features

def g2p_conversion(word, pos):
    phonemes = ['P', 'H', 'O', 'N', 'E', 'M', 'E']
    return phonemes

def text_to_phoneme_sequence(tokens, pos_tags):
    phoneme_sequence = [g2p_conversion(word, pos) for word, pos in zip(tokens, pos_tags)]
    return phoneme_sequence

def prosody_model(phonemes, prosodic_features):
    prosodic_parameters = {'pitch': 1, 'duration': 1}
    return prosodic_parameters

def prosody_generation(phoneme_sequence, prosody):
    prosodic_parameters = [prosody_model(phonemes, prosodic_features) for phonemes, prosodic_features in zip(phoneme_sequence, prosody)]
    return prosodic_parameters

def synthesis_model(phoneme_sequence, prosodic_parameters):
    speech_signal = np.sin(np.linspace(0, 100, 16000))
    return speech_signal

def speech_synthesis(phoneme_sequence, prosodic_parameters):
    speech_signal = synthesis_model(phoneme_sequence, prosodic_parameters)
    output_path = "output.wav"
    sf.write(output_path, speech_signal, 16000)
    return output_path

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    tokens, pos_tags, prosody = preprocess_text(text)
    phoneme_sequence = text_to_phoneme_sequence(tokens, pos_tags)
    prosodic_parameters = prosody_generation(phoneme_sequence, prosody)
    output_path = speech_synthesis(phoneme_sequence, prosodic_parameters)
    return send_file(output_path, as_attachment=True)

@app.route('/gtts', methods=['POST'])
def gtts_speech():
    data = request.get_json()
    text = data.get('text', '')
    tts = gTTS(text=text, lang="en", slow=False)
    output_path = "gtts.wav"
    tts.save(output_path)
    return send_file(output_path, as_attachment=True)

@app.route('/voice-to-text', methods=['POST'])
def voice_to_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    # Save the uploaded file
    audio_path = "uploaded_audio.wav"
    file.save(audio_path)

    # Convert audio to text
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    with audio as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)
    
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)
