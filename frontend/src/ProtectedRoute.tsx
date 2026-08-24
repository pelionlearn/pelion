import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "./auth.tsx";

function ProtectedRoute() {
    const { user, loading } = useAuth();

    if (loading) {
        return (
            <div className="flex h-screen items-center justify-center bg-background font-arvo text-text">
                Loading...
            </div>
        );
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (!user.is_verified) {
        return <Navigate to="/verify-email" replace />;
    }

    return <Outlet />;
}

export default ProtectedRoute;
