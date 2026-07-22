export default function DomainReport({ domainRep, domainAge }) {
  if (!domainRep) return null;

  return (
    <div style={{ marginBottom: 24 }}>
      <h3 style={{ fontSize: 16, marginBottom: 10 }}>Sender Domain Reputation</h3>
      <div style={{ border: "1px solid #e0e0e0", borderRadius: 8, padding: 12 }}>
        <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 6 }}>{domainRep.domain}</div>
        {domainRep.status === "found" ? (
          <div style={{ fontSize: 13, color: "#666" }}>
            Malicious: {domainRep.malicious} · Suspicious: {domainRep.suspicious} · Harmless: {domainRep.harmless}
            <br />Reputation score: {domainRep.reputation_score}
          </div>
        ) : (
          <div style={{ fontSize: 13, color: "#888" }}>No VirusTotal data available for this domain.</div>
        )}
        {domainAge?.status === "found" && (
          <div style={{
            fontSize: 13, marginTop: 8,
            color: domainAge.newly_registered ? "#d93025" : "#666"
          }}>
            Domain age: {domainAge.age_days} days (registered {domainAge.creation_date})
            {domainAge.newly_registered && "  ⚠ Newly registered — common phishing signal"}
          </div>
        )}
      </div>
    </div>
  );
}
