import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { motion } from "motion/react";

function Classroom() {
    const navigate = useNavigate();
    const location = useLocation();

    const items: [string, string, string][] = [
        ["user-tie", "Tutor", "tutor"],
        ["note-sticky", "Notes", "notes"],
        ["question", "Quizzes", "quizzes"],
        ["comment", "Chat", "chat"],
    ];

    return (
        <div className="flex h-screen bg-(--bg-950) text-text">
            {/* sidebar */}
            <aside className="flex w-52 flex-col border-r border-dark">
                <div className="p-6 flex items-center">
                    <img
                        src="/pelion_alt_nobg.svg"
                        alt="Pelion"
                        className="h-10 scale-200"
                    />
                    <h3 className="text-text font-arvo text-2xl ml-3">
                        Pelion
                    </h3>
                </div>

                <motion.nav className="flex flex-1 flex-col gap-1 px-3">
                    {items.map(([icon, name, route]) => (
                        <motion.button
                            key={name}
                            onClick={() => navigate(route)}
                            className={`
                                button-text cursor-pointer rounded-xl px-3 py-1.5 text-left
                                hover:text-primary hover:bg-dark
                                ${
                                    location.pathname.endsWith(route)
                                        ? "text-primary bg-dark"
                                        : ""
                                }
                            `}
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
                    <h2 className="text-xl">
                        Discrete Math
                    </h2>
                </header>
                
                {/* content */}
                <Outlet />

            </div>

        </div>
    );
}

export default Classroom;