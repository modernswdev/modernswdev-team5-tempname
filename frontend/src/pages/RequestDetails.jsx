import { useEffect, useState } from "react";
import {Link, useParams} from "react-router-dom";
import Card from "../components/Card.jsx";
import Navbar from "../components/Navbar.jsx";
import colors from "../colors";

export default function RequestDetails() {
  const {id} = useParams();

  const [request, setRequest] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/requests/${id}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Failed to fetch request details");
        }
        return res.json();
      })
      .then((data) => {
        setRequest(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load request details");
        setLoading(false);
      });
    }, [id]);

    const pageStyle = {
      padding:"2rem 2.5rem 2.5rem",
      backgroundColor: colors.lgbackground,
      minHeight: "100%",
    };

    const cardStyle = {
      backgroundColor: colors.surface,
      borderRadius: "1rem",
      boarder: `1px solid ${colors.border}`,
      padding: "1.5rem",
      display: "grid",
      gap: "1rem",
    };

    const labelStyle = {
      fontSize: "0.8rem",
      fontWeight: 700,
      letterSpacing: "0.06em",
      textTransform: "uppercase",
      color: colors.textMuted,
      marginBottom: "0.35rem",
    };

    const valueStyle = {
      fontSize: "1rem",
      color: colors.textMain,
    };
    
    if (loading) {
      return (
        <Card>
        <Navbar />
        <div style={pageStyle}>
          <h2 style={{ fontSize: "1.6rem", fontWeight: 700, color: colors.textMain }}>
            Request Details
          </h2>
          <p style={{color :colors.textMuted}}>Loading...</p>
        </div>
      </Card>
    );
  }

  if (error || !request) {
    return (
      <Card>
        <Navbar />
        <div style={pageStyle}>
          <h2 style={{ fontSize: "1.6rem", fontWeight: 700, color: colors.textMain }}>
            Request Details
          </h2>
          <p style={{color: "red"}}> {error ||"Failed to load request details" }</p>
          <Link to = "/home" style={{ color: colors.textMain, fontWeight: 600}}>
          Back to Dashboard 
          </Link>
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <Navbar />
      <div style={pageStyle}>
        <div style={{ marginBottom: "1.5rem" }}>
          <h2 style={{ fontsize: "1.6rem", fontWeight: 700, color: colors.textMain }}>
            Request Details
          </h2>
          <Link to="/home" style={{ color: colors.textMain, fontWeight: 600 }}>
            Back to Dashboard
          </Link>
        </div>

        <section style={cardStyle}>
          <div>
            <div style={labelStyle}>Request ID</div>
            <div style={valueStyle}>{request.id}</div>
          </div>

          <div>
            <div style={labelStyle}>Title</div>
            <div style={valueStyle}>{request.title}</div>
          </div>

          <div>
            <div style={labelStyle}>submitted By</div>
            <div style={valueStyle}>{request.user || "--"}</div>
          </div>

          <div>
            <div style={labelStyle}>Description</div>
            <div style={valueStyle}>{request.description || "--"}</div>
          </div>

          <div>
            <div style={labelStyle}>Created Date</div>
            <div style={valueStyle}>{request.created_at || "--"}</div>
          </div>

          <div>
            <div style={labelStyle}>Updated Date</div>
            <div style={valueStyle}>{request.updated_at || "--"}</div>
          </div>

          <div>
            <div style={labelStyle}>Priority</div>
            <div style={valueStyle}>{request.priority || "--"}</div>
          </div>

          <div>
            <div style={labelStyle}>Status</div>
            <div style={valueStyle}>{request.status || "--"}</div>
          </div>
        </section>
      </div>
    </Card>
  
  );
}