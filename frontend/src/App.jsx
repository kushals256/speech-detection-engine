import React, { useState } from 'react';
import Recorder from './components/Recorder';
import TranscriptView from './components/TranscriptView';
import Controls from './components/Controls';
import { Mic, Activity } from 'lucide-react';

function App() {
  const [rawText, setRawText] = useState('');
  const [processedText, setProcessedText] = useState('');
  const [tone, setTone] = useState('neutral');
  const [latency, setLatency] = useState(0);

  const handleDataReceived = (data) => {
    if (data.raw) {
      setRawText(prev => prev + " " + data.raw);
    }
    if (data.processed) {
      setProcessedText(prev => prev + " " + data.processed);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col items-center py-12 px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 tracking-tight flex items-center justify-center gap-3">
          <Mic className="w-10 h-10 text-blue-600" />
          Intelligent Dictation
        </h1>
        <p className="mt-3 text-lg text-gray-500 font-medium">
          Real-time, filler-free, and tone-perfect speech to text.
        </p>
      </div>

      {/* Controls & Recorder */}
      <div className="flex flex-col items-center space-y-6 w-full max-w-xl">
        <Controls tone={tone} setTone={setTone} />
        <Recorder onDataReceived={handleDataReceived} />
      </div>

      {/* Transcript View */}
      <TranscriptView rawText={rawText} processedText={processedText} />

      {/* Latency Indicator (Mockup for now) */}
      <div className="fixed bottom-4 right-4 bg-white/80 backdrop-blur px-3 py-1 rounded-full text-xs font-mono text-gray-400 border border-gray-200 flex items-center gap-2">
        <Activity className="w-3 h-3" />
        Latency: {latency < 1500 ? <span className="text-green-500">≤1500ms</span> : <span className="text-red-500">{latency}ms</span>}
      </div>
    </div>
  );
}

export default App;
