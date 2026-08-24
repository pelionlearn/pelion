import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, Navigate, RouterProvider } from "react-router-dom";

import "./index.css";
import Home from "./Home.tsx";
import About from "./About.tsx";
import Contact from "./Contact.tsx";
import Login from "./Login.tsx";
import Dashboard from "./dashboard/Dashboard.tsx";
import Classroom from "./dashboard/classroom/Classroom.tsx";
import Tutor from "./dashboard/classroom/Tutor.tsx";
import Notes from "./dashboard/classroom/Notes.tsx";
import Chat from "./dashboard/classroom/Chat.tsx";
import ClassroomPageNotFound from "./dashboard/classroom/ClassroomPageNotFound.tsx";
import NotFound from "./NotFound.tsx";
import Register from "./Register.tsx";
import { AuthProvider } from "./auth.tsx";
import { ToastProvider } from "./components/toast/toast.tsx";
import ProtectedRoute from "./ProtectedRoute.tsx";
import GuestRoute from "./GuestRoute.tsx";
import VerifyEmail from "./VerifyEmail.tsx";

const router = createBrowserRouter([
    {
        path: "/",
        element: <Home />,
    },
    {
        path: "/about",
        element: <About />,
    },
    {
        path: "/contact",
        element: <Contact />,
    },
    {
        element: <GuestRoute />,
        children: [
            {
                path: "/login",
                element: <Login />,
            },
            {
                path: "/register",
                element: <Register />,
            },
        ],
    },
    {
        element: <ProtectedRoute />,
        children: [
            {
                path: "/dashboard",
                element: <Dashboard />,
            },
            {
                path: "/dashboard/classroom/:classroomId",
                element: <Classroom />,
                children: [
                    {
                        index: true,
                        element: <Navigate to="tutor" replace />,
                    },
                    {
                        path: "tutor",
                        element: <Tutor />,
                    },
                    {
                        path: "notes",
                        element: <Notes />,
                    },
                    {
                        path: "chat/:chatId",
                        element: <Chat />,
                    },
                    {
                        path: "quizzes",
                        element: <ClassroomPageNotFound />,
                    },
                ],
            },
        ],
    },
    {
        path: "/verify-email",
        element: <VerifyEmail />,
    },
    {
        path: "*",
        element: <NotFound />,
    },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <ToastProvider>
            <AuthProvider>
                <RouterProvider router={router} />
            </AuthProvider>
        </ToastProvider>
    </React.StrictMode>
);
