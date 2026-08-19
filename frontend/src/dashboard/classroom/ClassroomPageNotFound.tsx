import { motion } from "motion/react";

function ClassroomPageNotFound() {
    return (
        <motion.main
            className="flex-1 flex flex-col min-h-0 p-8"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
        >
            <h2 className="text-3xl text-error">404</h2>
            <h2 className="text-xl text-error mt-2">Schrödinger's Page</h2>
            <p className="text-sm mt-2 text-text">You opened the page and the page was dead.</p>
        </motion.main>
    );
}

export default ClassroomPageNotFound;
