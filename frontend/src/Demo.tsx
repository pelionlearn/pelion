import { useState } from "react";
import "./Demo.css";
import { motion } from "motion/react";

function Demo() {
    const [active, setActive] = useState("Home");

    const items: [string, string][] = [
        ["house", "Home"],
        ["comment", "Tutor"],
        ["question", "Quizzes"],
        ["magnifying-glass", "Search"],
    ];

    return (
        <div className="flex h-screen bg-(--bg-950) text-(--text)">
            {/* sidebar */}
            <aside className="glass-bar flex w-52 flex-col border-r border-(--border)">
                <div className="p-6">
                    <h1 className="text-4xl font-bold">Pelion</h1>
                </div>

                <motion.nav
                    className="flex flex-1 flex-col gap-1 px-3 text-md"
                    initial="hidden"
                    animate="show"
                    variants={{
                        hidden: {},
                        show: {
                            transition: {
                                staggerChildren: 0.08,
                            },
                        },
                    }}
                >
                    {items.map(([icon, name]) => (
                        <motion.button
                            key={name}
                            variants={{
                                hidden: {
                                    opacity: 0,
                                    x: -20,
                                },
                                show: {
                                    opacity: 1,
                                    x: 0,
                                },
                            }}
                            transition={{
                                duration: 0.3,
                            }}
                            className={`button-text rounded-xl px-4 py-1.5 text-left hover:bg-white/5 ${active === name ? "glass text-(--green-400)" : ""}`}
                        >
                            <i className={`fa-solid fa-${icon} mr-3`}></i>
                            {name}
                        </motion.button>
                    ))}
                </motion.nav>
            </aside>

            <div className="flex flex-1 flex-col overflow-hidden">
                {/* top bar */}
                <header className="glass-bar flex h-18 items-center justify-between border-b border-(--border) px-8">
                    <h2 className="text-xl font-semibold">Home</h2>

                    <div className="flex items-center gap-4">
                        <button className="rounded-xl p-2 transition hover:bg-white/5">
                            <i className="fa-solid fa-bell"></i>
                        </button>

                        <button className="glass flex items-center gap-3 rounded-xl px-4 py-2">
                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-(--green-400) font-semibold text-black">
                                J
                            </div>

                            <div>
                                <p className="font-medium">Jeremy</p>

                                <p className="text-sm text-(--text-secondary)">Student</p>
                            </div>
                        </button>
                    </div>
                </header>

                {/* content */}
                <motion.main
                    className="flex-1 overflow-auto p-8"
                    animate={{ opacity: [0, 1], y: [-20, 0] }}
                    transition={{ duration: 0.5 }}
                >
                    <div className="mb-6">
                        <h1 className="text-4xl font-bold text-(--text)">Good evening, Jeremy.</h1>

                        <p className="mt-3 text-(--text-secondary)">
                            What do you want to learn today?
                        </p>
                    </div>

                    <div className="glass flex items-center rounded-xl border border-(--border) bg-white/5 px-2 py-2">
                        <input
                            className="flex-1 bg-transparent outline-none px-3"
                            placeholder="Ask questions about your notes..."
                        />

                        <button className="rounded-xl button-primary px-5 py-2">Ask</button>
                    </div>

                    {/* classes */}
                    <section className="mt-12">
                        <div className="mb-4 flex justify-between">
                            <h2 className="text-xl font-semibold text-(--green-400)">
                                Your Classes
                            </h2>

                            <button className="button-text text-(--green-400)">
                                + Create Class
                            </button>
                        </div>

                        <div className="cursor-pointer grid grid-cols-3 gap-5">
                            <div className="glass rounded-xl p-6">
                                <h3 className="font-semibold">Discrete Math</h3>

                                <p className="mt-2 text-sm text-(--text-secondary)">
                                    24 notes - 18 members
                                </p>
                            </div>
                        </div>
                    </section>
                </motion.main>
            </div>
        </div>
    );
}

export default Demo;
