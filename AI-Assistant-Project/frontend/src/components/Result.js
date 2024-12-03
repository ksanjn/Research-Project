import React from "react";

const Results = ({ results }) => {
  return (
    <div className="mt-6 p-4 border rounded">
      <h2 className="text-xl font-semibold">Results</h2>
      <p><strong>Score:</strong> {results.score}%</p>
      <p><strong>Skill Level:</strong> {results.skill_level}</p>
      <p><strong>Recommendation:</strong> {results.recommendation}</p>
    </div>
  );
};

export default Results;
