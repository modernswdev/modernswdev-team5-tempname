import {useState } from "react";
import { useNavigate } from "react-router-dom";
import Card from "../components/Card.jsx";
import colors from "../colors";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });
   
      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Invalid email or password.");
        return;
      }

      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/home");
    } catch (err) {
      setError("An error occurred. Please try again.");
    }
  };

  return (
    <Card size="narrow">
      <div style={{padding: "2rem 2.5rem"}}>
        <section style={{maxWidth: "480px", margin: "0 auto"}}>
          <h2 style={{marginBottom: "1rem", color: colors.textMain}}>
            Service Tracker Login
          </h2>

          <form onSubmit={handleLogin} 
          style={{display: "flex", flexDirection: "column", gap: "1rem"}}
          >

            <label style={{fontSize: "0.9rem", color: colors.textMain }}>
              Email
              <input 
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                  width: "100%",
                  marginTop: "0.25rem",
                  padding: "0.5rem 0.6rem",
                  borderRadius: "0.45rem",
                  border: `1px solid ${colors.border}`,
                }}/>
            </label>

            <label style={{fontSize: "0.9rem", color: colors.textMain }}>
              Password
              <input type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  width: "100%",
                  marginTop: "0.25rem",
                  padding: "0.5rem 0.6rem",
                  borderRadius: "0.45rem",
                  border: `1px solid ${colors.border}`,
                }}/>
            </label>
            
            {error && <div style={{color: colors.error, fontSize: "0.85rem"}}>{error}</div>}


            <button type="submit" style={{marginTop: "0.5rem",
                padding: "0.6rem 1.4rem",
                borderRadius: "999px",
                border: "none",
                backgroundColor: colors.primary,
                color: colors.surface,
                fontWeight: 600,
              }}> Login
            </button>
          </form>
        </section>
      </div>
    </Card>
  );
}
