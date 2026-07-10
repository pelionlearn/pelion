import { useState } from "react";
import heroImg from "./assets/icon.png";
import "./App.css";
import { motion } from "motion/react";
import confetti from "canvas-confetti";

function App() {
  const [email, setEmail] = useState("");
  const [signedUp, setSignedUp] = useState(false);
  const [contactOpen, setContactOpen] = useState(false);

  const [contactForm, setContactForm] = useState({
    firstName: "",
    lastName: "",
    email: "",
    message: "",
  });

  const handleContactSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // TODO: send message to backend
  };

  const handleNotify = () => {
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

    // TODO: send email to backend
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
        width="200"
        height="200"
      />

      <h1>Coming Soon</h1>

      <div className="subtitle">
        <h3>A learning platform for students, by students.<br/>Get notified when we launch.</h3>
      </div>

      {!signedUp ? (
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
            className="notify rounded-xl button-primary px-5 py-2"
          >
            Notify Me
          </button>
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
          className="contact-btn"
          onClick={() => setContactOpen(true)}
        >
          Contact Us
        </button>
      </div>

      {contactOpen && (
        <div className="contact-bg">

          <div className="contact-popup">
            <button
              type="button"
              className="close-popup"
              onClick={() => setContactOpen(false)}
            >
              ×
            </button>

            <h2>Contact Us</h2>

            <form onSubmit={handleContactSubmit}>
              <div className="name-row">
                <input
                  type="text"
                  placeholder="First name"
                  className="email-input"
                  value={contactForm.firstName}
                  onChange={(e) =>
                    setContactForm({ ...contactForm, firstName: e.target.value })
                  }
                  required
                />

                <input
                  type="text"
                  placeholder="Last name"
                  className="email-input"
                  value={contactForm.lastName}
                  onChange={(e) =>
                    setContactForm({ ...contactForm, lastName: e.target.value })
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
                  setContactForm({ ...contactForm, email: e.target.value })
                }
                required
              />

              <textarea
                placeholder="Enter your message"
                className="email-input"
                rows={5}
                value={contactForm.message}
                onChange={(e) =>
                  setContactForm({ ...contactForm, message: e.target.value })
                }
                required
              />

              <button
                type="submit"
                className="notify rounded-xl button-primary px-5 py-2"
              >
                Send Message
              </button>
            </form>
          </div>
          
        </div>
      )}
    </motion.div>
  );
}

export default App;