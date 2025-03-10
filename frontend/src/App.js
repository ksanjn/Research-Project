import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import ChatBot from "./components/ChatBot";
import Quiz from "./components/Quiz";
import Result from "./components/Result";
import AssessmentForm from "./components/AssessmentForm";
import SkillGapAnalysisDashboard from "./components/SkillGapAnalysisDashboard";
import ProgressDashboard from "./components/ProgressDashboard";
import LeaderBoardDashboard from "./components/LeaderBoardDashboard";
import "./styles/chatbot.css";

const App = () => {
  return (
    <Router>
      <div className="app-container">
        <nav className="navbar">
          <ul>
            <li><Link to="/"></Link></li>
            {/* <li><Link to="/quiz">Quiz</Link></li>
            <li><Link to="/assessment">Assessment</Link></li>
            <li><Link to="/skill-gap">Skill Gap</Link></li>
            <li><Link to="/progress">Progress</Link></li>
            <li><Link to="/leaderboard">Leaderboard</Link></li> */}
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<ChatBot />} />
          {/* <Route path="/quiz" element={<Quiz />} />
          <Route path="/assessment" element={<AssessmentForm />} />
          <Route path="/skill-gap" element={<SkillGapAnalysisDashboard skillGaps={[]} />} />
          <Route path="/progress" element={<ProgressDashboard progressData={[]} />} />
          <Route path="/leaderboard" element={<LeaderBoardDashboard leaderboardData={[]} />} /> */}
        </Routes>
      </div>
    </Router>
  );
};

export default App;
