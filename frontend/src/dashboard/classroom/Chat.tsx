import { motion } from "motion/react";
import { useParams } from "react-router-dom";

type Message = {
    sender: string;
    message: string;
    time: string;
    self?: boolean;
};

function Chat() {
    const { chatId } = useParams<{ chatId: string }>();

    const messages: Message[] = [
        {
            sender: "Teo",
            message: "im gay",
            time: "7:43 PM",
        },
        {
            sender: "Pelion",
            message: "Hi gay, I'm Pelion, your AI assistant. How can I help you today?",
            time: "7:44 PM",
        },
        {
            sender: "Matthew",
            message: "Hi bozo",
            time: "7:44 PM",
        },
        {
            sender: "You",
            message: "hi bozo",
            time: "7:45 PM",
            self: true,
        },
        {
            sender: "Matt",
            message: "i use arch btw",
            time: "7:46 PM",
        },
        {
            sender: "You",
            message: "ur a loser",
            time: "7:47 PM",
            self: true,
        },
    ];

    return (
        <motion.main
            key={chatId}
            className="flex-1 flex flex-col min-h-0"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
        >
            <div className="px-8 pt-6 pb-5 border-b border-white/10">
                <h2 className="text-primary text-xl font-semibold">{chatId}</h2>

                <p className="text-sm mt-1 text-primary">Pelion · You</p>
            </div>

            <div className="flex-1 overflow-y-auto px-8 py-6 space-y-5">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={`flex ${msg.self ? "justify-end" : "justify-start"}`}
                    >
                        <div
                            className={`max-w-[70%] flex flex-col ${
                                msg.self ? "items-end" : "items-start"
                            }`}
                        >
                            <span className="text-sm text-tertiary mb-2 ml-1">
                                {msg.sender} - {msg.time}
                            </span>

                            <div
                                className={`px-4 py-3 rounded-xl ${
                                    msg.self
                                        ? "bg-primary text-black rounded-br-xs"
                                        : "bg-dark text-text rounded-bl-xs"
                                }`}
                            >
                                <p className="text-md leading-relaxed">{msg.message}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="px-8 pb-6 pt-3 text-lg">
                <div className="flex items-center gap-3 border border-white/10 rounded-2xl px-4 py-3">
                    <input
                        type="text"
                        placeholder="Type a message..."
                        className="flex-1 bg-transparent outline-none text-primary placeholder:text-primary/25"
                    />

                    <button
                        type="button"
                        className="cursor-pointer px-2 py-1 rounded-xl text-primary hover:opacity-70 hover:bg-primary/25 transition-opacity"
                    >
                        <i className="fa-solid fa-arrow-right-long" />
                    </button>
                </div>
            </div>
        </motion.main>
    );
}

export default Chat;
