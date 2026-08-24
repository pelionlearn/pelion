import {
    createContext,
    useCallback,
    useContext,
    useMemo,
    useRef,
    useState,
    type ReactNode,
} from "react";
import Toaster, { type Toast, type ToastType } from "./Toaster.tsx";

const DEFAULT_DURATION = 4000;
const MAX_TOASTS = 5;

interface ToastContextValue {
    success: (message: string, duration?: number) => void;
    error: (message: string, duration?: number) => void;
    info: (message: string, duration?: number) => void;
    dismiss: (id: number) => void;
}

const ToastContext = createContext<ToastContextValue | undefined>(undefined);

export function ToastProvider({ children }: { children: ReactNode }) {
    const [toasts, setToasts] = useState<Toast[]>([]);
    const nextId = useRef(0);

    const dismiss = useCallback((id: number) => {
        setToasts(prev => prev.filter(toast => toast.id !== id));
    }, []);

    const show = useCallback((type: ToastType, message: string, duration?: number) => {
        const id = ++nextId.current;
        setToasts(prev => [
            ...prev.slice(-(MAX_TOASTS - 1)),
            { id, type, message, duration: duration ?? DEFAULT_DURATION },
        ]);
    }, []);

    const value = useMemo(
        () => ({
            success: (message: string, duration?: number) => show("success", message, duration),
            error: (message: string, duration?: number) => show("error", message, duration),
            info: (message: string, duration?: number) => show("info", message, duration),
            dismiss,
        }),
        [show, dismiss]
    );

    return (
        <ToastContext.Provider value={value}>
            {children}
            <Toaster toasts={toasts} onDismiss={dismiss} />
        </ToastContext.Provider>
    );
}

export function useToast() {
    const ctx = useContext(ToastContext);
    if (!ctx) throw new Error("useToast must be used within ToastProvider");
    return ctx;
}
