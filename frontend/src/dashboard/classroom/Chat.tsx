import { motion } from "motion/react";
import { useParams } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import type { ChatType } from "../../types/chat";

type Message = {
    id: string;
    chat_id: string;
    role: string;
    content: string;
    created_at: string;
};

function Chat() {
    const initialLoad = useRef(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const { classroomId, chatId } = useParams<{ classroomId: string; chatId: string }>();

    const [chat, setChat] = useState<ChatType | null>(null);

    const [userText, setUserText] = useState<string>("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [_, setLoading] = useState(true);

    const [sending, setSending] = useState(false);

    // const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

    useEffect(() => {
        if (!classroomId) return;

        let cancelled = false;

        fetch(`/api/classrooms/${classroomId}/chats/${chatId}`)
            .then(res => {
                if (!res.ok) throw new Error(`Request failed: ${res.status}`);
                return res.json();
            })
            .then(data => {
                if (!cancelled) setChat(data);
            })
            .catch(() => {
                if (!cancelled) setChat(null);
            })

        return () => {
            cancelled = true;
        };
    }, [classroomId, chatId]);

    const fetchMessages = () => {
        if (!classroomId || !chatId) return;
        setLoading(true);
        fetch(`/api/classrooms/${classroomId}/chats/${chatId}/messages`)
            .then(res => {
                if (!res.ok) throw new Error(`Request failed: ${res.status}`);
                return res.json();
            })
            .then(data => {
                setMessages(data);
            })
            .catch(() => {
                setMessages([]);
            })
            .finally(() => {
                setLoading(false);
            });
    };

    useEffect(() => {
        fetchMessages();
        initialLoad.current = true;
    }, [classroomId, chatId]);

    const handleSend = async (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        if (!classroomId || !chatId) return;
        if (userText == "") return;

        setSending(true);
        const message = userText;
        setUserText("");

        // this is basically a fake client-side only message rn
        const userMessage: Message = {
            id: "",
            chat_id: chatId,
            role: "user",
            content: message,
            created_at: new Date().toISOString(),
        };

        setMessages(prev => [...prev, userMessage]);

        const llm_response: Message = await fetch(
            `/api/classrooms/${classroomId}/chats/${chatId}/messages`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ content: message }),
            }
        )
            .then(res => {
                if (!res.ok) throw new Error(`Request failed: ${res.status}`);
                return res.json();
            })
            .finally(() => {
                setSending(false);
            });

        setMessages(prev => [...prev, llm_response]);

        // const prevLength = messages.length;
        // let currLength = messages.length;
        // while (prevLength == currLength) {
        //     await sleep(500);
        //     fetchMessages();
        //     currLength = messages.length;
        //     console.log(prevLength, currLength);
        // }
    };

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({
            behavior: initialLoad.current ? "instant" : "smooth",
        });

        initialLoad.current = false;
    }, [messages]);

    return (
        <motion.main
            key={chatId}
            className="flex-1 flex flex-col min-h-0"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
        >
            <div className="px-8 pt-6 pb-5 border-b border-white/10">
                <h2 className="text-primary text-xl font-semibold">{chat?.name || chatId}</h2>

                <p className="text-sm mt-1 text-primary">Pelion · You</p>
            </div>

            <div className="flex-1 overflow-y-auto px-8 py-6 space-y-5">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.role == "user" ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[70%] flex flex-col ${
                                msg.role == "user" ? "items-end" : "items-start"
                            }`}
                        >
                            <span className="text-sm text-tertiary mb-2 ml-1">
                                {msg.role} - {msg.created_at}
                            </span>

                            <div
                                className={`px-4 py-3 rounded-xl ${
                                    msg.role == "user"
                                        ? "bg-primary text-black rounded-br-xs"
                                        : "bg-dark text-text rounded-bl-xs"
                                }`}
                            >
                                <p className="text-md leading-relaxed whitespace-pre-wrap wrap-break-word">
                                    {msg.content}
                                </p>
                            </div>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div className="px-8 pb-6 pt-3 text-lg">
                <form
                    className="flex items-center gap-3 border border-white/10 rounded-2xl px-4 py-3"
                    onSubmit={handleSend}
                >
                    <input
                        type="text"
                        placeholder="Type a message..."
                        className="text-md flex-1 bg-transparent outline-none text-primary placeholder:text-primary/25"
                        value={userText}
                        onChange={e => setUserText(e.target.value)}
                    />

                    <button
                        type="submit"
                        className="text-md cursor-pointer px-2 py-1 rounded-xl text-primary hover:opacity-70 hover:bg-primary/25 transition-opacity"
                    >
                        {sending ? "..." : <i className="fa-solid fa-arrow-right-long" />}
                    </button>
                </form>
            </div>
        </motion.main>
    );
}

export default Chat;
