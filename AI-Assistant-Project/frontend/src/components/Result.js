import React from "react";
import "../styles/chatbot.css";

const Results = ({ results }) => {
  return (
    <div className="results-container">
      <h2 className="results-title">Skill Assessment Results</h2>
      <div className="results-content">
        <p className="results-text">Your Skill Level: <span className="skill-level">{results.predicted_skill_level}</span></p>
        <div className="progress-bar-container">
          <div className={`progress-bar level-${results.predicted_skill_level.toLowerCase()}`}></div>
        </div>
        <p className="improvement-tips">{results.improvement_tips}</p>
      </div>
      <button className="retry-button" onClick={() => window.location.reload()}>Try Again</button>
    </div>
  );
};

export default Results;
