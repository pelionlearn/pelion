import "./App.css";

function App() {
    return (
        <div className="flex h-screen bg-(--bg-950) text-(--text)">
            {/* Sidebar */}
            <aside className="glass-bar flex w-72 flex-col border-r border-(--border)">
                <div className="p-6">
                    <h1 className="text-4xl font-bold">Pelion</h1>
                </div>

                <nav className="flex flex-1 flex-col gap-1 px-3 text-xl">
                    <button className="glass rounded-xl bg-white/8 px-4 py-3 text-left">
                        <i className="fa-solid fa-house mr-3"></i>
                        Home
                    </button>

                    <button className="button-text rounded-xl px-4 py-3 text-left transition hover:bg-white/5">
                        <i className="fa-solid fa-users mr-3"></i>
                        Classes
                    </button>

                    <button className="button-text rounded-xl px-4 py-3 text-left transition hover:bg-white/5">
                        <i className="fa-solid fa-comment mr-3"></i>
                        Tutor
                    </button>

                    <button className="button-text rounded-xl px-4 py-3 text-left transition hover:bg-white/5">
                        <i className="fa-solid fa-question mr-3"></i>
                        Quizzes
                    </button>

                    <button className="button-text rounded-xl px-4 py-3 text-left transition hover:bg-white/5">
                        <i className="fa-solid fa-magnifying-glass mr-3"></i>
                        Search
                    </button>

                    <div className="mt-auto mb-4">
                        <button className="button-text w-full rounded-xl px-4 py-3 text-left transition hover:bg-white/5">
                            <i className="fa-solid fa-gear mr-3"></i>
                            Settings
                        </button>
                    </div>
                </nav>
            </aside>

            {/* Application */}
            <div className="flex flex-1 flex-col overflow-hidden">
                {/* Top bar */}
                <header className="glass-bar flex h-18 items-center justify-between border-b border-(--border) px-8">
                    <h2 className="text-xl font-semibold">Home</h2>

                    <div className="flex items-center gap-4">
                        <button className="rounded-xl p-2 transition hover:bg-white/5">
                            <i className="fa-solid fa-bell"></i>
                        </button>

                        <button className="glass flex items-center gap-3 rounded-xl px-4 py-2">
                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-(--green-500) font-semibold text-black">
                                J
                            </div>

                            <div>
                                <p className="font-medium">Jeremy</p>

                                <p className="text-sm text-(--text-secondary)">Student</p>
                            </div>
                        </button>
                    </div>
                </header>

                {/* Content */}
                <main className="flex-1 overflow-auto p-8">
                    <div className="mb-8">
                        <h1 className="text-4xl font-bold">Good evening, Jeremy</h1>

                        <p className="mt-2 text-(--text-secondary)">
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

                    {/* Classes */}
                    <section className="mt-8">
                        <div className="mb-4 flex justify-between">
                            <h2 className="text-xl font-semibold">Your Classes</h2>

                            <button className="button-text text-(--green-400)">+ Create Class</button>
                        </div>

                        <div className="grid grid-cols-3 gap-5">
                            <div className="glass rounded-xl p-6">
                                <h3 className="font-semibold">Discrete Math</h3>

                                <p className="mt-2 text-sm text-(--text-secondary)">
                                    24 notes - 18 members
                                </p>
                            </div>
                        </div>
                    </section>
                </main>
            </div>
        </div>
    );
}

export default App;
