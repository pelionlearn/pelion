import { useState, type ChangeEvent } from "react";
import Navbar from "./Navbar.tsx";
import { useAuth } from "./auth.tsx";
import { useNavigate } from "react-router-dom";

function Login() {
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const { setUser } = useAuth();
    const navigate = useNavigate();

    async function handleRegister(e: ChangeEvent<HTMLFormElement>) {
        e.preventDefault();

        try {
            const response = await fetch("/api/auth/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    email: email,
                    name: username,
                    password: password,
                }),
            });

            if (response.ok) {
                console.log("Registered");
                handleLogin();
            }

            if (response.status == 400) {
                console.log("Invalid credentials");
            }
        } catch (err) {
            console.log("ummm");
        }
    }

    async function handleLogin() {
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

    async function handleRegisterWithGoogle() {
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
                                Register
                            </button>
                        </div>
                    </form>

                    <hr className="border-dark" />

                    <div className="flex justify-center mt-4 gap-4">
                        <button
                            type="submit"
                            onClick={handleRegisterWithGoogle}
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
