import React from 'react';

const Controls = ({ tone, setTone }) => {
    const tones = ['Neutral', 'Formal', 'Casual', 'Concise'];

    return (
        <div className="flex items-center space-x-4 bg-white/50 backdrop-blur-sm p-2 rounded-full border border-white/20 shadow-sm mt-6">
            <span className="text-sm font-medium text-gray-600 pl-3">Tone:</span>
            <div className="flex space-x-1">
                {tones.map((t) => (
                    <button
                        key={t}
                        onClick={() => setTone(t.toLowerCase())}
                        className={`px-4 py-1.5 rounded-full text-sm transition-all ${tone === t.toLowerCase()
                                ? 'bg-white text-blue-600 shadow-md font-semibold'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-white/30'
                            }`}
                    >
                        {t}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default Controls;
