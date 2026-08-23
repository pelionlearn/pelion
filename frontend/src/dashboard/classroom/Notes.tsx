import { useEffect, useState } from "react";
import { motion } from "motion/react";
import { useParams } from "react-router-dom";
import type { NoteType } from "../../types/note";

function Notes() {
    const { classroomId } = useParams();

    const [dragging, setDragging] = useState(false);
    const [uploading, setUploading] = useState(false);
    const [uploadError, setUploadError] = useState<string | null>(null);

    const [files, setFiles] = useState<NoteType[] | null>(null);
    const [error, setError] = useState<string | null>(null);

    function fetchDocuments() {
        if (!classroomId) return;

        setError(null);

        return fetch(`/api/classrooms/${classroomId}/documents/`)
            .then(res => {
                if (!res.ok) throw new Error(`Request failed: ${res.status}`);
                return res.json();
            })
            .then((data: NoteType[]) => {
                setFiles(data);
            })
            .catch(() => {
                setError("Failed to load notes");
            });
    }

    useEffect(() => {
        let cancelled = false;
        setFiles(null);

        fetchDocuments()?.then(() => {
            if (cancelled) return;
        });

        return () => {
            cancelled = true;
        };
    }, [classroomId]);

    async function uploadFiles(fileList: FileList) {
        if (!classroomId || fileList.length === 0) return;

        setUploading(true);
        setUploadError(null);

        try {
            for (const file of Array.from(fileList)) {
                const formData = new FormData();
                formData.append("file", file);

                const response = await fetch(`/api/classrooms/${classroomId}/documents`, {
                    method: "POST",
                    body: formData,
                });

                if (!response.ok) {
                    throw new Error(`Failed to upload ${file.name}`);
                }
            }

            await fetchDocuments();
        } catch (err) {
            setUploadError(err instanceof Error ? err.message : "Upload failed");
        } finally {
            setUploading(false);
        }
    }

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
                    uploadFiles(e.dataTransfer.files);
                }}
            >
                {uploading ? (
                    <>
                        <i className="fa-solid fa-spinner animate-spin text-4xl text-primary" />
                        <h2 className="mt-4 text-xl font-semibold">Uploading...</h2>
                    </>
                ) : (
                    <>
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
                                    if (e.target.files) {
                                        uploadFiles(e.target.files);
                                    }
                                    e.target.value = "";
                                }}
                            />
                        </label>
                    </>
                )}
            </div>

            {uploadError && <p className="mt-3 text-sm text-red-500">{uploadError}</p>}

            <div className="mt-8">
                <h2 className="text-xl font-semibold mb-4">Recent Uploads</h2>

                <div className="flex flex-col gap-3">
                    {error && <div className="text-red-500">{error}</div>}
                    {!error && files?.length === 0 && (
                        <div className="flex items-center justify-center py-10 text-text-secondary">
                            <i className="fa-solid fa-file text-4xl mr-4" />
                            <span className="text-lg">No notes uploaded yet</span>
                        </div>
                    )}
                    {!error && files === null ? (
                        <div className="flex items-center justify-center py-10 text-text-secondary">
                            <i className="fa-solid fa-spinner animate-spin text-4xl mr-4" />
                            <span className="text-lg">Loading...</span>
                        </div>
                    ) : (
                        files?.map((doc, index) => (
                            <motion.div
                                key={doc.id}
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

                                        <p className="truncate text-md">{doc.file_name}</p>
                                    </div>

                                    {/* <div className="hidden xl:flex items-center gap-4 text-sm text-text-secondary ml-3">
                                        <p>
                                            added {doc.date_added.toLocaleTimeString()},{" "}
                                            {doc.date_added.toLocaleDateString()}
                                        </p>

                                        <p className="w-20 text-right">{doc.size} MB</p>
                                    </div>

                                    <p className="text-sm text-text-secondary ml-3 xl:hidden">
                                        {doc.date_added.toLocaleDateString()}
                                    </p> */}
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