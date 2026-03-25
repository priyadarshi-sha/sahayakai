"use client";

import React, { useState, useEffect } from "react";
import { InputHome } from "@/components/InputHome";
import { useToast } from "@/components/ui/use-toast";
import { addAnswer } from "@/provider/redux/Answer";
import { useDispatch } from "react-redux";
import ReactLoading from "react-loading";
import Sidebar from "@/components/Sidebar";

const Home = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { toast } = useToast();
  const dispatch = useDispatch();

  useEffect(() => {
    if (error) {
      toast({
        title: "Error",
        description: error,
        duration: 5000,
      });
    }
  }, [error, toast]);

  const handleAsk = async (question, notebookId) => {
    if (!question?.trim()) return;

    setLoading(true);

    let id = await dispatch(
      addAnswer({
        question: question,
        answer: "",
        notebookId: notebookId,
      })
    );

    id = id.payload;

    try {
      const response = await fetch("/api/questions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      console.log("Frontend received:", data);

      if (response.ok) {
        dispatch(
          addAnswer({
            question: question,
            answer: data.answer,
            sources: data.sources,
            id: id,
            youtube: data.youtube,
          })
        );
      } else {
        setError(data.error || "Failed to get answer.");
      }
    } catch (err) {
      console.error(err);
      setError("Unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full flex items-center justify-center">
      <Sidebar />

      <div className="w-full h-full flex justify-center relative items-center">
        <InputHome onAsk={handleAsk} />

        {loading && (
          <div className="h-full w-full absolute top-0 flex justify-center items-center bg-zinc-200 left-0">
            <ReactLoading
              type="spin"
              color="#13343B"
              height={"50px"}
              width={"70px"}
            />
          </div>
        )}
      </div>

      <div className="help-btn">
        <i className="ri-question-fill"></i>
      </div>
    </div>
  );
};

export default Home;
