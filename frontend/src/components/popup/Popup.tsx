import { type ReactNode } from "react";
import { AnimatePresence, motion } from "framer-motion";

interface PopupProps {
    open: boolean;
    onClose: () => void;
    children: ReactNode;
    maxWidth?: string;
}

function Popup({ open, onClose, children, maxWidth = "max-w-md" }: PopupProps) {
    return (
        <AnimatePresence>
            {open && (
                <motion.div
                    className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                >
                    <motion.div
                        className={`w-full ${maxWidth} rounded-2xl bg-background border border-dark p-6 text-text`}
                        initial={{ opacity: 0, scale: 0.95, y: -10 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.95, y: -10 }}
                        transition={{ duration: 0.2 }}
                        onClick={e => e.stopPropagation()}
                    >
                        {children}
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}

export default Popup;