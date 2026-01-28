import React from "react";
import "./footerbar.css";

export default function FooterBar() {
    return (
        <footer className="bottombar">
            <div className="techChips">
                <span className="tech">TensorFlow</span>
                <span className="tech">React</span>
                <span className="tech">Numpy</span>
                <span className="tech">Python</span>
                <span className="tech">FastAPI</span>
                <span className="tech">MediaPip</span>
            </div>

            <div className="links">
                <a
                    className="iconBtn"
                    href="https://github.com/alishlaibah"
                    target="_blank"
                    rel="noreferrer"
                    aria-label="GitHub"
                    title="GitHub"
                >
                    <svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
                        <path d="M12 .5C5.73.5.75 5.7.75 12.2c0 5.2 3.44 9.6 8.2 11.16.6.12.82-.27.82-.6v-2.2c-3.34.75-4.04-1.67-4.04-1.67-.54-1.44-1.33-1.82-1.33-1.82-1.1-.78.08-.76.08-.76 1.2.09 1.84 1.3 1.84 1.3 1.08 1.92 2.84 1.36 3.54 1.04.11-.8.42-1.36.76-1.67-2.67-.32-5.48-1.38-5.48-6.15 0-1.36.46-2.47 1.22-3.34-.12-.32-.54-1.62.12-3.38 0 0 1-.33 3.3 1.28a11 11 0 0 1 6 0c2.3-1.61 3.3-1.28 3.3-1.28.66 1.76.24 3.06.12 3.38.76.87 1.22 1.98 1.22 3.34 0 4.78-2.82 5.82-5.5 6.14.44.4.83 1.17.83 2.36v3.5c0 .33.22.72.83.6 4.76-1.56 8.2-5.96 8.2-11.16C23.25 5.7 18.27.5 12 .5z" />
                    </svg>
                </a>

                <a
                    className="iconBtn"
                    href="https://www.linkedin.com/in/alishlaibah/"
                    target="_blank"
                    rel="noreferrer"
                    aria-label="LinkedIn"
                    title="LinkedIn"
                >
                    <svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">
                        <path d="M20.45 20.45h-3.55v-5.6c0-1.34-.03-3.06-1.87-3.06-1.87 0-2.16 1.46-2.16 2.97v5.7H9.32V9h3.4v1.56h.05c.47-.9 1.63-1.85 3.36-1.85 3.6 0 4.26 2.37 4.26 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM3.56 20.45h3.55V9H3.56v11.45z" />
                    </svg>
                </a>
            </div>
        </footer>
    );
}
