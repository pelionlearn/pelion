import { motion } from "motion/react";

function Tutor() {
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
                    placeholder="Ask anything"
                    className="w-full resize-none rounded-xl border border-dark bg-white/5 p-4 text-primary placeholder:text-text-secondary focus:outline-none focus:ring-2 focus:ring-primary/25 transition"
                />

                <button className="absolute cursor-pointer bottom-4 right-2 rounded-lg bg-primary px-4 py-2 font-medium text-black transition hover:opacity-90">
                    Ask
                </button>
            </div>
        </motion.main>
    );
}

export default Tutor;
