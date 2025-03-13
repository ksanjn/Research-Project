import React, { useState } from "react";
import { startAssessment, submitAnswer } from "../api";

const ChatBot = () => {
  const [jobRole, setJobRole] = useState("");
  const [question, setQuestion] = useState("");
  const [questionType, setQuestionType] = useState("");
  const [options, setOptions] = useState([]);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [totalQuestions, setTotalQuestions] = useState(0);
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const startQuiz = async () => {
    setLoading(true);
    try {
      const response = await startAssessment(jobRole);
      setQuestion(response.question);
      setQuestionType(response.question_type);
      setOptions(response.options || []);
      setQuestionIndex(response.index);
      setTotalQuestions(response.total_questions);
      setResults(null);
    } catch (error) {
      alert("Error starting assessment. Please try again.");
    }
    setLoading(false);
  };

  const handleSubmit = async () => {
    if (!answer.trim()) {
      alert("Please enter an answer before submitting.");
      return;
    }

    setLoading(true);
    try {
      const response = await submitAnswer(jobRole, answer);
      if (response.next_question) {
        setQuestion(response.next_question);
        setQuestionType(response.question_type);
        setOptions(response.options || []);
        setQuestionIndex(response.index);
        setAnswer("");
      } else {
        setResults({
          score: response.final_score,
          skill_level: response.skill_level,
          recommendation: response.recommendation,
        });
        setQuestion("");
      }
    } catch (error) {
      alert("Error submitting answer. Please try again.");
    }
    setLoading(false);
  };

  return (
    <div className="max-w-lg mx-auto p-8 bg-white shadow-2xl rounded-2xl mt-10 border border-gray-200">
      <h2 className="text-3xl font-extrabold text-center text-gray-800 mb-5">
        🎯 Skill Assessment
      </h2>

      {/* Input for Job Role */}
      <input
        type="text"
        className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
        placeholder="Enter Job Role..."
        value={jobRole}
        onChange={(e) => setJobRole(e.target.value)}
        disabled={question !== ""}
      />

      {/* Start Assessment Button */}
      <button
        className="w-full mt-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-semibold rounded-lg hover:shadow-md hover:from-blue-600 hover:to-blue-700 transition"
        onClick={startQuiz}
        disabled={loading || question !== ""}
      >
        {loading ? "Starting..." : "🚀 Start Assessment"}
      </button>

      {/* Display Question */}
      {question && (
        <div className="mt-6 p-5 bg-gray-50 rounded-xl shadow-md">
          <h3 className="text-lg font-semibold text-gray-800">
            Question {questionIndex + 1} of {totalQuestions}
          </h3>
          <p className="mt-2 text-gray-700">{question}</p>

          {/* MCQ Options */}
          {questionType === "mcq" && options.length > 0 && (
            <div className="mt-4 space-y-2">
              {options.map((opt, index) => (
                <label
                  key={index}
                  className={`block p-3 rounded-lg border cursor-pointer transition ${
                    answer === opt
                      ? "bg-blue-500 text-white border-blue-600"
                      : "border-gray-300 hover:bg-gray-100"
                  }`}
                >
                  <input
                    type="radio"
                    name="mcq"
                    value={opt}
                    onChange={(e) => setAnswer(e.target.value)}
                    className="hidden"
                  />
                  {opt}
                </label>
              ))}
            </div>
          )}

          {/* Coding Input */}
          {questionType === "coding" && (
            <textarea
              className="w-full p-3 border border-gray-300 rounded-lg font-mono bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              placeholder="Write your code here..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              rows={6}
            />
          )}

          {/* Open-Ended Input */}
          {questionType === "open-ended" && (
            <textarea
              className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
              placeholder="Write your answer here..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              rows={4}
            />
          )}

          {/* Submit Answer Button */}
          <button
            className="w-full mt-4 py-3 bg-green-500 text-white font-semibold rounded-lg hover:shadow-md hover:bg-green-600 transition"
            onClick={handleSubmit}
            disabled={loading || answer.trim() === ""}
          >
            {loading ? "Submitting..." : "Submit Answer"}
          </button>
        </div>
      )}

      {/* Show Final Results */}
      {results && (
        <div className="mt-6 p-5 bg-green-50 border border-green-400 text-green-700 rounded-xl shadow-md">
          <h3 className="text-xl font-bold">🎉 Assessment Completed!</h3>
          <p>
            <strong>🏆 Score:</strong> {results.score}%
          </p>
          <p>
            <strong>📊 Skill Level:</strong> {results.skill_level}
          </p>
          <p>
            <strong>🔍 Recommendation:</strong> {results.recommendation}
          </p>

          {/* Learning Pathway Button */}
          <button
            className="w-full mt-4 py-3 bg-purple-500 text-white font-semibold rounded-lg hover:shadow-md hover:bg-purple-600 transition"
            onClick={() => alert("Learning Pathway coming soon!")} // Placeholder action
          >
            📚 Learning Pathway
          </button>
          
        </div>
      )}

      

    </div>
  );
};

export default ChatBot;