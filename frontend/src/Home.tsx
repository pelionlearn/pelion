import Navbar from "./Navbar.tsx";

function Home() {
    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <Navbar />
                <h1 className="text-text font-arvo text-3xl md:text-5xl p-10 md:pt-25 md:pb-25 md:mr-25 md:ml-25 leading-tight text-center border-b ">
                    The learning platform <span className="text-primary">for</span> students,{" "}
                    <span className="text-primary">by</span> students.
                </h1>
                <div className="flex flex-col md:flex-row">
                    <p className="text-text text-md font-arvo p-8 md:pl-20 md:pt-25 leading-relaxed">
                        Pelion is an AI-powered learning platform designed to bridge the gap between
                        simply consuming digital content and truly mastering it. In today's digital
                        landscape, high-quality educational videos are everywhere, but converting
                        that incoming stream of information into lasting comprehension remains a
                        major challenge. We solve this by combining structured AI notetaking,
                        interactive study groups, and seamless video integration into a single,
                        cohesive ecosystem—making learning more active, connected, and genuinely
                        effective for every student.
                    </p>
                    <p className="text-text text-md font-arvo p-8 pt-0 md:pr-20 md:pt-25 leading-relaxed">
                        Whether you are a high school student tackling advanced coursework, a
                        college student balancing heavy lectures, an educator seeking to engage your
                        classroom, or simply a lifelong learner pursuing a new passion, Pelion is
                        built specifically for you. By pairing peer-to-peer community spaces with
                        intelligent AI tutoring, Pelion makes productive self-improvement feel
                        engaging rather than burdensome. We believe that learning should be fun,
                        intuitive, and designed to help you succeed on your own terms.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Home;
