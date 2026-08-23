import { useState, type KeyboardEvent } from "react";
import { motion } from "motion/react";
import { useNavigate, useOutletContext, useParams } from "react-router-dom";
import type { ClassroomOutletContext } from "./Classroom";

function Tutor() {
    const navigate = useNavigate();
    const { classroomId } = useParams();
    const { refetchChats } = useOutletContext<ClassroomOutletContext>();

    const [message, setMessage] = useState("");
    const [creating, setCreating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function handleAsk() {
        const trimmed = message.trim();
        if (!trimmed || !classroomId || creating) return;

        setCreating(true);
        setError(null);

        try {
            const name = trimmed.slice(0, 13) + (trimmed.length > 13 ? "…" : "");

            const response = await fetch(`/api/classrooms/${classroomId}/chats`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name }),
            });

            if (!response.ok) {
                throw new Error(`Request failed: ${response.status}`);
            }

            const chat = await response.json();
            refetchChats();
            navigate(`/dashboard/classroom/${classroomId}/chat/${chat.id}`);
        } catch (err) {
            setError("Failed to start chat. Try again.");
        } finally {
            setCreating(false);
        }
    }

    function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleAsk();
        }
    }

    return (
        <motion.main
            className="flex-1 overflow-auto p-8 max-w-7xl"
            animate={{ opacity: [0, 1], x: [-50, 0] }}
        >
            <h1 className="text-4xl font-bold text-primary">Good evening, Jeremy.</h1>

            <p className="mt-4">Ask anything about this class.</p>

            <div className="relative mt-8">
                <textarea
                    rows={3}
                    value={message}
                    onChange={e => setMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask anything"
                    disabled={creating}
                    className="w-full resize-none rounded-xl border border-dark bg-white/5 p-4 text-primary placeholder:text-text-secondary focus:outline-none focus:ring-2 focus:ring-primary/25 transition disabled:opacity-50"
                />

                <button
                    onClick={handleAsk}
                    disabled={creating || !message.trim()}
                    className="absolute cursor-pointer bottom-4 right-2 rounded-lg bg-primary px-4 py-2 font-medium text-black transition hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {creating ? "Asking..." : "Ask"}
                </button>
            </div>

            {error && <p className="mt-3 text-sm text-red-500">{error}</p>}
        </motion.main>
    );
}

export default Tutor;
