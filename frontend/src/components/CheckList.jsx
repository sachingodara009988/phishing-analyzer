const ICONS = {
  pass: { symbol: "✓", color: "#1e8e3e" },
  fail: { symbol: "✗", color: "#d93025" },
  warning: { symbol: "!", color: "#c98a00" },
};

export default function CheckList({ title, checks }) {
  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ fontSize: 16, marginBottom: 10 }}>{title}</h3>
      <div style={{ border: "1px solid #e0e0e0", borderRadius: 8, overflow: "hidden" }}>
        {checks.map((c, i) => {
          const icon = ICONS[c.status] || ICONS.warning;
          return (
            <div key={i} style={{
              display: "flex", alignItems: "flex-start", gap: 10,
              padding: "10px 14px", borderBottom: i < checks.length - 1 ? "1px solid #eee" : "none",
              background: i % 2 === 0 ? "#fafafa" : "#fff"
            }}>
              <span style={{
                width: 20, height: 20, borderRadius: "50%", background: icon.color,
                color: "#fff", fontSize: 12, display: "flex", alignItems: "center",
                justifyContent: "center", flexShrink: 0, marginTop: 2
              }}>{icon.symbol}</span>
              <div>
                <div style={{ fontWeight: 600, fontSize: 14 }}>{c.name}</div>
                <div style={{ fontSize: 13, color: "#666" }}>{c.detail}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
