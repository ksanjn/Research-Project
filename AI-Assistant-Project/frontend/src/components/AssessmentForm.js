import React from "react";

const AssessmentForm = ({ questions, onAnswerChange, onSubmit }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">Assessment Questions</h2>
      {questions.map((question, index) => (
        <div key={index} className="mb-4">
          <p>{question}</p>
          <input
            type="text"
            className="border p-2 w-full"
            placeholder="Your Answer"
            onChange={(e) => onAnswerChange(`Q${index + 1}`, e.target.value)}
          />
        </div>
      ))}
      <button className="bg-green-500 text-white p-2 mt-4" onClick={onSubmit}>
        Submit Answers
      </button>
    </div>
  );
};

export default AssessmentForm;
