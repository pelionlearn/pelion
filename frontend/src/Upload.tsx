import { useState } from "react";

export default function Upload() {
    const [file, setFile] = useState<File | null>(null);

    const upload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,
            credentials: "include",
        });

        const data = await response.json();
        console.log(data);
    };

    return (
        <>
            <input
                type="file"
                onChange={(e) => {
                    if (e.target.files) setFile(e.target.files[0]);
                }}
            />

            <button onClick={upload}>
                Upload
            </button>
        </>
    );
}