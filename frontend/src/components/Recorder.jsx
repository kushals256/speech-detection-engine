import React, { useState, useRef, useEffect } from 'react';

const Recorder = ({ onDataReceived, onLatencyUpdate }) => {
    const [isRecording, setIsRecording] = useState(false);
    const websocketRef = useRef(null);
    const audioContextRef = useRef(null);
    const processorRef = useRef(null);
    const streamRef = useRef(null);

    const startRecording = async () => {
        try {
            websocketRef.current = new WebSocket('ws://localhost:8000/ws/dictate');

            websocketRef.current.onopen = () => {
                console.log('WebSocket Connected');
                setIsRecording(true);
                initAudio();
            };

            websocketRef.current.onmessage = (event) => {
                const data = JSON.parse(event.data);
                onDataReceived(data);
                // Calculate latency if timestamp was sent (TODO)
            };

            websocketRef.current.onclose = () => {
                console.log('WebSocket Disconnected');
                setIsRecording(false);
                stopAudio();
            };

        } catch (error) {
            console.error('Error starting recording:', error);
        }
    };

    const initAudio = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            streamRef.current = stream;

            audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 16000 });
            const source = audioContextRef.current.createMediaStreamSource(stream);

            // Buffer size 4096, 1 input channel, 1 output channel
            processorRef.current = audioContextRef.current.createScriptProcessor(4096, 1, 1);

            processorRef.current.onaudioprocess = (e) => {
                if (websocketRef.current?.readyState === WebSocket.OPEN) {
                    const inputData = e.inputBuffer.getChannelData(0);
                    // Convert float32 to int16
                    const pcmData = new Int16Array(inputData.length);
                    for (let i = 0; i < inputData.length; i++) {
                        pcmData[i] = Math.max(-1, Math.min(1, inputData[i])) * 0x7FFF;
                    }
                    websocketRef.current.send(pcmData.buffer);
                }
            };

            source.connect(processorRef.current);
            processorRef.current.connect(audioContextRef.current.destination);

        } catch (error) {
            console.error('Error initializing audio:', error);
        }
    };

    const stopRecording = () => {
        if (websocketRef.current) {
            websocketRef.current.close();
        }
        stopAudio();
        setIsRecording(false);
    };

    const stopAudio = () => {
        if (streamRef.current) {
            streamRef.current.getTracks().forEach(track => track.stop());
        }
        if (processorRef.current) {
            processorRef.current.disconnect();
        }
        if (audioContextRef.current) {
            audioContextRef.current.close();
        }
    };

    return (
        <div className="flex flex-col items-center justify-center p-4">
            <button
                onClick={isRecording ? stopRecording : startRecording}
                className={`px-6 py-3 rounded-full font-bold text-white transition-all ${isRecording
                        ? 'bg-red-500 hover:bg-red-600 animate-pulse shadow-[0_0_15px_rgba(239,68,68,0.5)]'
                        : 'bg-blue-600 hover:bg-blue-700 shadow-lg hover:shadow-xl'
                    }`}
            >
                {isRecording ? 'Stop Dictation' : 'Start Dictation'}
            </button>
            {isRecording && <p className="mt-2 text-sm text-gray-500">Listening...</p>}
        </div>
    );
};

export default Recorder;
