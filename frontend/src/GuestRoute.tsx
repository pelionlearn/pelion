import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./auth.tsx";

function GuestRoute() {
    const { user, loading } = useAuth();

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center bg-background font-arvo text-text">
                Loading...
            </div>
        );
    }

    if (user?.is_verified) {
        return <Navigate to="/dashboard" replace />;
    }

    return <Outlet />;
}

export default GuestRoute;
