import React, { useState } from "react";
import { startAssessment, submitAnswer } from "../api";

const ChatBot = () => {
  const [jobRole, setJobRole] = useState(""); // Store user input for job role
  const [question, setQuestion] = useState(""); // Current question
  const [questionType, setQuestionType] = useState(""); // Question Type (MCQ, Coding, Open-Ended)
  const [options, setOptions] = useState([]); // Options for MCQ
  const [questionIndex, setQuestionIndex] = useState(0); // Track current question
  const [totalQuestions, setTotalQuestions] = useState(0); // Total questions
  const [answers, setAnswers] = useState({}); // Store all answers
  const [answer, setAnswer] = useState(""); // Store current answer
  const [results, setResults] = useState(null); // Store final results
  const [loading, setLoading] = useState(false); // Track API loading state

  // Start assessment and get first question
  const startQuiz = async () => {
    setLoading(true);
    try {
      const response = await startAssessment(jobRole);
      setQuestion(response.question);
      setQuestionType(response.question_type);
      setOptions(response.options || []);
      setQuestionIndex(response.index);
      setTotalQuestions(response.total_questions);
      setAnswers({}); // Reset previous answers
      setResults(null); // Clear previous results
    } catch (error) {
      alert("Error starting assessment. Please try again.");
    }
    setLoading(false);
  };

  // Submit current answer and get next question
  const handleSubmit = async () => {
    if (!answer.trim()) {
      alert("Please enter an answer before submitting.");
      return;
    }

    setLoading(true);
    try {
      // Store the current answer in the answers object
      setAnswers((prev) => ({ ...prev, [question]: answer }));

      // Send answer to backend
      const response = await submitAnswer(jobRole, answer);

      if (response.next_question) {
        // Continue to next question
        setQuestion(response.next_question);
        setQuestionType(response.question_type);
        setOptions(response.options || []);
        setQuestionIndex(response.index);
        setAnswer(""); // Clear input for new answer
      } else {
        // All questions answered → Show final score & recommendations
        setResults({
          score: response.final_score,
          skill_level: response.skill_level,
          recommendation: response.recommendation,
        });
        setQuestion(""); // Remove current question from UI
      }
    } catch (error) {
      alert("Error submitting answer. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-10">
      <h2 className="text-2xl font-bold text-center mb-4">
        Skill Assessment Chatbot
      </h2>

      {/* Input for Job Role */}
      <input
        type="text"
        className="w-full p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300"
        placeholder="Enter Job Role..."
        value={jobRole}
        onChange={(e) => setJobRole(e.target.value)}
        disabled={question !== ""}
      />

      {/* Start Assessment Button */}
      <button
        className="w-full mt-3 p-2 bg-blue-500 text-white font-bold rounded-md hover:bg-blue-600"
        onClick={startQuiz}
        disabled={loading || question !== ""}
      >
        {loading ? "Starting..." : "Start Assessment"}
      </button>

      {/* Display Question */}
      {question && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold">
            Question {questionIndex + 1} of {totalQuestions}
          </h3>
          <p className="font-medium">{question}</p>

          {/* Render MCQ Options */}
          {questionType === "mcq" && options.length > 0 && (
            <div className="mt-2">
              {options.map((opt, index) => (
                <label key={index} className="block p-2 border rounded-md cursor-pointer">
                  <input
                    type="radio"
                    name="mcq"
                    value={opt}
                    onChange={(e) => setAnswer(e.target.value)}
                    className="mr-2"
                  />
                  {opt}
                </label>
              ))}
            </div>
          )}

          {/* Render Coding Input (Large Text Area) */}
          {questionType === "coding" && (
            <textarea
              className="w-full p-2 border rounded-md font-mono"
              placeholder="Write your code here..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              rows={6}
            />
          )}

          {/* Render Open-Ended (Short Answer) */}
          {questionType === "open-ended" && (
            <textarea
              className="w-full p-2 border rounded-md"
              placeholder="Write your answer here..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              rows={6}
            />
          )}

          {/* Submit Answer Button */}
          <button
            className="w-full mt-3 p-2 bg-green-500 text-white font-bold rounded-md hover:bg-green-600"
            onClick={handleSubmit}
            disabled={loading || answer.trim() === ""}
          >
            {loading ? "Submitting..." : "Submit Answer"}
          </button>
        </div>
      )}

      {/* Show Final Results */}
      {results && (
        <div className="mt-4 p-3 bg-green-100 border border-green-500 text-green-700 rounded">
          <strong>Score:</strong> {results.score}% <br />
          <strong>Skill Level:</strong> {results.skill_level} <br />
          <strong>Recommendation:</strong> {results.recommendation}
        </div>
      )}
    </div>
  );
};

export default ChatBot;