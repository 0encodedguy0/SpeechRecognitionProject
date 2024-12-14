import React from "react";
import SpeechToText from "./components/SpeechToText";
import TextToSpeech from "./components/TextToSpeech";

const App = () => {
    return (
        <div className="container mx-auto p-6">
            <h1 className="text-3xl font-bold mb-6">Speech Processing App</h1>
            <SpeechToText />
            <TextToSpeech />
        </div>
    );
};

export default App;