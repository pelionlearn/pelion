import { motion } from "motion/react";
import { useAuth } from "../auth";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import CreateClassPopup from "./classroom/CreateClassPopup";
import type { ClassroomType } from "../types/classroom";

function Dashboard() {
    const { user } = useAuth();

    const [classrooms, setClassrooms] = useState<ClassroomType[]>([]);
    const [classroomsLoading, setClassroomsLoading] = useState(true);
    const [classroomsError, setClassroomsError] = useState<string | null>(null);

    const [createModalOpen, setCreateModalOpen] = useState(false);

    function handleClassroomCreated(newClassroom: ClassroomType) {
        setClassrooms(prev => [...prev, newClassroom]);
    }

    useEffect(() => {
        if (!user) return;

        let cancelled = false;

        async function fetchClassrooms() {
            try {
                const response = await fetch("/api/users/me/classrooms");

                if (!response.ok) {
                    throw new Error(`Request failed: ${response.status}`);
                }

                const data = await response.json();

                if (!cancelled) {
                    setClassrooms(data);
                }
            } catch (err) {
                if (!cancelled) {
                    setClassroomsError("Failed to load classrooms");
                }
            } finally {
                if (!cancelled) {
                    setClassroomsLoading(false);
                }
            }
        }

        fetchClassrooms();

        return () => {
            cancelled = true;
        };
    }, [user]);

    return (
        <div className="flex h-screen bg-(--bg-950) text-text">
            <div className="flex flex-1 flex-col overflow-hidden">
                {/* top bar */}
                <header className="flex h-18 items-center justify-between border-b border-dark px-8">
                    <div className="flex items-center">
                        <img src="/pelion_alt_nobg.svg" alt="Pelion" className="h-10 scale-200" />
                        <h3 className="text-text font-arvo text-2xl ml-3">Pelion</h3>
                    </div>

                    <div className="flex items-center gap-4">
                        <button className="rounded-xl p-2 transition hover:bg-white/5 cursor-pointer">
                            <i className="fa-solid fa-bell"></i>
                        </button>

                        <button className="flex items-center gap-3 rounded-xl px-4 py-2">
                            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary font-semibold text-black">
                                {user?.name[0]}
                            </div>

                            <div>
                                <p className="font-medium">{user?.name}</p>

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
                            <h2 className="text-xl font-semibold text-text">Your Classes</h2>

                            <div className="flex gap-6">
                                <button className="button-text text-text hover:text-primary cursor-pointer transition-all duration-150">
                                    <i className="fa-solid fa-user-group mr-2" />
                                    Join
                                </button>

                                <button
                                    onClick={() => setCreateModalOpen(true)}
                                    className="button-text text-text hover:text-primary cursor-pointer transition-all duration-150"
                                >
                                    <i className="fa-solid fa-plus mr-2" />
                                    Create
                                </button>
                            </div>
                        </div>

                        {classroomsLoading && <div>Loading classrooms...</div>}

                        {classroomsError && <div className="text-red-500">{classroomsError}</div>}

                        {!classroomsLoading && !classroomsError && (
                            <div className="grid gap-5">
                                {classrooms.map((classroom, index) => (
                                    <Link to={`/dashboard/classroom/${classroom.id}`}>
                                        <motion.div
                                            className="rounded-2xl p-6 cursor-pointer outline outline-dark border-l-10 border-secondary"
                                            key={classroom.id}
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            transition={{
                                                delay: index * 0.1,
                                            }}
                                        >
                                            <h3 className="font-semibold">{classroom.name}</h3>

                                            <p className="mt-2 text-sm text-text-secondary">
                                                24 notes - 18 members
                                            </p>
                                        </motion.div>
                                    </Link>
                                ))}
                            </div>
                        )}
                    </section>
                </motion.main>

                <CreateClassPopup
                    open={createModalOpen}
                    onClose={() => setCreateModalOpen(false)}
                    onCreated={handleClassroomCreated}
                />
            </div>
        </div>
    );
}

export default Dashboard;
