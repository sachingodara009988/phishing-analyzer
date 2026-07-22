import { useState } from "react";

export default function InputTabs({ onAnalyze, loading }) {
  const [tab, setTab] = useState("file");
  const [file, setFile] = useState(null);
  const [headerText, setHeaderText] = useState("");
  const [rawText, setRawText] = useState("");

  const tabs = [
    { id: "file", label: "Upload .eml file" },
    { id: "headers", label: "Paste headers only" },
    { id: "raw", label: "Paste raw email" },
  ];

  const handleSubmit = () => {
    if (tab === "file" && file) onAnalyze({ type: "file", value: file });
    if (tab === "headers" && headerText.trim()) onAnalyze({ type: "headers", value: headerText });
    if (tab === "raw" && rawText.trim()) onAnalyze({ type: "raw", value: rawText });
  };

  const canSubmit =
    (tab === "file" && file) ||
    (tab === "headers" && headerText.trim()) ||
    (tab === "raw" && rawText.trim());

  return (
    <div style={{ marginBottom: 24 }}>
      <div style={{ display: "flex", gap: 4, marginBottom: 14 }}>
        {tabs.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              padding: "8px 16px", borderRadius: 20, border: "none", cursor: "pointer",
              fontSize: 13, fontWeight: 600,
              background: tab === t.id ? "#1a73e8" : "#eee",
              color: tab === t.id ? "#fff" : "#333",
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {tab === "file" && (
        <input
          type="file"
          accept=".eml,.msg,.txt"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ display: "block", marginBottom: 10 }}
        />
      )}

      {tab === "headers" && (
        <textarea
          rows={10}
          placeholder="Paste email headers here (From, Received, Authentication-Results, etc.)"
          value={headerText}
          onChange={(e) => setHeaderText(e.target.value)}
          style={{ width: "100%", fontFamily: "monospace", fontSize: 13, padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
        />
      )}

      {tab === "raw" && (
        <textarea
          rows={12}
          placeholder="Paste the full raw email source (View Source / Show Original in your mail client)"
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          style={{ width: "100%", fontFamily: "monospace", fontSize: 13, padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
        />
      )}

      <button
        onClick={handleSubmit}
        disabled={!canSubmit || loading}
        style={{
          marginTop: 12, padding: "10px 24px", borderRadius: 8, border: "none",
          background: canSubmit && !loading ? "#1a73e8" : "#aac1ee",
          color: "#fff", fontWeight: 700, fontSize: 14,
          cursor: canSubmit && !loading ? "pointer" : "not-allowed"
        }}
      >
        {loading ? "Analyzing..." : "Analyze Email"}
      </button>
    </div>
  );
}
