import React, { useState } from "react";

const SpeechToText = () => {
    const [result, setResult] = useState("");
    const [loading, setLoading] = useState(false);

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (file && file.type === "audio/wav") {
            const formData = new FormData();
            formData.append("file", file);

            setLoading(true);
            const response = await fetch("http://localhost:8000/speech-to-text/", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            setResult(data.text || "Не удалось распознать речь");
            setLoading(false);
        } else {
            alert("Пожалуйста, выберите файл в формате WAV.");
        }
    };

    return (
        <div className="mb-6">
            <h2 className="text-xl font-bold mb-4">Речь в текст</h2>
            <input
                type="file"
                accept=".wav"
                onChange={handleFileUpload}
                className="block mb-4"
            />
            {loading && <p>Загрузка...</p>}
            <p>Результат: {result}</p>
        </div>
    );
};

export default SpeechToText;