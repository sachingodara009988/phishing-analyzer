const BASE = "/api";

export async function analyzeFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${BASE}/analyze/file`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

export async function analyzeHeaders(headerText) {
  const formData = new FormData();
  formData.append("header_text", headerText);
  const res = await fetch(`${BASE}/analyze/headers`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}

export async function analyzeRaw(rawText) {
  const formData = new FormData();
  formData.append("raw_email", rawText);
  const res = await fetch(`${BASE}/analyze/raw`, { method: "POST", body: formData });
  if (!res.ok) throw new Error(`Server error: ${res.status}`);
  return res.json();
}
