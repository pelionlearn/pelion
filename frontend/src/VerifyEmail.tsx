import { useEffect, useState } from "react";
import { useAuth } from "./auth.tsx";

export default function VerifyEmail() {
    const [status, setStatus] = useState<string | null>(null);
    const { user, loading, refreshUser } = useAuth();
    const token = new URLSearchParams(window.location.search).get("token");

    useEffect(() => {
        if (!token) return;

        async function verify() {
            try {
                const response = await fetch("/api/auth/verify", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ token }),
                });

                if (!response.ok) {
                    setStatus("Verification failed.");
                    return;
                }

                setStatus(
                    "Your email has been verified!\nYou can close this page and log in to Pelion"
                );

                await refreshUser();
            } catch {
                setStatus("Something went wrong.");
            }
        }

        verify();
    }, [token]);

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center bg-background font-arvo text-text">
                Loading...
            </div>
        );
    }

    const message =
        status ??
        (token
            ? "Verifying your email..."
            : user && !user.is_verified
              ? "Please check your inbox and verify your email before logging in."
              : "Invalid verification link.");

    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <h1 className="text-text font-arvo text-xl md:text-xl p-20 text-center whitespace-pre-line">
                    {message}
                </h1>
            </div>
        </div>
    );
}
