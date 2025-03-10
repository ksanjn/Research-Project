import React, { useState } from "react";
import "../styles/chatbot.css";

const AssessmentForm = ({ questions, onAnswerChange, onSubmit }) => {
  const [answers, setAnswers] = useState({});

  const handleInputChange = (question, answer) => {
    setAnswers((prev) => ({ ...prev, [question]: answer }));
    onAnswerChange(question, answer);
  };

  return (
    <div className="assessment-form-container">
      <h2 className="assessment-title">Skill Assessment</h2>
      {questions.map((q, index) => (
        <div key={index} className="assessment-question">
          <p className="question-text">{q}</p>
          <input
            type="text"
            className="assessment-input"
            placeholder="Type your answer..."
            value={answers[q] || ""}
            onChange={(e) => handleInputChange(q, e.target.value)}
          />
        </div>
      ))}
      <button className="submit-assessment-button" onClick={() => onSubmit(answers)}>Submit</button>
    </div>
  );
};

export default AssessmentForm;
