import { useState } from "react";
import { useToast } from "./components/toast/toast";

export default function Upload() {
    const [file, setFile] = useState<File | null>(null);
    const toast = useToast();

    const upload = async () => {
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("http://localhost:8000/upload", {
            method: "POST",
            body: formData,
            credentials: "include",
        });

        if (!response.ok) {
            if (response.status === 413) {
                toast.error("File is too large");
                return;
            }

            toast.error("Upload failed");
            return;
        }

        const data = await response.json();
        console.log(data);

        toast.success("Upload successful");
    };

    return (
        <>
            <input
                type="file"
                onChange={e => {
                    if (e.target.files) setFile(e.target.files[0]);
                }}
            />

            <button className="glass button-primary" onClick={upload}>
                Upload
            </button>
        </>
    );
}
