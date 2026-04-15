import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import Card from "../components/Card.jsx";
import Navbar from "../components/Navbar.jsx";
import colors from "../colors";

export default function CreateRequest() {
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("Medium");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const pageStyle = {
    padding: "2rem 2.5rem 2.5rem",
    backgroundColor: colors.lgBackground,
    minHeight: "100%",
  };

  const formCardStyle = {
    backgroundColor: colors.surface,
    borderRadius: "1rem",
    border: `1px solid ${colors.border}`,
    padding: "1.5rem",
    display: "grid",
    gap: "1rem",
    maxWidth: "700px",
  };

  const labelStyle = {
    fontSize: "0.9rem",
    fontWeight: 600,
    color: colors.textMain,
    display: "flex",
    flexDirection: "column",
    gap: "0.4rem",
  };

  const inputStyle = {
    width: "100%",
    padding: "0.7rem 0.8rem",
    borderRadius: "0.6rem",
    border: `1px solid ${colors.border}`,
    backgroundColor: colors.surface,
    color: colors.textMain,
    fontSize: "0.95rem",
    boxSizing: "border-box",
  };

  const buttonStyle = {
    padding: "0.7rem 1.4rem",
    borderRadius: "999px",
    border: "none",
    backgroundColor: colors.primary,
    color: colors.surface,
    fontWeight: 600,
    cursor: "pointer",
  };

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);

    try {
      const response = await fetch("http://localhost:8000/requests", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title,
          description,
          priority,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to create request.");
        setSubmitting(false);
        return;
      }

      navigate("/home");
    } catch (err) {
      setError("Could not connect to the backend.");
      setSubmitting(false);
      return;
    }

    setSubmitting(false);
  }

  return (
    <Card>
      <Navbar />
      <div style={pageStyle}>
        <div style={{ marginBottom: "1.5rem" }}>
          <h2
            style={{
              fontSize: "1.6rem",
              fontWeight: 700,
              color: colors.textMain,
              marginBottom: "0.5rem",
            }}
          >
            Create Request
          </h2>

          <Link to="/home" style={{ color: colors.textMain, fontWeight: 600 }}>
            ← Back to Dashboard
          </Link>
        </div>

        <form onSubmit={handleSubmit} style={formCardStyle}>
          <label style={labelStyle}>
            Title
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              style={inputStyle}
              placeholder="Enter request title"
            />
          </label>

          <label style={labelStyle}>
            Description
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              rows={6}
              style={{ ...inputStyle, resize: "vertical" }}
              placeholder="Describe the issue"
            />
          </label>

          <label style={labelStyle}>
            Priority
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              style={inputStyle}
            >
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </label>

          {error && (
            <div style={{ color: "red", fontSize: "0.9rem" }}>{error}</div>
          )}

          <div style={{ display: "flex", gap: "0.75rem" }}>
            <button type="submit" style={buttonStyle} disabled={submitting}>
              {submitting ? "Submitting..." : "Submit Request"}
            </button>

            <Link
              to="/home"
              style={{
                ...buttonStyle,
                textDecoration: "none",
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                backgroundColor: colors.surface,
                color: colors.textMain,
                border: `1px solid ${colors.border}`,
              }}
            >
              Cancel
            </Link>
          </div>
        </form>
      </div>
    </Card>
  );
}
