import React from "react";
import "../styles/chatbot.css";

const ProgressDashboard = ({ progressData }) => {
  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Progress Tracking</h2>
      <p className="dashboard-description">Monitor your skill improvement over time.</p>
      <div className="progress-list">
        {progressData.length > 0 ? (
          progressData.map((progress, index) => (
            <div key={index} className="progress-item">
              <p className="skill-name">{progress.skill}</p>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${progress.percentage}%` }}></div>
              </div>
              <p className="progress-percentage">{progress.percentage}% completed</p>
            </div>
          ))
        ) : (
          <p className="no-progress">No progress data available yet.</p>
        )}
      </div>
    </div>
  );
};

export default ProgressDashboard;


