import React from "react";
import "../styles/chatbot.css";

const SkillGapAnalysisDashboard = ({ skillGaps }) => {
  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Skill Gap Analysis</h2>
      <p className="dashboard-description">Identify areas where improvement is needed.</p>
      <div className="skill-gap-list">
        {skillGaps.length > 0 ? (
          skillGaps.map((gap, index) => (
            <div key={index} className="skill-gap-item">
              <p className="skill-name">{gap.skill}</p>
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${gap.percentage}%` }}></div>
              </div>
              <p className="skill-percentage">{gap.percentage}% proficiency</p>
            </div>
          ))
        ) : (
          <p className="no-skill-gap">No significant skill gaps detected.</p>
        )}
      </div>
    </div>
  );
};

export default SkillGapAnalysisDashboard;