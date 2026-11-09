import Navbar from "./Navbar.tsx";

function Contact() {
    return (
        <div>
            <div className="fixed -z-10 bg-background top-0 left-0 w-screen h-screen flex flex-col items-center"></div>
            <div className="relative z-10">
                <Navbar />
                <h1 className="text-text font-arvo text-3xl md:text-5xl p-10 md:pt-25 md:pb-25 md:mr-25 md:ml-25 leading-tight text-center border-b ">
                    Let's get in <span className="text-primary">touch.</span>
                </h1>
                <div className="flex flex-col md:flex-row">
                    <p className="w-full md:w-2/3 text-text text-lg font-arvo p-8 md:pl-20 md:pt-25 leading-relaxed">
                        Have questions, feedback, or ideas on how we can make Pelion even better? We
                        would love to hear from you. Whether you're a student with feature requests,
                        an educator interested in bringing Pelion to your classroom, or an early
                        adopter wanting to share your experience, our team is always ready to
                        connect.
                    </p>
                    <p className="w-full md:w-1/3 text-text text-lg font-arvo p-8 pt-0 md:pr-20 md:pt-25 leading-relaxed">
                        Email Us Directly:{" "}
                        <a
                            href="mailto:contact@pelionlearn.com"
                            className="underline text-primary hover:text-secondary"
                        >
                            contact@pelionlearn.com
                        </a>
                        <br />
                        Visit Our Platform:{" "}
                        <a
                            href="www.pelionlearn.com"
                            className="underline text-primary hover:text-secondary"
                        >
                            www.pelionlearn.com
                        </a>
                        <br />
                        <br />
                        <i>We respond to all early-access inquiries within 2-3 Business Days.</i>
                    </p>
                </div>
            </div>
        </div>
    );
}

export default Contact;
