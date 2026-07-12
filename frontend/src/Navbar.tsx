import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav className="bg-background top-0 left-0 w-screen h-20 border-b border-dark">
            <ul className="flex flex-row items-center">
                <li>
                    <Link to="/" className="flex items-center">
                        <img src="/pelion_alt_nobg.svg" alt="Pelion" className="h-20 -mr-3" />
                        <h3 className="text-text font-arvo text-md md:text-xl">Pelion</h3>
                    </Link>
                </li>
                <li>
                    <Link to="/about">
                        <h3 className="pl-5 text-text font-arvo text-md md:text-xl">About</h3>
                    </Link>
                </li>
                <li>
                    <Link to="/contact">
                        <h3 className="pl-5 text-text font-arvo text-md md:text-xl">Contact</h3>
                    </Link>
                </li>
                <li className="ml-auto">
                    <Link to="/signin">
                        <h3 className="pl-5 text-text font-arvo text-md md:text-xl">Sign in</h3>
                    </Link>
                </li>
                <li>
                    <Link to="/signup">
                        <h3 className="pl-5 pr-5 text-text font-arvo text-md md:text-xl">
                            Register
                        </h3>
                    </Link>
                </li>
            </ul>
        </nav>
    );
}

export default Navbar;
