import React from 'react';

const TranscriptView = ({ rawText, processedText }) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-6xl mt-8">
            {/* Raw Transcript */}
            <div className="bg-white/80 backdrop-blur-md rounded-2xl p-6 shadow-xl border border-white/20">
                <h3 className="text-lg font-semibold text-gray-700 mb-4 flex items-center">
                    <span className="w-2 h-2 bg-gray-400 rounded-full mr-2"></span>
                    Raw Transcript
                </h3>
                <div className="h-64 overflow-y-auto p-4 bg-gray-50 rounded-xl font-mono text-sm text-gray-600 whitespace-pre-wrap">
                    {rawText || "Waiting for speech..."}
                </div>
            </div>

            {/* Processed Output */}
            <div className="bg-white/90 backdrop-blur-md rounded-2xl p-6 shadow-2xl border border-blue-100 ring-1 ring-blue-50">
                <h3 className="text-lg font-semibold text-blue-700 mb-4 flex items-center">
                    <span className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></span>
                    Intelligent Output
                </h3>
                <div className="h-64 overflow-y-auto p-4 bg-blue-50/50 rounded-xl font-sans text-base text-gray-800 leading-relaxed whitespace-pre-wrap">
                    {processedText || "Ready to process..."}
                </div>
            </div>
        </div>
    );
};

export default TranscriptView;
