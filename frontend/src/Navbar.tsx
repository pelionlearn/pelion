import { useState } from "react";
import { Link } from "react-router-dom";
import { LiaTimesSolid, LiaBarsSolid } from "react-icons/lia";

function Navbar() {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    return (
        <nav className="bg-background sticky top-0 left-0 w-screen h-20 border-b border-dark">
            {/* min-[450px]: */}
            <ul className="hidden min-[600px]:flex flex-row items-center">
                <li>
                    <Link to="/" className="flex items-center">
                        <img src="/pelion_alt_nobg.svg" alt="Pelion" className="h-20 -mr-3" />
                        <h3 className="text-text font-arvo text-xl md:text-xl">Pelion</h3>
                    </Link>
                </li>
                <li>
                    <Link to="/about">
                        <h3 className="pl-5 text-text font-arvo text-xl md:text-xl">About</h3>
                    </Link>
                </li>
                <li>
                    <Link to="/contact">
                        <h3 className="pl-5 text-text font-arvo text-xl md:text-xl">Contact</h3>
                    </Link>
                </li>
                <li className="ml-auto">
                    <Link to="/signin">
                        <h3 className="pl-5 text-text font-arvo text-xl md:text-xl">Sign in</h3>
                    </Link>
                </li>
                <li>
                    <Link to="/signup">
                        <h3 className="pl-5 pr-5 text-text font-arvo text-xl md:text-xl">
                            Register
                        </h3>
                    </Link>
                </li>
            </ul>
            <ul className="min-[600px]:hidden flex flex-row items-center">
                <li>
                    <Link to="/" className="flex items-center">
                        <img src="/pelion_alt_nobg.svg" alt="Pelion" className="h-20 -mr-3" />
                        <h3 className="text-text font-arvo text-xl md:text-xl">Pelion</h3>
                    </Link>
                </li>
                <li className="ml-auto">
                    <button onClick={toggleMenu} className="focus:outline-none pr-5">
                        <div className="text-text inline">
                            {isOpen ? (
                                <LiaTimesSolid size={24} className="inline" />
                            ) : (
                                <LiaBarsSolid size={24} className="inline" />
                            )}
                        </div>
                    </button>
                </li>
            </ul>
            {isOpen && (
                <ul className="z-100 ml-auto w-min bg-background min-[600px]:hidden flex flex-col gap-2 border-b border-l border-dark">
                    <li>
                        <Link to="/about">
                            <h3 className="pl-5 pt-5 text-text font-arvo text-xl">About</h3>
                        </Link>
                    </li>
                    <li>
                        <Link to="/contact">
                            <h3 className="pl-5 text-text font-arvo text-xl">Contact</h3>
                        </Link>
                    </li>
                    <li>
                        <Link to="/signin">
                            <h3 className="pl-5 text-text font-arvo text-xl">Sign in</h3>
                        </Link>
                    </li>
                    <li>
                        <Link to="/signup">
                            <h3 className="pl-5 pr-5 pb-5 text-text font-arvo text-xl">Register</h3>
                        </Link>
                    </li>
                </ul>
            )}
        </nav>
    );
}

export default Navbar;
