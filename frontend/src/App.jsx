import { useState } from "react";
import InputTabs from "./components/InputTabs";
import VerdictBanner from "./components/VerdictBanner";
import CheckList from "./components/CheckList";
import URLReport from "./components/URLReport";
import AttachmentReport from "./components/AttachmentReport";
import DomainReport from "./components/DomainReport";
import { analyzeFile, analyzeHeaders, analyzeRaw } from "./api";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async ({ type, value }) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      let data;
      if (type === "file") data = await analyzeFile(value);
      else if (type === "headers") data = await analyzeHeaders(value);
      else data = await analyzeRaw(value);
      setResult(data);
    } catch (e) {
      setError(e.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      maxWidth: 800, margin: "0 auto", padding: "32px 20px",
      fontFamily: "'Segoe UI', system-ui, sans-serif", color: "#222"
    }}>
      <header style={{ marginBottom: 28 }}>
        <h1 style={{ fontSize: 28, marginBottom: 4 }}>🎣 Phishing Mail Analyzer</h1>
        <p style={{ color: "#666", fontSize: 14 }}>
          Upload an email or paste headers to check reputation, header authenticity, attachments, and AI-based phishing indicators.
        </p>
      </header>

      <InputTabs onAnalyze={handleAnalyze} loading={loading} />

      {error && (
        <div style={{ background: "#fdecea", border: "1px solid #d93025", borderRadius: 8, padding: 12, marginBottom: 20, color: "#d93025", fontSize: 14 }}>
          Error: {error}
        </div>
      )}

      {loading && (
        <div style={{ textAlign: "center", padding: 40, color: "#666" }}>
          Running header checks, reputation lookups, and AI analysis…
        </div>
      )}

      {result && (
        <div>
          <VerdictBanner verdict={result.verdict} aiSummary={result.ai_analysis?.summary} />
          <CheckList title="Header Authentication Checklist" checks={result.headers.checks} />
          <DomainReport domainRep={result.domain_reputation} domainAge={result.domain_age} />
          <URLReport urls={result.urls} urlscanReports={result.urlscan} />
          <AttachmentReport attachments={result.attachments} />

          {result.ai_analysis?.status === "success" && (
            <div style={{ marginBottom: 24 }}>
              <h3 style={{ fontSize: 16, marginBottom: 10 }}>AI Content Analysis (Gemini)</h3>
              <div style={{ border: "1px solid #e0e0e0", borderRadius: 8, padding: 12, fontSize: 14 }}>
                <div><strong>Likely phishing:</strong> {result.ai_analysis.is_likely_phishing ? "Yes" : "No"} ({result.ai_analysis.confidence} confidence)</div>
                {result.ai_analysis.impersonated_brand && (
                  <div style={{ marginTop: 6 }}><strong>Possible impersonation:</strong> {result.ai_analysis.impersonated_brand}</div>
                )}
                {result.ai_analysis.social_engineering_tactics?.length > 0 && (
                  <div style={{ marginTop: 6 }}>
                    <strong>Social engineering tactics:</strong> {result.ai_analysis.social_engineering_tactics.join(", ")}
                  </div>
                )}
                {result.ai_analysis.tone_red_flags?.length > 0 && (
                  <div style={{ marginTop: 6 }}>
                    <strong>Tone red flags:</strong> {result.ai_analysis.tone_red_flags.join(", ")}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
