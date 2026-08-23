import { useState, type ChangeEvent } from "react";
import Navbar from "./Navbar.tsx";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "./auth.tsx";

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const { setUser } = useAuth();
    const navigate = useNavigate();

    async function handleLogin(e: ChangeEvent<HTMLFormElement>) {
        e.preventDefault();

        try {
            const body = new URLSearchParams();
            body.append("username", username);
            body.append("password", password);

            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body,
            });

            if (response.ok) {
                console.log("Logged in");
                const meResponse = await fetch("/api/users/me");
                const userData = await meResponse.json();
                setUser(userData);
                navigate("/dashboard");
            }

            if (response.status == 400) {
                console.log("Invalid credentials");
            }
        } catch (err) {
            console.log("ummm");
        }
    }

    async function handleLoginWithGoogle() {
        const response = await fetch("/api/auth/google/authorize");

        const data = await response.json();

        const authUrl = new URL(data.authorization_url, window.location.origin);

        window.location.href = authUrl.toString();
    }

    return (
        <div className="top-0 left-0 min-w-screen min-h-screen">
            <div className="relative z-10">
                <Navbar />
            </div>

            <div className="flex items-center justify-center px-6 mt-20">
                <div className="w-full max-w-md p-6 bg-background border border-dark rounded-2xl text-text">
                    <h2 className="text-2xl font-bold my-6 text-center">Log into Pelion</h2>
                    <form onSubmit={handleLogin} className="mb-4">
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
                                    onChange={e => setPassword(e.target.value)}
                                    required
                                />
                            </div>
                        </div>
                        <div className="flex justify-center mt-2">
                            <button
                                type="submit"
                                className="w-full py-3 bg-primary text-dark rounded-2xl cursor-pointer hover:-translate-y-0.5 transition-all duration-200"
                            >
                                Login
                            </button>
                        </div>
                    </form>

                    <div className="flex justify-center mt-4 gap-4 mb-4">
                        <button
                            type="submit"
                            className="w-full py-3 bg-background text-text rounded-2xl outline outline-dark cursor-pointer hover:-translate-y-0.5 transition-all duration-200"
                        >
                            Forgot Password
                        </button>
                        <Link
                            to="/register"
                            className="w-full text-center py-3 bg-background text-text rounded-2xl outline outline-dark cursor-pointer hover:-translate-y-0.5 transition-all duration-200"
                        >
                            Register
                        </Link>
                    </div>

                    <hr className="border-dark" />

                    <div className="flex justify-center mt-4 gap-4">
                        <button
                            type="submit"
                            onClick={handleLoginWithGoogle}
                            className="w-full py-3 bg-background text-text rounded-2xl outline outline-dark cursor-pointer hover:-translate-y-0.5 transition-all duration-200"
                        >
                            <i className="fa-brands fa-google mr-2" />
                            Google
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
