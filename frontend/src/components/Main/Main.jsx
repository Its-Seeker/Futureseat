import React from 'react'
import './Main.css'
import college_image from "../../assets/vision board.jpeg"

const Main = () => {
  return (
    <div className="main">
      <nav className="main-navbar">
        <div className="main-logo">FutureSeat</div>

        <ul className="main-nav-links">
          <li><a href="#">Home</a></li>
          <li><a href="#">College Predictor</a></li>
          <li><a href="#">Colleges</a></li>
          <li><a href="#">About</a></li>
          <li><a href="#">Contact</a></li>
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
            <button>Predict College</button>
          </div>
        </div>
      </div>

      <div className="main-scroll-down">
        <h1>tyfyfytfyfytfyfutfuyttu</h1>
        <h1>tyfyfytfyfytfyfutfuyttu</h1>
        <h1>tyfyfytfyfytfyfutfuyttu</h1>
        <h1>tyfyfytfyfytfyfutfuyttu</h1>
        <h1>tyfyfytfyfytfyfutfuyttu</h1>
      </div>
    </div>
  )
}

export default Main