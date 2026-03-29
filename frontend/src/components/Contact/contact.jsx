import React, { useState } from "react";
import "./Contact.css";
import { useNavigate } from "react-router-dom";

import ketanImg from "../../assets/ketan.jpeg";
import mayankImg from "../../assets/Mayank.jpeg";
import utkarshImg from "../../assets/utkarsh.jpeg";
import vaibhavImg from "../../assets/vaibhav.jpeg";

import { FaLinkedin, FaGithub, FaMoon, FaSun } from "react-icons/fa";
import { motion } from "framer-motion";

const team = [
  {
    name: "Ketan Arora",
    role: "Frontend Developer",
    desc: "Builds modern, responsive UI using React.",
    image: ketanImg,
    linkedin: "https://www.linkedin.com/in/ketan-arora-028961325/",
    github: "https://github.com/Its-Seeker",
  },
  {
    name: "Mayank Sharma",
    role: "Backend Developer",
    desc: "Handles APIs and server-side logic.",
    image: mayankImg,
    linkedin: "https://www.linkedin.com/in/mayank-sharma-028961325/",
    github: "https://github.com/BtkSkull",
  },
  {
    name: "Utkarsh",
    role: "Database Handler",
    desc: "Manages data and database optimization.",
    image: utkarshImg,
    linkedin: "https://www.linkedin.com/in/utkarsh-jagga-446303327/#",
    github: "https://github.com/UtkarshJagga",
  },
  {
    name: "Vaibhav",
    role: "ML Model Trainer",
    desc: "Develops and trains ML models.",
    image: vaibhavImg,
    linkedin: "https://www.linkedin.com/in/vaibhav-chaturvedi-5872a131b/",
    github: "https://github.com/Vaibhav-801",
  },
];

const Contact = () => {
  const [dark, setDark] = useState(false);
  const navigate = useNavigate(); // ✅ add this

  return (
    <div className={dark ? "contact-page dark" : "contact-page"}>

      {/* 🔥 NAVBAR ADDED */}
      <div className="contact-navbar">
        <div className="contact-container">
          <h2>Rank Vision</h2>

          <div className="contact-buttons">
            <button onClick={() => navigate("/about")}>About</button>
            <button onClick={() => navigate("/")}>Home</button>
          </div>
          <div className="toggle" onClick={() => setDark(!dark)}>
        {dark ? <FaSun /> : <FaMoon />}
      </div>

        </div>
      </div>

      {/* 🌙 DARK MODE */}
      {/* <div className="toggle" onClick={() => setDark(!dark)}>
        {dark ? <FaSun /> : <FaMoon />}
      </div> */}

      <h1>Meet Our Team</h1>
      <p className="subtitle">
        Building smart solutions for JEE & NEET aspirants.
      </p>

      <div className="team-container">
        {team.map((member, index) => (
          <motion.div
            className="team-card"
            key={index}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.2 }}
          >
            <img src={member.image} alt="profile" className="profile-img" />

            <h2>{member.name}</h2>
            <p className="role">{member.role}</p>
            <p className="desc">{member.desc}</p>

            <div className="links">
              <a href={member.linkedin} target="_blank" rel="noreferrer">
                <FaLinkedin /> LinkedIn
              </a>
              <a href={member.github} target="_blank" rel="noreferrer">
                <FaGithub /> GitHub
              </a>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default Contact;