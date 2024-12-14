import React, { useState } from "react";
import axios from "axios";

function App() {
    const [file, setFile] = useState(null);
    const [text, setText] = useState("");
    const [taskId, setTaskId] = useState("");
    const [status, setStatus] = useState("");
    const [audioUrl, setAudioUrl] = useState("");

    const handleFileChange = (e) => setFile(e.target.files[0]);

    const handleSTT = async () => {
        const formData = new FormData();
        formData.append("file", file);
        const response = await axios.post("http://localhost:8000/speech-to-text/", formData);
        setTaskId(response.data.task_id);
    };

    const handleTTS = async () => {
        const response = await axios.post("http://localhost:8000/text-to-speech/", { text });
        setTaskId(response.data.task_id);
    };

    const checkStatus = async () => {
        const response = await axios.get(`http://localhost:8000/task-status/${taskId}/`);
        setStatus(response.data.status);
        if (response.data.status === "Completed") {
            setAudioUrl(response.data.result);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center">
            <h1 className="text-4xl font-bold text-blue-600">Speech Processing App</h1>
            <div className="w-1/2 mt-5">
                <input
                    type="file"
                    className="border rounded p-2 w-full"
                    onChange={handleFileChange}
                />
                <button
                    onClick={handleSTT}
                    className="mt-3 bg-blue-500 text-white py-2 px-4 rounded"
                >
                    Convert Speech to Text
                </button>
            </div>
            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="mt-5 w-1/2 h-40 p-3 border rounded"
            />
            <button
                onClick={handleTTS}
                className="mt-3 bg-green-500 text-white py-2 px-4 rounded"
            >
                Convert Text to Speech
            </button>
            {taskId && (
                <div className="mt-5">
                    <button onClick={checkStatus} className="bg-yellow-500 text-white py-2 px-4 rounded">
                        Check Task Status
                    </button>
                    <p className="mt-3">Status: {status}</p>
                </div>
            )}
            {audioUrl && (
                <audio className="mt-5" controls>
                    <source src={`http://localhost:8000/${audioUrl}`} type="audio/mpeg" />
    </audio>
    )}
    </div>
    );
}

export default App;