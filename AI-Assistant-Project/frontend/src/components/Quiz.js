import React, { useState } from "react";

const Quiz = ({ quizQuestions, setAnswers, submitQuiz }) => {
  const [localAnswers, setLocalAnswers] = useState({});

  const handleChange = (e, idx) => {
    setLocalAnswers({ ...localAnswers, [`Q${idx + 1}`]: e.target.value });
  };

  const handleSubmit = () => {
    setAnswers(localAnswers); // Set answers in parent component
    submitQuiz(); // Submit the quiz
  };

  return (
    <div className="mt-4">
      <h2 className="text-lg font-bold mb-2">Quiz</h2>
      {quizQuestions.map((q, idx) => (
        <div key={idx} className="mb-2">
          <p>{q}</p>
          <input
            type="text"
            placeholder="Your answer"
            className="border p-2 w-full"
            onChange={(e) => handleChange(e, idx)}
          />
        </div>
      ))}
      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white p-2 rounded mt-2"
      >
        Submit Quiz
      </button>
    </div>
  );
};

export default Quiz;
