import React, { useState, useEffect, useRef } from "react";
import { uploadFile, getStatus } from "./api";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [taskId, setTaskId] = useState(null);
  const [status, setStatus] = useState("");
  const [data, setData] = useState([]);
  const [error, setError] = useState("");
  const resultsRef = useRef();

  const handleUpload = async () => {
    setError("");
    setData([]);
    setStatus("PENDING");
    try {
      const resp = await uploadFile(file);
      setTaskId(resp.data.task_id);
    } catch {
      setError("Upload failed. Please try again.");
      setStatus("");
    }
  };

  useEffect(() => {
    if (!taskId) return;
    const iv = setInterval(async () => {
      try {
        const resp = await getStatus(taskId);
        const s = resp.data.status;
        setStatus(s);
        if (s === "ERROR") {
          setError(resp.data.message);
          clearInterval(iv);
        }
        if (s === "SUCCESS") {
          setData(resp.data.data);
          clearInterval(iv);
        }
      } catch {
        setError("Error checking status.");
        clearInterval(iv);
      }
    }, 2000);
    return () => clearInterval(iv);
  }, [taskId]);

  // Scroll to results when ready
  useEffect(() => {
    if (status === "SUCCESS" && resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [status]);

  return (
    <div className="app">
      <div className="top-panel">
        <h1 className="title" style={{ fontFamily: "'Kanit', sans-serif" }}>
          LegalFinePrint
        </h1>

        <div className="uploader">
          <input
            id="file-input"
            type="file"
            accept=".pdf,.docx,.doc"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button
            className="analyze-button"
            onClick={handleUpload}
            disabled={!file || status === "PENDING"}
          >
            Analyze
          </button>
        </div>
      </div>

      {status === "PENDING" && (
        <div className="loader-container">
          <div className="loader" />
          <p className="processing-text">Processing…</p>
        </div>
      )}

      {error && <div className="error">{error}</div>}

      {status === "SUCCESS" && (
        <div className="results" ref={resultsRef}>
          {data.map((c, i) => {
            const riskClass =
              c.risk_label === "Normal" ? "card low" : "card high";
            return (
              <div key={i} className={riskClass}>
                <div className="header">
                  <span className="label">{c.risk_label}</span>
                </div>
                {c.summary && <p className="summary">{c.summary}</p>}
                <p className="text">{c.text}</p>
                <details className="analysis">
                  <summary>Analysis</summary>
                  <pre>{c.analysis}</pre>
                </details>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
