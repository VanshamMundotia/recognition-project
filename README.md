# NOVA — AI Assistive Vision for Visually Impaired

This project is a Python-based, offline-first web app designed for visually impaired users. It allows a user to upload an image or capture a live frame from the webcam, generates a natural spatial description using a local LLaVA vision model via Ollama, reads the description aloud using text-to-speech, and logs persistent feedback locally on disk.

Features
- Upload a photo from the device or capture live frames using the webcam
- Generate spatial descriptions, obstacle warnings, and text readings using a local AI vision model
- Convert descriptions into speech automatically so the user can hear them
- High-contrast, responsive Streamlit web interface built for accessibility
- Persistent local feedback loop saving image-correction pairs for continuous improvement

Technology used
- Streamlit for the website UI and custom CSS styling
- Ollama with LLaVA for offline, privacy-first local vision-language processing
- gTTS (Google Text-to-Speech) for text-to-speech audio generation
- Pillow for image processing and format conversion
- JSON and local file storage for persistent feedback logging

Setup
1. Clone or download this repository containing `app.py` and `gui.py`.

2. Ensure Ollama is installed and running on your system, then pull the LLaVA model:
   ollama pull llava
   TO STOP:
   ollama stop llava

3. Open a terminal in the project folder.

4. Install dependencies:
   pip install streamlit ollama gtts pillow

5. Run the app using the GUI script:
   streamlit run gui.py


6. Open the local Streamlit URL in your browser.
   
7. Open new terminal type:
   ngrok http 8501 or(whatever local host it is running on).

8. copy the url from the terminal to share with anyone:
   [https://xxxx-xxxx-xx.ngrok-free.app](https://xxxx-xxxx-xx.ngrok-free.app) (in this format shown in second terminal).
   TO STOP :
   ctrl+c.


Usage
- Upload an image file or use the live webcam stream.
- Click "Re-Analyze & Describe Image" or let it generate automatically.
- Listen to the automated audio narration.
- Provide accuracy feedback using the buttons to help store local corrections.

Notes
- This app runs completely offline using local AI (Ollama/LLaVA), ensuring total data privacy with zero cloud latency.
- Ensure both `app.py` and `gui.py` are placed in the same project directory.
- Webcam support depends on your browser and device permissions.