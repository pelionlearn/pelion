import Navbar from "./Navbar.tsx";

function About() {
    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <Navbar />
                <h1 className="text-text font-arvo text-3xl md:text-5xl p-10 md:pt-15 md:pb-15 md:mr-25 md:ml-25 leading-tight text-center border-b ">
                    Meet the <span className="text-primary">team :)</span>
                </h1>
                <div className="flex flex-col xl:flex-row px-4 md:px-12">
                    <p className="text-text text-md font-arvo p-4 md:pt-15 leading-relaxed flex-1">
                        <b className="text-primary">Carson Fonner</b>
                        <br />
                        <i className="text-text-secondary">Marketing Lead</i>
                        <br />
                        <br />
                        Carson leads marketing and outreach at Pelion. He is currently pursuing a
                        business degree at Texas A&M University, where he focuses his studies on
                        strategic growth, brand management, and audience expansion.
                    </p>
                    <p className="text-text text-md font-arvo p-4 md:pt-15 leading-relaxed flex-1">
                        <b className="text-primary">Elijah Morales</b>
                        <br />
                        <i className="text-text-secondary">Sales Lead</i>
                        <br />
                        <br />
                        Elijah helps with collaborative aspects, working to cultivate better team
                        environment and work towards customer outreach.
                    </p>
                    <p className="text-text text-md font-arvo p-4 md:pt-15 leading-relaxed flex-1">
                        <b className="text-primary">Teo Lazzari</b>
                        <br />
                        <i className="text-text-secondary">Lead Developer</i>
                        <br />
                        <br />
                        Teo leads the technical architecture at Pelion, managing core platform
                        development, system infrastructure, and AI feature deployment.
                    </p>
                    <p className="text-text text-md font-arvo p-4 md:pt-15 leading-relaxed flex-1">
                        <b className="text-primary">Matthew Sequeira </b>
                        <br />
                        <i className="text-text-secondary">Backend Developer</i>
                        <br />
                        <br />
                        Matt develops core system tools and video integrations, drawing on his
                        technical background in custom Minecraft mod development to build
                        user-focused features.
                    </p>
                    <p className="text-text text-md font-arvo p-4 md:pt-15 leading-relaxed flex-1">
                        <b className="text-primary">Jeremy Sequeira</b>
                        <br />
                        <i className="text-text-secondary">Frontend Developer</i>
                        <br />
                        <br />
                        Jeremy works on software execution and interactive feature engineering,
                        bringing extensive development experience that includes creating popular
                        Minecraft mods with millions of downloads on CurseForge.
                    </p>
                    <p className="text-text text-md font-arvo p-4 md:pt-15 leading-relaxed flex-1">
                        <b className="text-primary">Matthew Labastida</b>
                        <br />
                        <i className="text-text-secondary">Intern</i>
                        <br />
                        <br />
                        Matthew assists the engineering team with feature development, testing, and
                        system optimization, gaining hands-on experience building core platform
                        tools.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default About;
