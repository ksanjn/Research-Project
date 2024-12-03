import React, { useState } from "react";
import { getQuestions, evaluateAnswers } from "../api";
import AssessmentForm from "./AssessmentForm";
import Results from "./Result";
import "../styles/chatbot.css"
const ChatBot = () => {
  const [jobRole, setJobRole] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState(null);

  const fetchQuestions = async () => {
    try {
      const response = await getQuestions(jobRole);
      setQuestions(response.questions);
      setResults(null); // Reset results if fetching new questions
    } catch (error) {
      alert("Error fetching questions. Please try again.");
    }
  };

  const handleAnswerChange = (question, answer) => {
    setAnswers((prev) => ({ ...prev, [question]: answer }));
  };

  const submitAnswers = async () => {
    try {
      const response = await evaluateAnswers(jobRole, answers);
      setResults(response);
    } catch (error) {
      alert("Error submitting answers. Please try again.");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Job Role Skill Assessment</h1>
      
      <div className="mb-4">
        <input
          type="text"
          className="border p-2 w-full"
          placeholder="Enter Job Role (e.g., Data Scientist)"
          value={jobRole}
          onChange={(e) => setJobRole(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white p-2 mt-2"
          onClick={fetchQuestions}
        >
          Get Questions
        </button>
      </div>

      {questions.length > 0 && (
        <AssessmentForm
          questions={questions}
          onAnswerChange={handleAnswerChange}
          onSubmit={submitAnswers}
        />
      )}

      {results && <Results results={results} />}
    </div>
  );
};

export default ChatBot;
