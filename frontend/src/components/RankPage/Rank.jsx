import React from "react";
import './rank.css'
import { FaLinkedin, FaEnvelope, FaTwitter } from "react-icons/fa";
import { FaShieldAlt, FaTrophy, FaStar } from "react-icons/fa";

const Rank = () => {
    return (
        <div className="rank-page">

            {/* NAVBAR */}
            <div className="rank-navbar">
                <div className="rank-container">
                    <h2>Rank Vision</h2>
                    <p>About</p>
                </div>
            </div>

            {/* HERO */}
            <div className="rank-hero-section">
                <div className="rank-container rank-hero">

                    <div className="rank-hero-left">
                        <h1>
                            From <span>Rank</span> to Reality
                        </h1>
                        <p>
                            Understand your JEE Mains chances and plan your college strategy smarter
                        </p>

                        <div className="rank-form-box">
                            <div className="rank-input-group">
                                <label>Exam type</label>
                                <select><option>JEE Main</option></select>
                            </div>

                            <div className="rank-input-group">
                                <label>Exam type</label>
                                <select><option>JEE Main</option></select>
                            </div>

                            <div className="rank-input-group">
                                <label>Exam type</label>
                                <select><option>JEE Main</option></select>
                            </div>

                            <div className="rank-input-group">
                                <label>Exam type</label>
                                <select><option>JEE Main</option></select>
                            </div>

                            <button>Analyze my marks</button>
                        </div>
                    </div>

                    <div className="rank-hero-right">
                        <div className="graph-placeholder">Graph Area</div>
                    </div>

                </div>
            </div>

            {/* HOW */}
            <div className="rank-how-section">
                <div className="rank-container">
                    <h2>How it works ?</h2>

                    <div className="rank-steps">
                        <div className="rank-step">
                            <div className="rank-circle">1</div>
                            <p>Enter details like Marks, Branch, etc.</p>
                        </div>

                        <div className="rank-step">
                            <div className="rank-circle">2</div>
                            <p>Get estimated ranks.</p>
                        </div>

                        <div className="rank-step">
                            <div className="rank-circle">3</div>
                            <p>Explore college options.</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* CATEGORY */}
            <div className="rank-category-section">
                <div className="rank-container">
                    <h2>College Categories</h2>

                    <div className="rank-card green">
                        <FaShieldAlt className="card-icon green-icon" />
                        <div>
                            <h3>Safe</h3>
                            <p>High Chance</p>
                        </div>
                    </div>

                    <div className="rank-card yellow">
                        <FaTrophy className="card-icon yellow-icon" />
                        <div>
                            <h3>Competitive</h3>
                            <p>Realistic Target</p>
                        </div>
                    </div>

                    <div className="rank-card red">
                        <FaStar className="card-icon red-icon" />
                        <div>
                            <h3>Aspirational</h3>
                            <p>Ambitious with current score</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* FOOTER */}
            <div className="rank-footer">
                <div className="rank-container footer-content">

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
    );
};

export default Rank;