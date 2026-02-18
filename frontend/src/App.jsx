import React, { useState } from "react";
import WebcamFeed from "./components/webcamfeed";
import AlphabetReference from "./components/AlphabetReference";
import HeaderBar from "./components/HeaderBar";
import FooterBar from "./components/FooterBar";
import "./App.css";

class DemoBoundary extends React.Component {
  state = { hasError: false };
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  render() {
    if (this.state.hasError) {
      return (
        <div className="demo-error-fallback">
          <p>The webcam demo couldn't load. Check the browser console for details.</p>
          <button className="btn btn-secondary" onClick={() => this.setState({ hasError: false })}>
            Retry
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

const PIPELINE_STEPS = [
  {
    num: "1",
    title: "Track hand",
    desc: "MediaPipe Hands extracts 21 3D landmarks from each webcam frame in real time.",
  },
  {
    num: "2",
    title: "Normalize in-browser",
    desc: "Landmarks are normalized and structured client-side. No raw video leaves the browser.",
  },
  {
    num: "3",
    title: "Buffer sequence",
    desc: "A sliding 30-frame window captures motion over time, enabling recognition of motion-dependent letters.",
  },
  {
    num: "4",
    title: "Classify",
    desc: "The sequence is sent to a trained classifier. It returns the predicted letter and confidence score.",
  },
];

const STACK = [
  {
    label: "ML Pipeline",
    items: ["TensorFlow / Keras", "MediaPipe Hands", "NumPy", "scikit-learn", "OpenCV"],
  },
  {
    label: "Backend",
    items: ["FastAPI", "Uvicorn", "Pydantic", "Render"],
  },
  {
    label: "Frontend",
    items: ["React 19", "Vite", "Cloudflare Pages"],
  },
];

const STACK_LINKS = {
  "TensorFlow / Keras": "https://www.tensorflow.org/",
  "MediaPipe Hands": "https://developers.google.com/mediapipe",
  "NumPy": "https://numpy.org/doc/",
  "scikit-learn": "https://scikit-learn.org/stable/",
  "OpenCV": "https://docs.opencv.org/",
  "FastAPI": "https://fastapi.tiangolo.com/",
  "Uvicorn": "https://www.uvicorn.org/",
  "Pydantic": "https://docs.pydantic.dev/",
  "Render": "https://render.com/docs",
  "React 19": "https://react.dev/",
  "Vite": "https://vitejs.dev/guide/",
  "Cloudflare Pages": "https://developers.cloudflare.com/pages/",
};

function App() {
  const [showLandmarks, setShowLandmarks] = useState(false);

  return (
    <div className="app-shell">
      <HeaderBar />

      <main>
        <section id="demo" className="hero">
          <div className="container hero-grid">
            <div className="hero-demo animate-in">
              <div className="card demo-card">
                <div className="demo-card-header">
                  <div>
                    <h2 className="demo-card-title">Live Demo</h2>
                    <p className="demo-card-hint">
                      Keep your hand <strong>close</strong>, centered, and well-lit.
                    </p>
                  </div>

                  <div className="demo-controls">
                    <label className="toggle">
                      <input
                        type="checkbox"
                        checked={showLandmarks}
                        onChange={() => setShowLandmarks((v) => !v)}
                      />
                      <span className="toggle-track" />
                      <span className="toggle-label">Landmarks</span>
                    </label>

                    <span className="pill">
                      Model:&nbsp;
                      <strong>asl_sequence_classifier</strong>
                    </span>
                  </div>
                </div>

                <DemoBoundary>
                  <WebcamFeed showLandmarks={showLandmarks} />
                </DemoBoundary>

                <p className="privacy-note">
                  Runs locally in your browser. No video is uploaded.
                </p>
                <p className="coldstart-note">
                  First prediction may take 30 to 60 seconds while the Render backend wakes up.
                </p>
              </div>
            </div>

            <div className="hero-copy animate-in animate-in-delay-1">
              <h1 className="hero-title">
                ASL Letter Recognition
                <span className="hero-title-dim">Real time, in your browser.</span>
              </h1>
              <p className="hero-subtitle">
                A webcam-based pipeline that tracks hand landmarks, buffers motion sequences, and classifies ASL letters using a model I trained on my own labeled dataset.
              </p>
              <p className="hero-detail">
                Built with MediaPipe Hands for 21-point landmark extraction, a TensorFlow sequence classifier, and a FastAPI backend, all deployed for real-time inference.
              </p>

              <div id="reference" className="ref-panel card">
                <h3 className="ref-panel-title">ASL Reference</h3>
                <AlphabetReference />
              </div>
            </div>
          </div>
        </section>

        <section id="highlights" className="section">
          <div className="container">
            <h2 className="section-title animate-in">How It Works</h2>
            <p className="section-subtitle animate-in animate-in-delay-1">
              The core inference loop, from webcam frame to predicted letter.
            </p>
            <div className="pipeline-steps">
              {PIPELINE_STEPS.map((step) => (
                <div key={step.num} className="pipeline-step animate-in animate-in-delay-2">
                  <span className="pipeline-num">{step.num}</span>
                  <div>
                    <h3 className="pipeline-step-title">{step.title}</h3>
                    <p className="pipeline-step-desc">{step.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <h2 className="section-title animate-in">Building the System</h2>
            <p className="section-subtitle animate-in animate-in-delay-1">
              From data collection to production deployment.
            </p>
            <div className="build-grid">
              <div className="build-block animate-in animate-in-delay-2">
                <h3 className="build-block-title">Data Collection</h3>
                <p className="build-block-text">
                  I wrote a webcam-based data collection script to record and label my own training set. Collected roughly 200 to 300 samples per letter. For letters that depend on motion (like J and Z), I captured short frame sequences instead of single snapshots.
                </p>
              </div>
              <div className="build-block animate-in animate-in-delay-2">
                <h3 className="build-block-title">Training</h3>
                <p className="build-block-text">
                  Trained and evaluated models in TensorFlow/Keras on the landmark sequences. Used NumPy and scikit-learn for preprocessing, normalization, and iteration. The sequence-based architecture makes classification motion-aware.
                </p>
              </div>
              <div className="build-block animate-in animate-in-delay-3">
                <h3 className="build-block-title">Deployment</h3>
                <p className="build-block-text">
                  Packaged the final model behind a production-style FastAPI API (Uvicorn &amp; Pydantic). The backend is deployed on Render with the frontend hosted on Cloudflare Pages.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className="section">
          <div className="container">
            <h2 className="section-title animate-in">Tech Stack</h2>
            <div className="stack-row">
              {STACK.map((group) => (
                <div key={group.label} className="stack-group">
                  <h3 className="stack-label">{group.label}</h3>
                  <div className="pill-grid">
                    {group.items.map((t) => (
                      <a
                        key={t}
                        className="pill"
                        href={STACK_LINKS[t] ?? "#"}
                        target="_blank"
                        rel="noreferrer noopener"
                        aria-label={`Open ${t} documentation`}
                      >
                        {t}
                      </a>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <FooterBar />
    </div>
  );
}

export default App;
