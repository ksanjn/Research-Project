import React, { useState } from "react";
import "../styles/chatbot.css";

const Quiz = ({ questions, onSubmit }) => {
  const [answers, setAnswers] = useState({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const handleAnswerChange = (question, answer) => {
    setAnswers((prev) => ({ ...prev, [question]: answer }));
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const prevQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const submitQuiz = () => {
    onSubmit(answers);
  };

  return (
    <div className="quiz-container">
      <h2 className="quiz-title">Question {currentQuestionIndex + 1} of {questions.length}</h2>
      <p className="quiz-question">{questions[currentQuestionIndex]}</p>
      <input
        type="text"
        className="quiz-input"
        placeholder="Type your answer..."
        value={answers[questions[currentQuestionIndex]] || ""}
        onChange={(e) => handleAnswerChange(questions[currentQuestionIndex], e.target.value)}
      />
      <div className="quiz-navigation">
        <button className="quiz-button" onClick={prevQuestion} disabled={currentQuestionIndex === 0}>Back</button>
        {currentQuestionIndex < questions.length - 1 ? (
          <button className="quiz-button" onClick={nextQuestion}>Next</button>
        ) : (
          <button className="quiz-button submit" onClick={submitQuiz}>Submit</button>
        )}
      </div>
    </div>
  );
};

export default Quiz;
