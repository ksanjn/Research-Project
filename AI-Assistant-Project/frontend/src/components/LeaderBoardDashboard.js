import React from "react";
import "../styles/chatbot.css";

const LeaderBoardDashboard = ({ leaderboardData }) => {
  return (
    <div className="dashboard-container">
      <h2 className="dashboard-title">Leaderboard</h2>
      <p className="dashboard-description">See how you rank among other learners.</p>
      <div className="leaderboard-list">
        {leaderboardData.length > 0 ? (
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {leaderboardData.map((user, index) => (
                <tr key={index} className={index === 0 ? "leaderboard-top" : "leaderboard-row"}>
                  <td>{index + 1}</td>
                  <td>{user.name}</td>
                  <td>{user.score}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="no-leaderboard">No leaderboard data available.</p>
        )}
      </div>
    </div>
  );
};

export default LeaderBoardDashboard;
