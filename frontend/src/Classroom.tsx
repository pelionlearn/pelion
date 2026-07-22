import { useState } from "react";
import "./Demo.css";
import { motion } from "motion/react";

function Classroom() {
    const [active, setActive] = useState("Tutor");

    const items: [string, string][] = [
        ["user-tie", "Tutor"],
        ["note-sticky", "Notes"],
        ["question", "Quizzes"],
        ["comment", "Chat"],
    ];

    return (
        <div className="flex h-screen bg-(--bg-950) text-text">
            {/* sidebar */}
            <aside className="flex w-52 flex-col border-r border-dark">
                <div className="p-6 flex items-center">
                    <img src="/pelion_alt_nobg.svg" alt="Pelion" className="h-10 scale-200" />
                    <h3 className="text-text font-arvo text-2xl ml-3">Pelion</h3>
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
                            className={`button-text rounded-xl px-4 py-1.5 text-left hover:text-primary ${active === name ? "text-primary" : ""}`}
                        >
                            <i className={`fa-solid fa-${icon} mr-3`}></i>
                            {name}
                        </motion.button>
                    ))}
                </motion.nav>
            </aside>

            <div className="flex flex-1 flex-col overflow-hidden">
                {/* top bar */}
                <header className="flex h-18 items-center justify-between border-b border-dark px-8">
                    <h2 className="text-xl">Discrete Math</h2>

                    <div className="flex items-center gap-4">
                        <button className="rounded-xl p-2 transition hover:bg-white/5 cursor-pointer">
                            <i className="fa-solid fa-bell"></i>
                        </button>

                        <button className="flex items-center gap-3 rounded-xl px-4 py-2">
                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary font-semibold text-black">
                                J
                            </div>

                            <div>
                                <p className="font-medium">Jeremy</p>

                                <p className="text-sm text-text-secondary">Student</p>
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
                        <h1 className="text-4xl font-bold text-primary">Good evening, Jeremy.</h1>
                    </div>

                    
                </motion.main>
            </div>
        </div>
    );
}

export default Classroom;
