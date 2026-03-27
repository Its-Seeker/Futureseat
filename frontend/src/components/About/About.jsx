import React from "react";
import "./About.css";
import { useNavigate } from "react-router-dom";

const About = () => {
    const navigate = useNavigate();
    return (
        <div className="about-page">

            {/* NAVBAR */}
            <div className="about-nav">
                <div className="about-logo">
                    Rank<span>Vision</span>
                </div>
                <button
                    className="about-nav-link"
                    onClick={() => navigate("/")}
                >
                    Home
                </button>
            </div>

            {/* BODY */}
            <div className="about-body">

                <div className="about-eyebrow">About RankVision</div>

                <h1 className="about-heading">
                    Built for students,<br />not algorithms
                </h1>

                <p className="about-sub">
                    RankVision helps JEE and NEET students cut through the noise and find
                    colleges that are actually within reach — based on real cutoff data,
                    not guesswork.
                </p>

                {/* STATS */}
                <div className="about-stats">
                    <div className="about-stat">
                        <div className="about-stat-num">2000+</div>
                        <div className="about-stat-lbl">Total courses</div>
                    </div>

                    <div className="about-stat">
                        <div className="about-stat-num">2</div>
                        <div className="about-stat-lbl">Exams supported</div>
                    </div>

                    <div className="about-stat">
                        <div className="about-stat-num">3</div>
                        <div className="about-stat-lbl">Chance categories</div>
                    </div>
                </div>

                {/* HOW SECTION */}
                <div className="about-section">
                    <h2>How the prediction works</h2>

                    <div className="about-steps">

                        <div className="about-step">
                            <div className="about-step-n">01</div>
                            <div>
                                <h3>You enter your rank</h3>
                                <p>Along with category, gender, and optionally your preferred branch or state.</p>
                            </div>
                        </div>

                        <div className="about-step">
                            <div className="about-step-n">02</div>
                            <div>
                                <h3>We query real cutoffs</h3>
                                <p>Your rank is compared against historical opening and closing ranks.</p>
                            </div>
                        </div>

                        <div className="about-step">
                            <div className="about-step-n">03</div>
                            <div>
                                <h3>Results are bucketed</h3>
                                <p>Safe, Moderate, Risky categories based on cutoff comparison.</p>
                            </div>
                        </div>

                    </div>
                </div>

                {/* TEAM */}
                <div className="about-section">
                    <h2>The team</h2>
                    <p className="about-team-note">
                        Built by engineering students who went through the JEE process and wanted a better tool.
                    </p>
                </div>

                {/* CTA */}
                <div className="about-cta">
                    <h2>Ready to find your colleges?</h2>

                    <button
                        className="about-cta-btn"
                        onClick={() => navigate("/rank")}
                    >
                        Start predicting →
                    </button>
                </div>

            </div>

            {/* FOOTER */}
            <div className="about-footer">
                <div className="about-logo">
                    Rank<span>Vision</span>
                </div>

                <div className="about-footer-links">
                    <a href="#">Privacy</a>
                    <a href="#">Terms</a>
                </div>
            </div>

        </div>
    );
};

export default About;