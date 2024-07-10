async function textToSpeech() {
    const text = document.getElementById('text').value;
    const response = await fetch('/text-to-speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
}

async function gttsSpeech() {
    const text = document.getElementById('text').value;
    const response = await fetch('/gtts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
    });
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
}

function startVoiceRecognition() {
    if (!('webkitSpeechRecognition' in window)) {
        alert('Web Speech API is not supported in this browser. Please use Google Chrome.');
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = function() {
        document.getElementById('voice-status').innerText = 'Voice recognition started. Speak now.';
    };

    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = 0; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript;
            if (event.results[i].isFinal) {
                finalTranscript += transcript + ' ';
            } else {
                interimTranscript += transcript;
            }
        }

        document.getElementById('transcribed-text').innerText = finalTranscript + interimTranscript;
    };

    recognition.onerror = function(event) {
        document.getElementById('voice-status').innerText = 'Error occurred in voice recognition: ' + event.error;
    };

    recognition.onend = function() {
        document.getElementById('voice-status').innerText = 'Voice recognition ended.';
    };

    recognition.start();
}
