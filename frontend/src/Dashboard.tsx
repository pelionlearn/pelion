import { useState } from "react";
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
        <div className="flex h-screen bg-(--bg-950) text-text">
            <div className="flex flex-1 flex-col overflow-hidden">
                {/* top bar */}
                <header className="flex h-18 items-center justify-between border-b border-dark px-8">
                    <h2 className="text-xl">Home</h2>

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

                    {/* classes */}
                    <section className="mt-0">
                        <div className="mb-4 flex justify-between">
                            <h2 className="text-xl font-semibold text-text">
                                Your Classes
                            </h2>

                            <div className="flex gap-6">
                                <button className="button-text text-text hover:text-primary cursor-pointer transition-all duration-150">
                                    <i className="fa-solid fa-user-group mr-2"/>Join
                                </button>

                                <button className="button-text text-text hover:text-primary cursor-pointer transition-all duration-150">
                                    <i className="fa-solid fa-plus mr-2"/>Create
                                </button>
                            </div>
                            
                        </div>

                        <div className="grid gap-5">
                            <div className="rounded-2xl p-6 cursor-pointer outline outline-dark border-l-10 border-secondary">
                                <h3 className="font-semibold">Discrete Math</h3>

                                <p className="mt-2 text-sm text-text-secondary">
                                    24 notes - 18 members
                                </p>
                            </div>
                            <div className="rounded-2xl p-6 cursor-pointer outline outline-dark border-l-10 border-dark">
                                <h3 className="font-semibold">Calculus I</h3>

                                <p className="mt-2 text-sm text-text-secondary">
                                    24 notes - 18 members
                                </p>
                            </div>
                            <div className="rounded-2xl p-6 cursor-pointer outline outline-dark border-l-10 border-tertiary">
                                <h3 className="font-semibold">Government</h3>

                                <p className="mt-2 text-sm text-text-secondary">
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
