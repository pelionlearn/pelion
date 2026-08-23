import { useState, type FormEvent } from "react";
import PopupHeader from "../../components/popup/PopupHeader";
import Popup from "../../components/popup/Popup";
import ColorPicker from "../../components/colorpicker/ColorPicker";

interface CreateClassPopupProps {
    open: boolean;
    onClose: () => void;
    onCreated: (classroom: { id: string; name: string; color: string }) => void;
}

function CreateClassPopup({ open, onClose, onCreated }: CreateClassPopupProps) {
    const [name, setName] = useState("");
    const [color, setColor] = useState("#6b9c6b");
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleSubmit(e: FormEvent) {
        e.preventDefault();
        setSubmitting(true);
        setError(null);

        try {
            const response = await fetch("/api/classrooms", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, color }),
            });

            if (!response.ok) {
                throw new Error("Failed to create class");
            }

            const data = await response.json();
            onCreated(data);
            setName("");
            setColor("#60a5fa");
            onClose();
        } catch (err) {
            setError("Something went wrong. Try again.");
        } finally {
            setSubmitting(false);
        }
    }

    return (
        <Popup open={open} onClose={onClose}>
            <PopupHeader title="Create a class" onClose={onClose} />

            <form onSubmit={handleSubmit}>
                <label className="mb-1 block text-sm text-text-secondary">Class name</label>
                <input
                    type="text"
                    value={name}
                    onChange={e => setName(e.target.value)}
                    placeholder="e.g. AP Biology"
                    className="w-full rounded-lg px-3 py-2 outline outline-dark"
                    required
                    autoFocus
                />

                <label className="mb-1 mt-4 block text-sm text-text-secondary">Color</label>
                <ColorPicker value={color} onChange={setColor} />

                {error && <p className="mt-2 text-sm text-red-500">{error}</p>}

                <div className="mt-6 flex justify-end gap-3">
                    <button
                        type="button"
                        onClick={onClose}
                        className="rounded-xl px-4 py-2 outline outline-dark cursor-pointer hover:bg-white/5"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        disabled={submitting}
                        className="rounded-xl px-4 py-2 bg-primary text-black cursor-pointer disabled:opacity-50"
                    >
                        {submitting ? "Creating..." : "Create"}
                    </button>
                </div>
            </form>
        </Popup>
    );
}

export default CreateClassPopup;