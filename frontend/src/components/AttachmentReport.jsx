export default function AttachmentReport({ attachments }) {
  if (!attachments || attachments.length === 0) {
    return <p style={{ color: "#666", fontSize: 14 }}>No attachments found in this email.</p>;
  }

  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ fontSize: 16, marginBottom: 10 }}>Attachment Sandbox Report</h3>
      {attachments.map((a, i) => {
        const malicious = a.status === "found" && a.malicious > 0;
        const color = malicious ? "#d93025" : a.status === "found" ? "#1e8e3e" : "#888";
        const label = malicious ? "Malicious" : a.status === "found" ? "Clean" : "Unknown / Not in VT DB";
        return (
          <div key={i} style={{ border: "1px solid #e0e0e0", borderRadius: 8, padding: 12, marginBottom: 8 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <strong style={{ fontSize: 14 }}>{a.filename}</strong>
              <span style={{
                background: color, color: "#fff", fontSize: 12, fontWeight: 600,
                padding: "2px 10px", borderRadius: 12
              }}>{label}</span>
            </div>
            <div style={{ fontSize: 12, color: "#666", marginTop: 6, wordBreak: "break-all" }}>
              SHA256: {a.sha256}
            </div>
            {a.status === "found" && (
              <div style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
                Detections: {a.malicious} malicious, {a.suspicious} suspicious · Type: {a.type_description || "n/a"}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
