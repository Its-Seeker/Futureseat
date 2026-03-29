import React, { useState } from "react";
import './rank.css';
import { useNavigate } from "react-router-dom";
import { FaShieldAlt, FaTrophy, FaStar, FaLinkedin, FaEnvelope, FaTwitter } from "react-icons/fa";

const Rank = () => {
    const navigate = useNavigate();

    const [examType, setExamType] = useState("btech");
    const [rank, setRank] = useState("");
    const [category, setCategory] = useState("GEN");
    const [gender, setGender] = useState("Male");
    const [special, setSpecial] = useState("None");

    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleAnalyze = async () => {
        if (!rank) return alert("Please enter your rank");

        setLoading(true);
        setError(null);

        try {
            let url = `http://127.0.0.1:8000/api/v1/predict/${examType}?rank=${rank}`;

            if (examType === "btech") {
                url += `&category=${category}&gender=${gender}`;
                if (special !== "None") {
                    url += `&special=${special}`;
                }
            }

            const response = await fetch(url);
            if (!response.ok) throw new Error("Failed to fetch data from the server.");

            const data = await response.json();
            setResults(data);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="rank-page">
            <div className="rank-navbar">
                <div className="rank-container">
                    <h2>Rank Vision</h2>

                    <div className="rank-buttons">
                        <button onClick={() => navigate("/about")}>About</button>
                        <button onClick={() => navigate("/")}>Home</button>
                    </div>
                </div>


            </div>

            <div className="rank-hero-section">
                <div className="rank-container rank-hero">

                    <div className="rank-hero-left">
                        <h1>From <span>Rank</span> to Reality</h1>
                        <p>Understand your chances and plan your college strategy smarter</p>

                        <div className="rank-form-box">
                            <div className="rank-input-group">
                                <label>Exam Type</label>
                                <select value={examType} onChange={(e) => setExamType(e.target.value)}>
                                    <option value="Prefrences">Exam Options</option>
                                    <option value="btech">JEE Main (B.Tech)</option>
                                    <option value="neet">NEET</option>
                                </select>
                            </div>

                            <div className="rank-input-group">
                                <label>Your Rank</label>
                                <input
                                    type="number"
                                    placeholder="e.g. 20000"
                                    value={rank}
                                    onChange={(e) => setRank(e.target.value)}
                                />
                            </div>

                            {examType === "btech" && (
                                <>
                                    <div className="rank-input-group">
                                        <label>Category</label>
                                        <select value={category} onChange={(e) => setCategory(e.target.value)}>
                                            <option value="GEN">General</option>
                                            <option value="OBC">OBC</option>
                                            <option value="SC">SC</option>
                                            <option value="ST">ST</option>
                                            <option value="EWS">EWS</option>
                                        </select>
                                    </div>

                                    <div className="rank-input-group">
                                        <label>Gender</label>
                                        <select value={gender} onChange={(e) => setGender(e.target.value)}>
                                            <option value="Male">Male</option>
                                            <option value="Female">Female</option>
                                        </select>
                                    </div>

                                    <div className="rank-input-group">
                                        <label>Special Quota</label>
                                        <select value={special} onChange={(e) => setSpecial(e.target.value)}>
                                            <option value="None">None</option>
                                            <option value="PwD">PwD</option>
                                            <option value="Sports">Sports</option>
                                            <option value="CW">CW (Defence)</option>
                                        </select>
                                    </div>

                                </>
                            )}

                            <button onClick={handleAnalyze} disabled={loading}>
                                {loading ? "Analyzing..." : "Analyze Colleges"}
                            </button>

                            {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
                        </div>
                    </div>

                    <div className="rank-hero-right">
                        {results ? (
                            <div className="results-container" style={{ backgroundColor: "white", padding: "20px", borderRadius: "10px", color: "black", maxHeight: "400px", overflowY: "auto" }}>

                                {results.safe?.length > 0 && (
                                    <>
                                        <h4>🟢 Safe Choices</h4>
                                        <ul>
                                            {results.safe.slice(0, 10).map((r, i) => (
                                                <li key={i}><strong>{r.college}</strong> - {r.course}</li>
                                            ))}
                                        </ul>
                                    </>
                                )}

                                {results.moderate?.length > 0 && (
                                    <>
                                        <h4 style={{ marginTop: "15px" }}>🟡 Moderate Choices</h4>
                                        <ul>
                                            {results.moderate.slice(0, 10).map((r, i) => (
                                                <li key={i}><strong>{r.college}</strong> - {r.course}</li>
                                            ))}
                                        </ul>
                                    </>
                                )}

                                {results.risky?.length > 0 && (
                                    <>
                                        <h4 style={{ marginTop: "15px" }}>🔴 Risky Choices</h4>
                                        <ul>
                                            {results.risky.slice(0, 10).map((r, i) => (
                                                <li key={i}><strong>{r.college}</strong> - {r.course}</li>
                                            ))}
                                        </ul>
                                    </>
                                )}

                                {results.count === 0 && (
                                    <p style={{ textAlign: "center", color: "#666" }}>No colleges found for this rank. Try a higher rank or different filters.</p>
                                )}
                            </div>
                        ) : (
                            <div className="graph-placeholder">Results will appear here</div>
                        )}
                    </div>

                </div>
            </div>

            {/* HOW */}
            <div className="rank-how-section">
                <div className="rank-container">
                    <h2>How it works ?</h2>
                    <div className="rank-steps">
                        <div className="rank-step"><div className="rank-circle">1</div><p>Enter details like Rank, Category, etc.</p></div>
                        <div className="rank-step"><div className="rank-circle">2</div><p>Get college predictions instantly.</p></div>
                        <div className="rank-step"><div className="rank-circle">3</div><p>Explore your college options.</p></div>
                    </div>
                </div>
            </div>

            {/* CATEGORY */}
            <div className="rank-category-section">
                <div className="rank-container">
                    <h2>College Categories</h2>
                    <div className="rank-card green"><FaShieldAlt className="card-icon green-icon" /><div><h3>Safe</h3><p>High Chance</p></div></div>
                    <div className="rank-card yellow"><FaTrophy className="card-icon yellow-icon" /><div><h3>Competitive</h3><p>Realistic Target</p></div></div>
                    <div className="rank-card red"><FaStar className="card-icon red-icon" /><div><h3>Aspirational</h3><p>Ambitious</p></div></div>
                </div>
            </div>

            {/* FOOTER */}
            <div className="rank-footer">
                <div className="rank-container footer-content">
                    <div><button
                        className="contact-switch"
                        onClick={() => navigate("/contact")}>
                        Contact
                    </button><p><FaLinkedin /> Linkedin</p><p><FaEnvelope /> Mail</p><p><FaTwitter /> Twitter</p></div>
                    <div><h4>Legal</h4><p>Privacy Policy</p><p>Terms</p></div>
                </div>
            </div>

        </div>
    );
};

export default Rank;