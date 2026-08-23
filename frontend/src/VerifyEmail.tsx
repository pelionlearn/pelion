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

                setStatus("Your email has been verified!");
            } catch {
                setStatus("Something went wrong.");
            }
        }

        verify();
    }, []);

    return <div>{status}</div>;
}
