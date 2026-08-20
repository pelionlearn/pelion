import { useEffect, useState } from "react";
import { motion } from "motion/react";

function Notes() {
    const [dragging, setDragging] = useState(false);

    const [files, setFiles] = useState<[string, Date, number][] | null>(null);

    useEffect(() => {
        const timeout = setTimeout(() => {
            setFiles([
                ["Syllabus_and_Course_Overview.pdf", new Date(2026, 5, 22, 17, 20, 1, 20), 2.4],
                ["Lecture_Notes_Week_2.pdf", new Date(2026, 5, 29, 16, 45, 12, 10), 18.7],
                ["Homework_1_Solutions.pdf", new Date(2026, 6, 6, 19, 10, 5, 30), 6.8],
                ["Unit_2_Review_Guide.pdf", new Date(2026, 6, 15, 14, 30, 20, 15), 12.3],
                ["Unit_3_Notes.pdf", new Date(2026, 6, 24, 18, 5, 40, 25), 27.9],
                ["midterm study guide.pdf", new Date(2026, 7, 2, 17, 20, 1, 20), 4.5],
                ["Final_Exam_Review_Notes.pdf", new Date(2026, 7, 12, 20, 15, 8, 5), 15.6],
                ["carsons_trash_notes.pdf", new Date(2026, 7, 22, 17, 20, 1, 20), 1.2],
            ]);
        }, 400);

        return () => clearTimeout(timeout);
    }, []);

    return (
        <motion.main
            className="flex-1 overflow-auto p-8"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
        >
            <h1 className="text-4xl font-bold text-primary">Notes</h1>

            <div
                className={`
                    mt-8 flex h-64 w-full flex-col items-center justify-center
                    rounded-xl border-2 border-dashed transition
                    ${
                        dragging
                            ? "border-primary bg-tertiary/10"
                            : "border-dark hover:border-tertiary/50"
                    }
                `}
                onDragOver={e => {
                    e.preventDefault();
                    setDragging(true);
                }}
                onDragLeave={() => setDragging(false)}
                onDrop={e => {
                    e.preventDefault();
                    setDragging(false);

                    const files = e.dataTransfer.files;
                    console.log(files);
                }}
            >
                <i className="fa-solid fa-cloud-arrow-up text-4xl text-primary" />

                <h2 className="mt-4 text-xl font-semibold">Drop your notes here</h2>

                <p className="mt-2 text-text-secondary">Upload PDFs, images, or documents</p>

                <label className="mt-5 cursor-pointer rounded-xl bg-primary px-5 py-2 font-medium text-black transition hover:opacity-80">
                    Browse Files
                    <input
                        type="file"
                        multiple
                        className="hidden"
                        accept=".pdf,.png,.jpg,.jpeg,.txt,.doc,.docx"
                        onChange={e => {
                            console.log(e.target.files);
                        }}
                    />
                </label>
            </div>

            <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4">Recent Uploads</h2>

                <div className="flex flex-col gap-3">
                    {files === null ? (
                        <div className="flex items-center justify-center py-10 text-text-secondary">
                            <i className="fa-solid fa-spinner animate-spin text-4xl mr-4" />
                            <span className="text-lg">Loading...</span>
                        </div>
                    ) : (
                        files
                            .sort((a, b) => b[1].getTime() - a[1].getTime())
                            .map(([filename, date_added, size_mb], index) => (
                                <motion.div
                                    key={filename}
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    transition={{
                                        delay: index * 0.05,
                                    }}
                                    className="flex items-center justify-between rounded-xl border border-dark bg-white/5 px-3 py-2 transition hover:bg-white/10"
                                >
                                    <div className="flex flex-1 min-w-0 items-center justify-between">
                                        <div className="flex items-center gap-3 min-w-0">
                                            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-secondary/20 text-secondary">
                                                <i className="fa-solid fa-file" />
                                            </div>

                                            <p className="truncate text-md">{filename}</p>
                                        </div>

                                        <div className="hidden xl:flex items-center gap-4 text-sm text-text-secondary ml-3">
                                            <p>
                                                added {date_added.toLocaleTimeString()},{" "}
                                                {date_added.toLocaleDateString()}
                                            </p>

                                            <p className="w-20 text-right">{size_mb} MB</p>
                                        </div>

                                        {/* smaller screen widths */}
                                        <p className="text-sm text-text-secondary ml-3 xl:hidden">
                                            {date_added.toLocaleDateString()}
                                        </p>
                                    </div>

                                    <button className="rounded-xl p-2 ml-3 text-text-secondary transition hover:bg-white/10 hover:text-primary">
                                        <i className="fa-solid fa-ellipsis" />
                                    </button>
                                </motion.div>
                            ))
                    )}
                </div>
            </div>
        </motion.main>
    );
}

export default Notes;
