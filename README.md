# Intelligent Dictation Engine

A real-time, low-latency speech-to-text application that produces clean, structured, and grammatically correct text. This project is designed to run locally without relying on Large Language Models (LLMs), ensuring privacy and speed.

## 🚀 Features

- **Real-time Transcription**: Low-latency speech-to-text using `distil-whisper`.
- **Smart Chunking**: Voice Activity Detection (VAD) ensures natural pauses are respected and words aren't cut off.
- **Grammar Correction**: Lightweight on-device grammar correction using `flan-t5-small`.
- **Text Processing**: Automatic removal of fillers ("umm", "uhh") and repetitions.
- **Privacy First**: Runs entirely locally on your CPU.
- **Modern UI**: Clean, responsive React frontend.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, WebSockets
- **AI/ML**: 
  - STT: `faster-whisper` (distil-small.en)
  - Grammar: `transformers` (google/flan-t5-small)
  - VAD: `webrtcvad`
- **Frontend**: React, Vite, TailwindCSS

## 📦 Installation

### Prerequisites
- Python 3.10+
- Node.js & npm

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

## 🎮 Usage

1. Open your browser and navigate to `http://localhost:5173`.
2. Allow microphone access.
3. Click the **Microphone** icon to start recording.
4. Speak naturally. The system will transcribe and correct your speech in real-time.
5. The "Raw" output shows the direct transcription, while "Processed" shows the cleaned and corrected version.

## ⚡ Performance

- **Latency**: Optimized for ≤1500ms end-to-end latency.
- **Hardware**: Designed to run smoothly on standard CPUs (e.g., Apple Silicon, Intel i5+).
