import { motion } from "motion/react";

function Tutor() {
    return (
        <motion.main
            className="flex-1 overflow-auto p-8"
            animate={{ opacity: [0, 1], x: [-50, 0] }}
        >
            <h1 className="text-4xl font-bold text-primary">
                Good evening, Jeremy.
            </h1>

            <p className="mt-4">
                Ask Pelion anything about this class.
            </p>
        </motion.main>
    );
}

export default Tutor;