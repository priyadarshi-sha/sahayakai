import axios from "axios";

export const handleAsk = async (question) => {
  try {
    const response = await axios.post("/api/questions", {
      question: question,
    });

    const data = response.data;

    console.log("handleAsk received:", data);

    return {
      question: data.question,
      answer: data.answer || "",
      sources: data.sources || [],
      youtube: data.youtube || [],
    };

  } catch (error) {
    console.error("handleAsk error:", error);
    throw error;
  }
};
