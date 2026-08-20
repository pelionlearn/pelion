import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

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
        path: "/login",
        element: <Login />,
    },
    {
        path: "/dashboard",
        element: <Dashboard />,
    },
    {
        path: "*",
        element: <NotFound />,
    },
    {
        path: "/dashboard/classroom/:classroomId",
        element: <Classroom />,
        children: [
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
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);
