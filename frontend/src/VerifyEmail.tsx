import { useEffect, useState } from "react";

export default function VerifyEmail() {
    const [status, setStatus] = useState("Verifying your email...");

    useEffect(() => {
        async function verify() {
            const params = new URLSearchParams(window.location.search);
            const token = params.get("token");

            if (!token) {
                setStatus("Invalid verification link.");
                return;
            }

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

                setStatus("Your email has been verified!\nYou can close this page.");
            } catch {
                setStatus("Something went wrong.");
            }
        }

        verify();
    }, []);

    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <h1 className="text-text font-arvo text-xl md:text-xl p-20 text-center whitespace-pre-line">
                    {status}
                </h1>
            </div>
        </div>
    );
}
