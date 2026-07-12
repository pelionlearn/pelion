import { useRouteError } from "react-router-dom";

import Navbar from "./Navbar.tsx";

function NotFound() {
    const error = useRouteError();
    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <Navbar />
                <h1 className="text-text font-arvo text-xl md:text-xl p-20 text-center">
                    not found :(
                </h1>
            </div>
        </div>
    );
}

export default NotFound;
