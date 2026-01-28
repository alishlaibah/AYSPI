import React, { useRef, useEffect, useState, useCallback } from "react";
import { Hands, HAND_CONNECTIONS } from "@mediapipe/hands";
import "./webcamfeed.css";

const DEFAULT_SEQ_LEN = 30;
const SEND_INTERVAL_MS = 250;
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

function WebcamFeed({ showLandmarks = true }) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const stageRef = useRef(null);
  const handsRef = useRef(null);

  const sequenceRef = useRef([]);
  const lastSentRef = useRef(0);
  const inFlightRef = useRef(false);

  const showLandmarksRef = useRef(showLandmarks);

  const [seqLen, setSeqLen] = useState(DEFAULT_SEQ_LEN);
  const [prediction, setPrediction] = useState({ letter: "-", confidence: 0 });
  const [status, setStatus] = useState("Waiting for hand...");
  const [error, setError] = useState("");

  useEffect(() => {
    showLandmarksRef.current = showLandmarks;
  }, [showLandmarks]);

  const handleVideoMetadata = useCallback(() => {
    const videoEl = videoRef.current;
    const stageEl = stageRef.current;

    if (!videoEl || !stageEl) return;

    const { videoWidth, videoHeight } = videoEl;

    if (videoWidth && videoHeight) {
      const aspectRatio = videoWidth / videoHeight;
      stageEl.style.setProperty("--cam-aspect", aspectRatio.toFixed(6));

      console.log(
        `Camera resolution: ${videoWidth}×${videoHeight} (aspect: ${aspectRatio.toFixed(3)})`
      );
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    fetch(`${API_BASE}/metadata`)
      .then(async (res) => {
        if (!res.ok) {
          const text = await res.text();
          throw new Error(text || `Metadata request failed: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        if (!isMounted) return;
        if (data?.seq_len) setSeqLen(data.seq_len);
      })
      .catch((err) => {
        if (!isMounted) return;
        console.warn("Metadata fetch failed:", err);
        setError("Failed to fetch");
      });

    return () => {
      isMounted = false;
    };
  }, []);

  // Reset sequence if seqLen changes
  useEffect(() => {
    sequenceRef.current = [];
  }, [seqLen]);

  // Start webcam stream
  useEffect(() => {
    let stream;

    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((s) => {
        stream = s;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      })
      .catch((err) => {
        console.error("Error accessing webcam:", err);
        setError("Webcam permission denied or not available.");
      });

    return () => {
      if (stream) {
        stream.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  useEffect(() => {
    if (handsRef.current) return;

    const hands = new Hands({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
    });

    hands.setOptions({
      maxNumHands: 1,
      minDetectionConfidence: 0.9,
      minTrackingConfidence: 0.9,
      modelComplexity: 1,
    });

    hands.onResults((results) => {
      const videoEl = videoRef.current;
      const canvasEl = canvasRef.current;
      const stageEl = stageRef.current;

      if (!videoEl || !canvasEl || !stageEl) return;

      const ctx = canvasEl.getContext("2d");
      if (!ctx) return;

      const videoW = videoEl.videoWidth;
      const videoH = videoEl.videoHeight;

      if (!videoW || !videoH) return;

      const stageRect = stageEl.getBoundingClientRect();
      const stageW = stageRect.width;
      const stageH = stageRect.height;

      if (!stageW || !stageH) return;

      const dpr = window.devicePixelRatio || 1;
      const canvasW = Math.round(stageW * dpr);
      const canvasH = Math.round(stageH * dpr);

      if (canvasEl.width !== canvasW || canvasEl.height !== canvasH) {
        canvasEl.width = canvasW;
        canvasEl.height = canvasH;
      }

      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvasW, canvasH);

      ctx.scale(dpr, dpr);

      const hasHand =
        results.multiHandLandmarks && results.multiHandLandmarks.length > 0;

      if (!hasHand) {
        setStatus("No hand detected");
        return;
      }

      setStatus("Hand detected");

      const landmarks = results.multiHandLandmarks[0];
      if (showLandmarksRef.current) {
        const scale = Math.min(stageW / videoW, stageH / videoH);
        const scaledW = videoW * scale;
        const scaledH = videoH * scale;

        const offsetX = (stageW - scaledW) / 2;
        const offsetY = (stageH - scaledH) / 2;

        const transformedLandmarks = landmarks.map((lm) => ({
          x: offsetX + lm.x * scaledW,
          y: offsetY + lm.y * scaledH,
          z: lm.z,
        }));

        ctx.strokeStyle = "#4DE1FF";
        ctx.lineWidth = 2;
        ctx.lineCap = "round";
        ctx.lineJoin = "round";

        for (const [startIdx, endIdx] of HAND_CONNECTIONS) {
          const start = transformedLandmarks[startIdx];
          const end = transformedLandmarks[endIdx];

          ctx.beginPath();
          ctx.moveTo(start.x, start.y);
          ctx.lineTo(end.x, end.y);
          ctx.stroke();
        }

        ctx.fillStyle = "#7C5CFF";

        for (const lm of transformedLandmarks) {
          ctx.beginPath();
          ctx.arc(lm.x, lm.y, 4, 0, 2 * Math.PI);
          ctx.fill();
        }

        ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
        ctx.lineWidth = 1;

        for (const lm of transformedLandmarks) {
          ctx.beginPath();
          ctx.arc(lm.x, lm.y, 4, 0, 2 * Math.PI);
          ctx.stroke();
        }
      }

      const frame = [];
      for (const lm of landmarks) {
        frame.push(lm.x, lm.y, lm.z);
      }

      sequenceRef.current.push(frame);
      if (sequenceRef.current.length > seqLen) {
        sequenceRef.current.shift();
      }

      const now = Date.now();
      const shouldSend =
        sequenceRef.current.length === seqLen &&
        !inFlightRef.current &&
        now - lastSentRef.current > SEND_INTERVAL_MS;

      if (!shouldSend) return;

      inFlightRef.current = true;
      lastSentRef.current = now;

      fetch(`${API_BASE}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ landmarks: sequenceRef.current.flat() }),
      })
        .then(async (res) => {
          if (!res.ok) {
            const text = await res.text();
            throw new Error(text || `Request failed: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          if (data?.error) {
            setError(data.error);
          } else {
            setError("");
          }

          if (data?.letter) {
            setPrediction({
              letter: data.letter,
              confidence: data.confidence ?? 0,
            });
          }
        })
        .catch((err) => {
          setError(err.message || "Prediction failed");
        })
        .finally(() => {
          inFlightRef.current = false;
        });
    });

    let animationFrameId;

    async function loop() {
      const videoEl = videoRef.current;
      if (videoEl && videoEl.readyState >= 2) {
        await hands.send({ image: videoEl });
      }
      animationFrameId = requestAnimationFrame(loop);
    }

    animationFrameId = requestAnimationFrame(loop);
    handsRef.current = hands;

    return () => {
      cancelAnimationFrame(animationFrameId);
      hands.close();
      handsRef.current = null;
    };
  }, [seqLen]);

  return (
    <div className="webcam-shell">
      <div className="webcam-stage" ref={stageRef}>
        <video
          ref={videoRef}
          autoPlay
          playsInline
          muted
          className="webcam-video"
          onLoadedMetadata={handleVideoMetadata}
        />
        <canvas ref={canvasRef} className="webcam-canvas" />

        <div className="webcam-badge" aria-live="polite">
          {prediction.letter}
        </div>
      </div>

      <div className="webcam-meta">
        <div className="webcam-row">
          <span className="webcam-label">Prediction</span>
          <span className="webcam-value">{prediction.letter}</span>
        </div>

        <div className="webcam-row">
          <span className="webcam-label">Confidence</span>
          <span className="webcam-value">
            {Number(prediction.confidence).toFixed(2)}
          </span>
        </div>

        <div className="webcam-status">{status}</div>
        {error ? <div className="webcam-error">{error}</div> : null}
      </div>
    </div>
  );
}

export default WebcamFeed;