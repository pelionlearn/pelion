import { useState } from "react";
import heroImg from "./assets/pelion_banner_left_alt_nobg.svg";
import "./App.css";
import { motion } from "motion/react";
import confetti from "canvas-confetti";

function App() {
  const [email, setEmail] = useState("");
  const [signedUp, setSignedUp] = useState(false);
  const [contactOpen, setContactOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [contactSent, setContactSent] = useState(false);
  const [contactLoading, setContactLoading] = useState(false);

  const [contactForm, setContactForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    message: "",
  });

  const handleContactSubmit = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    setContactLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/contact", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          first_name: contactForm.firstName,
          last_name: contactForm.lastName,
          email: contactForm.email,
          message: contactForm.message,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to send message");
      }

      setContactSent(true);

      setContactForm({
        firstName: "",
        lastName: "",
        email: "",
        message: "",
      });

    } catch (err) {
      console.error(err);
    } finally {
      setContactLoading(false);
    }
  };

  const handleNotify = async () => {
    if (!email.trim()) return;

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/waitlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to join waitlist");
      }

      const colors = ["#5be09a", "#ffffff"];

      confetti({
        particleCount: 75,
        angle: 60,
        spread: 55,
        origin: { x: 0, y: 0.6 },
        colors,
      });

      confetti({
        particleCount: 75,
        angle: 120,
        spread: 55,
        origin: { x: 1, y: 0.6 },
        colors,
      });

      setSignedUp(true);
    } catch (err) {
      console.error(err);
      alert("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="hero"
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 1 }}
    >
      <img
        src={heroImg}
        alt="Hero Image"
        className="hero-image"
        width="400"
        height="400"
      />
      <div className="subtitle">
          <h3>A learning platform for students, &nbsp;by students.<br/></h3>
      </div>

      <div className="">
        <h1>Get notified when we launch.</h1>
      </div>
      
      
      {!signedUp ? (
        <div>
          <div className="email-notification">
            <input
              type="email"
              placeholder="Enter your email"
              className="email-input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <button
              onClick={handleNotify}
              disabled={loading}
              className="notify rounded-xl button-primary px-5 py-2"
            >
              {loading ? "Signing up..." : "Notify Me"}
            </button>
          </div>
        </div>
        
      ) : (
        <motion.div
          className="signup-success"
          initial={{ opacity: 0, scale: 0.9, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          transition={{ duration: 0.1 }}
        >
          <h2>You're all signed up!</h2>
          <p>
            We'll let you know as soon as Pelion is
            ready.
          </p>
        </motion.div>
      )}
      
      <div>
        <button
          className="button-secondary button-shape contact-button"
          onClick={() => setContactOpen(true)}
        >
          Contact Us
        </button>
      </div>

      {contactOpen && (
        <motion.div className="contact-bg" animate={{ opacity: 1 }} initial={{ opacity: 0 }}>

          <motion.div
            className="contact-popup"
            animate={{ scale: 1 }}
            initial={{ scale: 0.8 }}
            transition={{ duration: 0.1 }}
          >
            <button
              type="button"
              className="close-popup"
              onClick={() => {
                setContactOpen(false);
                setContactSent(false);
              }}
            >
              ×
            </button>

            {!contactSent ? (
              <>
                <h2>Contact Us</h2>

                <form onSubmit={handleContactSubmit}>
                  <div className="name-row">
                    <input
                      type="text"
                      placeholder="First name"
                      className="email-input"
                      value={contactForm.firstName}
                      onChange={(e) =>
                        setContactForm({
                          ...contactForm,
                          firstName: e.target.value,
                        })
                      }
                      required
                    />

                    <input
                      type="text"
                      placeholder="Last name"
                      className="email-input"
                      value={contactForm.lastName}
                      onChange={(e) =>
                        setContactForm({
                          ...contactForm,
                          lastName: e.target.value,
                        })
                      }
                      required
                    />
                  </div>

                  <input
                    type="email"
                    placeholder="Email address"
                    className="email-input"
                    value={contactForm.email}
                    onChange={(e) =>
                      setContactForm({
                        ...contactForm,
                        email: e.target.value,
                      })
                    }
                    required
                  />

                  <textarea
                    placeholder="Enter your message"
                    className="email-input"
                    rows={5}
                    value={contactForm.message}
                    onChange={(e) =>
                      setContactForm({
                        ...contactForm,
                        message: e.target.value,
                      })
                    }
                    required
                  />

                  <button
                    type="submit"
                    disabled={contactLoading}
                    className="button-shape rounded-xl button-primary px-5 py-2"
                  >
                    {contactLoading ? "Sending..." : "Send Message"}
                  </button>
                </form>
              </>
            ) : (
              <motion.div
                className="contact-success"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.2 }}
              >
                <h2>Message Sent!</h2>
                <p>
                  Thanks for reaching out. We'll get back to you soon.
                </p>
              </motion.div>
            )}
          </motion.div>
          
        </motion.div>
      )}
    </motion.div>
  );
}

export default App;