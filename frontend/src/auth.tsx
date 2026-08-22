import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

interface User {
    id: string;
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    is_verified: boolean;
    name: string;
}

interface AuthContextValue {
    user: User | null;
    loading: boolean;
    setUser: (user: User | null) => void;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch("/api/users/me")
            .then(res => (res.ok ? res.json() : null))
            .then(data => setUser(data))
            .finally(() => setLoading(false));
    }, []);

    async function logout() {
        await fetch("/api/auth/logout", { method: "POST" });
        setUser(null);
    }

    return (
        <AuthContext.Provider value={{ user, loading, setUser, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const ctx = useContext(AuthContext);
    if (!ctx) throw new Error("useAuth must be used within AuthProvider");
    return ctx;
}