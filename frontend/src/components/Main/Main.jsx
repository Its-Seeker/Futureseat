import React, { useState, useEffect } from 'react'
import './Main.css'

import img1 from "../../assets/1.jpg";
import img2 from "../../assets/2.jpg";
import img3 from "../../assets/3.jpg";
import img4 from "../../assets/4.jpg";
import img5 from "../../assets/5.jpg";

import { FaLinkedin, FaEnvelope, FaTwitter } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

const Main = () => {
  const navigate = useNavigate();

  const images = [img1, img2, img3, img4, img5];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % images.length);
    }, 3000);

    return () => clearInterval(interval);
  }, [images.length]);

  return (
    <div className="main">

      {/* NAVBAR */}
      <nav className="main-navbar">
        <div className="main-logo">RankVision</div>

        <ul className="main-nav-links">
          <li>
            <button onClick={() => navigate("/rank")}>
              College Predictor
            </button>
          </li>

          <li>
            <button onClick={() => navigate("/about")}>
              About
            </button>
          </li>

          <li>
            <button onClick={() => navigate("/contact")}>
              Contact
            </button>
          </li>
        </ul>

        <button
          className="main-login-btn"
          onClick={() => navigate("/login")}
        >
          Login
        </button>
      </nav>

      {/* HERO WITH SLIDING BACKGROUND */}
      <div
        className="main-hero fade"
        style={{ backgroundImage: `url(${images[currentIndex]})` }}
      >
        <div className="main-hero-content">
          <h1>Find the Best Colleges Based on Your Rank</h1>
          <p>Enter your rank and discover the best engineering colleges.</p>

          <div className="main-search-box">
            <button onClick={() => navigate("/rank")}>
              Find Colleges
            </button>
          </div>
        </div>
      </div>

      {/* FOOTER */}
      <div className="Main-footer">
        <div className="Main-container footer-message">

          <div>
            <button
            className="contact-btn" 
            onClick={() => navigate("/contact")}>
              Contact
            </button>
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

export default Main;