function verdictOf(u) {
  if (u.status !== "found") return { label: u.status.replace("_", " "), color: "#888" };
  if (u.malicious > 0) return { label: "Malicious", color: "#d93025" };
  if (u.suspicious > 0) return { label: "Suspicious", color: "#c98a00" };
  return { label: "Clean", color: "#1e8e3e" };
}

export default function URLReport({ urls, urlscanReports }) {
  if (!urls || urls.length === 0) {
    return <p style={{ color: "#666", fontSize: 14 }}>No URLs found in this email.</p>;
  }

  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ fontSize: 16, marginBottom: 10 }}>URL / Link Reputation</h3>
      {urls.map((u, i) => {
        const v = verdictOf(u);
        const scan = urlscanReports?.find(s => s.url === u.url);
        return (
          <div key={i} style={{ border: "1px solid #e0e0e0", borderRadius: 8, padding: 12, marginBottom: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 10 }}>
              <div style={{ fontSize: 13, wordBreak: "break-all", flex: 1 }}>{u.url}</div>
              <span style={{
                background: v.color, color: "#fff", fontSize: 12, fontWeight: 600,
                padding: "2px 10px", borderRadius: 12, flexShrink: 0
              }}>{v.label}</span>
            </div>
            {u.status === "found" && (
              <div style={{ fontSize: 12, color: "#666", marginTop: 6 }}>
                Malicious: {u.malicious} · Suspicious: {u.suspicious} · Harmless: {u.harmless}
              </div>
            )}
            {scan && scan.status === "complete" && (
              <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
                urlscan.io score: {scan.score} ·{" "}
                <a href={scan.report_url} target="_blank" rel="noreferrer">View live scan report</a>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
