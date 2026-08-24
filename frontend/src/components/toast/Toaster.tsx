import { useEffect } from "react";
import { AnimatePresence, motion } from "motion/react";

export type ToastType = "success" | "error" | "info";

export interface Toast {
    id: number;
    type: ToastType;
    message: string;
    duration: number;
}

interface ToasterProps {
    toasts: Toast[];
    onDismiss: (id: number) => void;
}

interface ToastItemProps {
    toast: Toast;
    onDismiss: (id: number) => void;
}

const icons: Record<ToastType, string> = {
    success: "fa-solid fa-circle-check",
    error: "fa-solid fa-circle-exclamation",
    info: "fa-solid fa-circle-info",
};

const accents: Record<ToastType, string> = {
    success: "border-l-secondary text-secondary",
    error: "border-l-error text-error",
    info: "border-l-tertiary text-tertiary",
};

function ToastItem({ toast, onDismiss }: ToastItemProps) {
    useEffect(() => {
        const timer = setTimeout(() => onDismiss(toast.id), toast.duration);
        return () => clearTimeout(timer);
    }, [toast.id, toast.duration, onDismiss]);

    return (
        <motion.div
            layout
            role={toast.type === "error" ? "alert" : "status"}
            className={`pointer-events-auto flex items-start gap-3 rounded-2xl border border-dark border-l-4 bg-background p-4 text-text shadow-lg ${accents[toast.type]}`}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 50 }}
            transition={{ duration: 0.2 }}
        >
            <i className={`${icons[toast.type]} mt-0.5`} aria-hidden="true" />
            <p className="flex-1 text-sm leading-relaxed">{toast.message}</p>
            <button
                type="button"
                onClick={() => onDismiss(toast.id)}
                className="cursor-pointer text-text-secondary transition-colors hover:text-text"
                aria-label="Dismiss notification"
            >
                <i className="fa-solid fa-xmark" aria-hidden="true" />
            </button>
        </motion.div>
    );
}

function Toaster({ toasts, onDismiss }: ToasterProps) {
    return (
        <div
            aria-live="polite"
            className="pointer-events-none fixed bottom-6 right-6 z-50 flex w-[calc(100vw-3rem)] flex-col gap-3 sm:w-96"
        >
            <AnimatePresence>
                {toasts.map(toast => (
                    <ToastItem key={toast.id} toast={toast} onDismiss={onDismiss} />
                ))}
            </AnimatePresence>
        </div>
    );
}

export default Toaster;
