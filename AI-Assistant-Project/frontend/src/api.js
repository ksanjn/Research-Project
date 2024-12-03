const BASE_URL = "http://127.0.0.1:5000";

export const getQuestions = async (jobRole) => {
  const response = await fetch(`${BASE_URL}/get_questions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_role: jobRole }),
  });
  return response.json();
};

export const evaluateAnswers = async (jobRole, answers) => {
  const response = await fetch(`${BASE_URL}/evaluate_answers`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ job_role: jobRole, answers }),
  });
  return response.json();
};
