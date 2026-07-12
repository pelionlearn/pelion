import Navbar from "./Navbar.tsx";

function About() {
    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <Navbar />
                <h1 className="text-text font-arvo text-3xl md:text-5xl p-10 md:pt-25 md:pb-25 md:mr-25 md:ml-25 leading-tight text-center border-b ">
                    Meet the team <span className="text-primary">:)</span>
                </h1>
                <div className="flex flex-col md:flex-row">
                    <p className="text-text text-md font-arvo p-8 md:pl-20 md:pt-25 leading-relaxed">
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed massa felis,
                        molestie elementum accumsan vitae, mollis sed dolor. Nunc ultrices vulputate
                        ullamcorper. Proin a magna et nulla bibendum aliquam ac vel eros. Quisque
                        velit lacus, congue a placerat non, rhoncus ut diam. Nullam rutrum dictum
                        est. Nulla ornare sapien quis venenatis iaculis. Orci varius natoque
                        penatibus et magnis dis parturient montes, nascetur ridiculus mus. In hac
                        habitasse platea dictumst. Fusce mollis quam id nulla fermentum, sed semper
                        nisl iaculis. Fusce sollicitudin mauris sed gravida volutpat.
                    </p>
                    <p className="text-text text-md font-arvo p-8 pt-0 md:pr-20 md:pt-25 leading-relaxed">
                        Suspendisse consectetur laoreet interdum. Vivamus augue quam, congue nec
                        nulla sed, interdum rutrum lorem. Integer tempor a turpis id rutrum. Vivamus
                        pharetra eros ut est euismod, eget euismod odio feugiat. Fusce a massa
                        turpis. Nam aliquet at metus in congue. Aliquam egestas scelerisque
                        consectetur. Duis id eros posuere, aliquam tellus sed, sodales neque. Donec
                        commodo nibh ut sapien congue ullamcorper. Quisque interdum euismod diam,
                        quis eleifend mauris molestie id. Ut at lacus vitae purus pretium dictum in
                        eu quam.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default About;
