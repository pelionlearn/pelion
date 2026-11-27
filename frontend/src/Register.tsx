
import { useState, type FormEvent } from "react";
import { useMutation } from "@tanstack/react-query";
import Navbar from "./Navbar.tsx";
import { useToast } from "./components/toast/toast.tsx";
import { useNavigate } from "react-router-dom";

async function registerUser(email: string, username: string, password: string) {
    const response = await fetch("/api/auth/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email,
            name: username,
            password,
        }),
    });

    if (response.status === 400) {
        throw new Error("User already exists with this email");
    }

    if (!response.ok) {
        throw new Error("Registration failed");
    }

    const verifyResponse = await fetch("/api/auth/request-verify-token", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
    });

    if (!verifyResponse.ok) {
        throw new Error("Account created, but verification email could not be sent");
    }
}

async function registerWithGoogle() {
    const response = await fetch("/api/auth/google/authorize");

    if (!response.ok) {
        throw new Error("Failed to initialize Google authentication");
    }

    const data = await response.json();

    return new URL(data.authorization_url, window.location.origin).toString();
}

function Login() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const toast = useToast();
    const navigate = useNavigate();

    const registerMutation = useMutation({
        mutationFn: () => registerUser(email, username, password),

        onSuccess: () => {
            toast.info("Verification Email Sent: please check your email");
            navigate("/login");
        },

        onError: (error) => {
            toast.error(error.message);
            console.error(error);
        },
    });

    const googleMutation = useMutation({
        mutationFn: registerWithGoogle,

        onSuccess: (authUrl) => {
            window.location.href = authUrl;
        },

        onError: (error) => {
            toast.error(error.message);
            console.error(error);
        },
    });

    function handleRegister(e: FormEvent<HTMLFormElement>) {
        e.preventDefault();
        registerMutation.mutate();
    }

    return (
        <div className="top-0 left-0 min-w-screen min-h-screen">
            <div className="relative z-10">
                <Navbar />
            </div>

            <div className="flex items-center justify-center px-6 mt-20">
                <div className="w-full max-w-md p-6 bg-background border border-dark rounded-2xl text-text">
                    <h2 className="text-2xl font-bold my-6 text-center">Create an Account</h2>
                    <form onSubmit={handleRegister} className="mb-4">
                        <div className="py-2">
                            <div className="relative">
                                <i
                                    className="fa-regular fa-envelope absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary"
                                    aria-hidden="true"
                                />
                                <input
                                    type="email"
                                    placeholder="Email"
                                    className="pl-10 px-3 py-2 w-full outline outline-dark rounded-lg"
                                    value={email}
                                    onChange={e => setEmail(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="py-2">
                            <div className="relative">
                                <i
                                    className="fa-solid fa-user absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary"
                                    aria-hidden="true"
                                />
                                <input
                                    type="username"
                                    placeholder="Username"
                                    className="pl-10 px-3 py-2 w-full outline outline-dark rounded-lg"
                                    value={username}
                                    onChange={e => setUsername(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="py-2">
                            <div className="relative">
                                <i
                                    className="fa-solid fa-key absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary"
                                    aria-hidden="true"
                                />
                                <input
                                    type="password"
                                    placeholder="Password"
                                    className="pl-10 px-3 py-2 w-full outline outline-dark rounded-lg"
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="flex justify-center mt-2">
                            <button
                                type="submit"
                                disabled={registerMutation.isPending}
                                className="w-full py-3 bg-primary text-dark rounded-2xl cursor-pointer hover:-translate-y-0.5 transition-all duration-200"
                            >
                                {registerMutation.isPending ? "Registering..." : "Register"}
                            </button>
                        </div>
                    </form>

                    <hr className="border-dark" />

                    <div className="flex justify-center mt-4 gap-4">
                        <button
                            type="button"
                            onClick={() => googleMutation.mutate()}
                            disabled={googleMutation.isPending}
                            className="w-full py-3 bg-background text-text rounded-2xl outline outline-dark cursor-pointer hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50"
                        >
                            <i className="fa-brands fa-google mr-2" />
                            {googleMutation.isPending ? "Redirecting..." : "Google"}
                        </button>
                    </div>

                    {/* <div className="flex justify-center mt-4 gap-4">
                        <button
                            type="submit"
                            className="w-full py-3 bg-background text-text rounded-2xl outline outline-dark cursor-pointer hover:-translate-y-0.5 transition-all duration-200"
                        >
                            <i className="fa-brands fa-apple mr-2" />
                            Apple
                        </button>
                    </div> */}
                </div>
            </div>
        </div>
    );
}

export default Login;
