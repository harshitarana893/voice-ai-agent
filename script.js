const micBtn = document.getElementById('mic-btn');
const status = document.getElementById('status');
const responseDiv = document.getElementById('response');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (!SpeechRecognition) {
    status.innerText = "Speech Recognition is not supported in this browser. Use Chrome.";
    micBtn.disabled = true;
} else {
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US'; // Gujarati mate 'gu-IN' pan kari shako cho
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micBtn.onclick = () => {
        try {
            recognition.start();
        } catch (e) {
            console.log(e);
        }
    };

    recognition.onstart = () => {
        status.innerText = 'Listening... Speak now.';
        micBtn.style.background = '#2ed573';
    };

    recognition.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        status.innerText = 'AI is thinking...';
        responseDiv.innerText = `You: "${transcript}"`;
        
        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: transcript })
            });
            const data = await res.json();
            
            responseDiv.innerText = data.reply;
            
            // Speak response
            const utterance = new SpeechSynthesisUtterance(data.reply);
            utterance.rate = 1.0;
            window.speechSynthesis.speak(utterance);
        } catch (err) {
            status.innerText = 'Error connecting to server.';
        }
        
        micBtn.style.background = '#ff4757';
    }

    recognition.onerror = (event) => {
        status.innerText = 'Error occurred: ' + event.error;
        micBtn.style.background = '#ff4757';
    };

    recognition.onend = () => {
        if (status.innerText === 'Listening... Speak now.') {
            status.innerText = 'Click mic to speak again';
            micBtn.style.background = '#ff4757';
        }
    };
}