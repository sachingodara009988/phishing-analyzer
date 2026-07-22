export default function VerdictBanner({ verdict, aiSummary }) {
  const colors = {
    Low: { bg: "#e6f6ec", border: "#1e8e3e", text: "#1e8e3e" },
    Medium: { bg: "#fff8e1", border: "#c98a00", text: "#c98a00" },
    High: { bg: "#fdecea", border: "#d93025", text: "#d93025" },
    Critical: { bg: "#fce4e4", border: "#a50e0e", text: "#a50e0e" },
  };
  const c = colors[verdict.verdict] || colors.Medium;

  return (
    <div style={{
      background: c.bg, border: `2px solid ${c.border}`, borderRadius: 10,
      padding: "20px 24px", marginBottom: 24
    }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div>
          <div style={{ fontSize: 13, color: "#555", fontWeight: 600, letterSpacing: 0.5 }}>VERDICT</div>
          <div style={{ fontSize: 28, fontWeight: 800, color: c.text }}>{verdict.verdict} Risk</div>
        </div>
        <div style={{ textAlign: "right" }}>
          <div style={{ fontSize: 13, color: "#555" }}>Risk Score</div>
          <div style={{ fontSize: 28, fontWeight: 800, color: c.text }}>{verdict.score}/100</div>
        </div>
      </div>

      {aiSummary && (
        <div style={{ marginTop: 12, fontSize: 15, color: "#333" }}>
          <strong>AI Summary:</strong> {aiSummary}
        </div>
      )}

      {verdict.reasons?.length > 0 && (
        <ul style={{ marginTop: 12, paddingLeft: 20 }}>
          {verdict.reasons.map((r, i) => (
            <li key={i} style={{ fontSize: 14, color: "#444", marginBottom: 4 }}>{r}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
