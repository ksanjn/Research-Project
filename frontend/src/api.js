const BASE_URL = "http://127.0.0.1:5000"; // Ensure backend is running on this URL

// Start Assessment: Get First Question
export const startAssessment = async (jobRole) => {
  try {
    const response = await fetch(`${BASE_URL}/start_assessment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_role: jobRole }),
    });

    if (!response.ok) {
      throw new Error("Error starting assessment");
    }

    return await response.json();
  } catch (error) {
    console.error("Error starting assessment:", error);
    return { message: "Failed to start assessment. Please try again." };
  }
};

// Submit Answer and Get Next Question
export const submitAnswer = async (jobRole, answer) => {
  try {
    const response = await fetch(`${BASE_URL}/submit_answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_role: jobRole, answer }),
    });

    if (!response.ok) {
      throw new Error("Error submitting answer");
    }

    return await response.json();
  } catch (error) {
    console.error("Error submitting answer:", error);
    return { message: "Failed to submit answer. Please try again." };
  }
};


export const getQuestions = async (jobRole) => {
  try {
    const response = await fetch(`${BASE_URL}/get_questions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_role: jobRole }),
    });

    if (!response.ok) {
      throw new Error("Error fetching questions");
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching questions:", error);
    return { message: "Failed to fetch questions. Please try again." };
  }
};

export const evaluateAnswers = async (jobRole, answers) => {
  try {
    const response = await fetch(`${BASE_URL}/evaluate_answers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_role: jobRole, answers }),
    });

    if (!response.ok) {
      throw new Error("Error evaluating answer");
    }

    return await response.json();
  } catch (error) {
    console.error("Error evaluating answer:", error);
    return { message: "Failed to evaluate answer. Please try again." };
  }
};

