<script>
    const micBtn = document.getElementById('micBtn');
    const status = document.getElementById('status');
    const userTextDiv = document.getElementById('userText');
    const aiReplyDiv = document.getElementById('aiReply');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        status.innerText = "તમારા બ્રાઉઝરમાં Voice Support ઉપલબ્ધ નથી.";
    } else {
        const recognition = new SpeechRecognition();
        
        // Multilingual Support: ગુજરાતી, હિન્દી, ઈંગ્લિશ બધું જ કેપ્ચર કરવા માટે
        recognition.lang = 'gu-IN'; // Default: gu-IN, hi-IN, or en-IN
        recognition.continuous = false;
        recognition.interimResults = false;

        micBtn.addEventListener('click', () => {
            try {
                recognition.start();
            } catch (e) {
                recognition.stop();
            }
        });

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            status.innerText = "સાંભળી રહ્યો છું... બોલો!";
        };

        recognition.onresult = async (event) => {
            micBtn.classList.remove('listening');
            const text = event.results[0][0].transcript;
            userTextDiv.innerText = text;
            status.innerText = "જવાબ વિચારી રહ્યો છું...";

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text })
                });

                const data = await response.json();
                const reply = data.reply;

                aiReplyDiv.innerText = reply;
                status.innerText = "જવાબ બોલી રહ્યો છું...";

                // Auto Language Text-to-Speech
                speakResponse(reply);

            } catch (err) {
                status.innerText = "Error: જવાબ મેળવવામાં તકલીફ થઈ.";
            }
        };

        recognition.onerror = (event) => {
            micBtn.classList.remove('listening');
            status.innerText = "સાંભળવામાં ભૂલ થઈ. ફરી પ્રયાસ કરો.";
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
        };
    }

    // ઓટોમેટિક જે ભાષાનો જવાબ હશે એ જ ભાષાના એક્સેન્ટમાં બોલશે
    function speakResponse(text) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        
        // અક્ષરો પરથી ભાષા ઓળખીને વોઇસ લેંગ્વેજ સેટ કરવી
        if (/[\u0A80-\u0AFF]/.test(text)) {
            utterance.lang = 'gu-IN'; // Gujarati
        } else if (/[\u0900-\u097F]/.test(text)) {
            utterance.lang = 'hi-IN'; // Hindi
        } else {
            utterance.lang = 'en-US'; // English / Gujlish
        }

        utterance.onend = () => {
            status.innerText = "બોલવા માટે માઈક પર દબાવો";
        };

        window.speechSynthesis.speak(utterance);
    }
</script>
    