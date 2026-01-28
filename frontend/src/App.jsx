import React, { useState } from "react";
import WebcamFeed from "./components/webcamfeed";
import AlphabetReference from "./components/AlphabetReference";
import HeaderBar from "./components/HeaderBar";
import FooterBar from "./components/FooterBar";
import "./App.css";

function App() {
    const [showLandmarks, setShowLandmarks] = useState(false);

    return (
        <div className="page">
            <HeaderBar />

            <main className="stage">
                <section className="cameraColumn">
                    <div className="cameraHeader">
                        <h1 className="headline">Real-time ASL recognition.</h1>
                        <p className="subhead">
                            AYSPI uses a custom AI model to recognize fingerspelled letters directly from your webcam, and shows the result instantly.
                        </p>
                    </div>

                    <div className="glassCard cameraCard">
                        <div className="cardTopRow">
                            <div>
                                <div className="cardCaption">
                                    Keep your hand <strong>close</strong>, centered, and well-lit.
                                </div>
                            </div>

                            <div className="topControls">
                                <label className="toggle">
                                    <input
                                        type="checkbox"
                                        checked={showLandmarks}
                                        onChange={() => setShowLandmarks((v) => !v)}
                                    />
                                    <span className="toggleTrack" />
                                    <span className="toggleLabel">Landmarks</span>
                                </label>

                                <div className="chip">
                                    Model:{" "}
                                    <span className="chipStrong">
                                        asl_sequence_classifier.keras
                                    </span>
                                </div>
                            </div>
                        </div>

                        <WebcamFeed showLandmarks={showLandmarks} />
                    </div>
                </section>

                <section className="refColumn">
                    <div className="glassCard refCard">
                        <div className="refHeader">
                            <div>
                                <div className="refEyebrow">Reference</div>
                                <div className="refTitle">ASL Alphabet Guide</div>
                            </div>
                        </div>

                        <AlphabetReference />
                    </div>
                </section>
            </main>

            <FooterBar />
        </div>
    );
}

export default App;
