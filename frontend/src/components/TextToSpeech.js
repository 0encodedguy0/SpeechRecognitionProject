import React, { useState } from "react";

const TextToSpeech = () => {
    const [text, setText] = useState("");
    const [audioUrl, setAudioUrl] = useState("");
    const [loading, setLoading] = useState(false);

    const handleTextSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        const response = await fetch("http://localhost:8000/text-to-speech/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();
        setAudioUrl(data.path);
        setLoading(false);
    };

    return (
        <div className="mb-6">
            <h2 className="text-xl font-bold mb-4">Текст в речь</h2>
            <form onSubmit={handleTextSubmit}>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Введите текст"
                    rows="4"
                    className="block w-full p-2 mb-4 border rounded"
                />
                <button
                    type="submit"
                    className="bg-blue-500 text-white px-4 py-2 rounded"
                >
                    Преобразовать
                </button>
            </form>
            {loading && <p>Загрузка...</p>}
            {audioUrl && (
                <div className="mt-4">
                    <p>Аудиофайл готов:</p>
                    <audio controls>
                        <source src={`http://localhost:8000/${audioUrl}`} type="audio/wav" />
                        Ваш браузер не поддерживает аудио.
                    </audio>
                </div>
            )}
        </div>
    );
};

export default TextToSpeech;