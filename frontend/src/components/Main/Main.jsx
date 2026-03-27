import React from 'react'
import './Main.css'
import college_image from "../../assets/vision board.jpeg"
import { FaLinkedin, FaEnvelope, FaTwitter } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const Main = () => {
  const navigate = useNavigate(); // ✅ navigation enable

  return (
    <div className="main">
      <nav className="main-navbar">
        <div className="main-logo">FutureSeat</div>

        <ul className="main-nav-links">
          <li>
            <button onClick={() => navigate("/")}>Home</button>
          </li>

          <li>
            <button onClick={() => navigate("/rank")}>
              College Predictor
            </button>
          </li>

          <li>
            <button>Colleges</button>
          </li>

          <li>
            <button onClick={() => navigate("/about")}>
              About
            </button>
          </li>

          <li>
            <button>Contact</button>
          </li>
        </ul>

        <button className="main-login-btn">Login</button>
      </nav>

      <div
        className="main-hero"
        style={{ backgroundImage: `url(${college_image})` }}
      >
        <div className="main-hero-content">
          <h1>Find the Best Colleges Based on Your JEE Rank</h1>
          <p>Enter your rank and discover the best engineering colleges.</p>

          <div className="main-search-box">
            <input type="text" placeholder="Enter Rank" />

            {/* ✅ Predict button → Rank page */}
            <button onClick={() => navigate("/rank")}>
              Predict College
            </button>
          </div>
        </div>
      </div>

      <div className="Main-footer">
        <div className="Main-container footer-message">

          <div>
            <h4>Contact</h4>

            <p><FaLinkedin /> Linkedin</p>
            <p><FaEnvelope /> Mail</p>
            <p><FaTwitter /> Twitter</p>
          </div>

          <div>
            <h4>Legal</h4>
            <p>Privacy Policy</p>
            <p>Terms</p>
          </div>

        </div>
      </div>
    </div>
  )
}

export default Main