import { useState } from "react";
import { motion } from "motion/react";

function Notes() {
    const [dragging, setDragging] = useState(false);

    const files: [string, Date][] = [
        ["Unit_1_Notes.pdf", new Date(2026, 7, 22, 17, 20, 1, 20)],
        ["Unit_2_Notes.pdf", new Date(2026, 7, 22, 17, 20, 1, 20)],
        ["Unit_3_Notes.pdf", new Date(2026, 7, 22, 17, 20, 1, 20)],
        ["midterm study guide.pdf", new Date(2026, 7, 22, 17, 20, 1, 20)],
        ["carsons_trash_notes.pdf", new Date(2026, 7, 22, 17, 20, 1, 20)]
    ]

    return (
        <motion.main
            className="flex-1 overflow-auto p-8"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
        >
            <h1 className="text-4xl font-bold text-primary">
                Notes
            </h1>

            <div
                className={`
                    mt-8 flex h-64 w-full flex-col items-center justify-center
                    rounded-2xl border-2 border-dashed transition
                    ${
                        dragging
                            ? "border-primary bg-primary/10"
                            : "border-dark hover:border-primary/50"
                    }
                `}
                onDragOver={(e) => {
                    e.preventDefault();
                    setDragging(true);
                }}
                onDragLeave={() => setDragging(false)}
                onDrop={(e) => {
                    e.preventDefault();
                    setDragging(false);

                    const files = e.dataTransfer.files;
                    console.log(files);
                }}
            >
                <i className="fa-solid fa-cloud-arrow-up text-4xl text-primary"/>

                <h2 className="mt-4 text-xl font-semibold">
                    Drop your notes here
                </h2>

                <p className="mt-2 text-text-secondary">
                    Upload PDFs, images, or documents
                </p>

                <label className="mt-5 cursor-pointer rounded-xl bg-primary px-5 py-2 font-medium text-black transition hover:opacity-80">
                    Browse Files
                    <input type="file" multiple className="hidden" accept=".pdf,.png,.jpg,.jpeg,.txt,.doc,.docx"
                        onChange={(e) => {
                            console.log(e.target.files);
                        }}
                    />
                </label>
            </div>

            <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4">
                    Recent Uploads
                </h2>

                <div className="flex flex-col gap-3">
                    {files.map(([filename, date_added]) => (
                        <div
                            key={filename}
                            className="flex items-center justify-between rounded-xl border border-dark bg-white/5 px-3 py-2 transition hover:bg-white/10"
                        >
                            <div className="flex items-center gap-3">
                                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/20 text-primary">
                                    <i className="fa-solid fa-file"/>
                                </div>

                                <div>
                                    <p className="text-md">
                                        {filename}
                                    </p>
                                    <p className="text-sm text-text-secondary">
                                        Uploaded {date_added.toLocaleTimeString()}, {date_added.toLocaleDateString()}
                                    </p>
                                </div>
                            </div>

                            <button className="rounded-lg p-2 text-text-secondary transition hover:bg-white/10 hover:text-primary">
                                <i className="fa-solid fa-ellipsis"/>
                            </button>
                        </div>
                    ))}
                </div>
            </div>
        </motion.main>
    );
}

export default Notes;