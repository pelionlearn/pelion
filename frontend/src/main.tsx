import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import "./index.css";
import Home from "./Home.tsx";
import About from "./About.tsx";
import Contact from "./Contact.tsx";
import NotFound from "./NotFound.tsx";
import Login from "./Login.tsx";
import Dashboard from "./Dashboard.tsx";
import Classroom from "./Classroom.tsx";

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
        element: <Login />
    },
    {
        path: "/dashboard",
        element: <Dashboard />
    },
    {
        path: "*",
        element: <NotFound />,
    },
    {
        path: "/dashboard/classroom",
        element: <Classroom />,
    },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
    <React.StrictMode>
        <RouterProvider router={router} />
    </React.StrictMode>
);
