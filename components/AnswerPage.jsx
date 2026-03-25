'use client';

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useDispatch, useSelector } from 'react-redux';
import { addAnswer, showAnswer } from '@/provider/redux/Answer';
import { handleAsk } from '@/utils/handleAsk.js';
import ReactLoading from 'react-loading';
import Source from '@/components/ui/Sources';
import Skeleton from '@/components/ui/Skeleton';
import { useSession } from 'next-auth/react';
import YoutubeCard from '@/components/ui/YoutubeCard';
import MarkdownRenderer from '@/components/MarkdownRenderer';

const AnswerPage = ({ notebookId, notebookName }) => {
  const { status } = useSession();
  const dispatch = useDispatch();

  const [newNotebookName, setNewNotebookName] = useState(notebookName || "");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [retrieving, setRetrieving] = useState(false);
  const [hasRunOnce, setHasRunOnce] = useState(false);

  const answerList = useSelector((store) => store.qna.content);

  /* =========================
     Fetch Saved Questions
  ========================= */
  useEffect(() => {
    const fetchQuestions = async () => {
      if (status === "authenticated" && notebookId && !hasRunOnce) {
        try {
          setRetrieving(true);

          const res = await axios.get(
            `/api/questions?notebookId=${notebookId}`
          );

          const arr = res.data;

          if (arr.length !== 0) {
            arr.forEach((ques) => {
              dispatch(
                showAnswer({
                  notebookId: notebookId,
                  question: ques.question,
                  answer: ques.answer,
                  sources: ques.sources || [],
                  id: ques.question_id,
                  youtube: ques.youtube || [],
                })
              );
            });
          }

          setHasRunOnce(true);
        } catch (error) {
          console.error("Error fetching questions:", error);
        } finally {
          setRetrieving(false);
        }
      }
    };

    fetchQuestions();
  }, [status, notebookId, hasRunOnce, dispatch]);

  /* =========================
     Submit Question
  ========================= */
  const submitHandler = async (e) => {
    if (!question.trim()) return;

    e.preventDefault();

    let id = await dispatch(
      addAnswer({
        question: question,
        answer: "",
        notebookId: notebookId,
      })
    );

    id = id.payload;

    setLoading(true);
    const currentQuestion = question;
    setQuestion("");

    try {
      const resp = await handleAsk(currentQuestion);

      await dispatch(addAnswer({ ...resp, id }));

      if (status === "authenticated" && notebookId) {
        await axios.post("/api/uploadingAnswer", {
          id: id,
          question: resp.question,
          answer: resp.answer,
          sources: resp.sources,
          notebookId: notebookId,
          youtube: resp.youtube,
        });
      }
    } catch (error) {
      console.error("Submit error:", error);
    } finally {
      setLoading(false);
    }
  };

  /* =========================
     UI
  ========================= */
  return (
    <div className="answer-container">
      {retrieving && (
        <div className="h-screen w-full absolute z-[99] bg-gray-100 flex justify-center items-center flex-col">
          <img
            src="/loader.webp"
            alt="Loading"
            className="w-[250px]"
          />
          <h1 className="bold text-xl">
            Retrieving all questions..
          </h1>
        </div>
      )}

      <div className="answer-box flex flex-row justify-center">
        <div className="flex flex-col w-full">

          {/* Notebook Header */}
          <div className="flex justify-between py-7 px-5 relative z-10">
            <input
              className="p-2 bg-gray-200 outline-none border-2 rounded-lg"
              value={newNotebookName}
              onChange={(e) => setNewNotebookName(e.target.value)}
            />
          </div>

          {/* Questions */}
          <div className="w-4/5 md:w-3/5 mx-auto mt-16 pb-12 relative">
            {answerList
              .filter((ques) => ques.notebookId === notebookId)
              .map((el, index) => (
                <div key={el.id} className="mb-8">
                  <h3 className="font-semibold">
                    {index + 1}. {el.question}
                  </h3>

                  <div className="mt-2">
                    {el.answer && el.answer.length > 0 ? (
                      <MarkdownRenderer content={el.answer} />
                    ) : (
                      <Skeleton />
                    )}
                  </div>

                  {/* Sources */}
                  {el.sources && el.sources.length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-semibold">Sources</h4>
                      {el.sources.map((source, i) => (
                        <Source
                          key={i}
                          link={source.metadata?.source || ""}
                          filename={
                            source.metadata?.source?.split("\\").pop() ||
                            "Source"
                          }
                          pageNumber={source.metadata?.page}
                        />
                      ))}
                    </div>
                  )}

                  {/* YouTube Videos */}
                  {el.youtube && el.youtube.length > 0 && (
                    <div className="mt-4 flex gap-4 flex-wrap">
                      {el.youtube.map((vdo, i) => (
                        <YoutubeCard
                          key={i}
                          title={vdo.title}
                          id={vdo.videoId}
                          imgAddress={`https://img.youtube.com/vi/${vdo.videoId}/0.jpg`}
                          index={i}
                        />
                      ))}
                    </div>
                  )}
                </div>
              ))}
          </div>
        </div>

        {/* Input Section */}
        <div className="fixed bottom-8 w-10/12 md:w-3/5 m-auto flex items-center p-2 bg-white rounded-xl border">
          <input
            type="text"
            placeholder="Ask Follow Up...."
            className="flex-grow p-2 focus:outline-none"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                submitHandler(e);
              }
            }}
          />
          <button
            className="flex items-center justify-center text-white bg-black rounded-3xl px-4 py-2"
            onClick={submitHandler}
          >
            {loading ? (
              <ReactLoading
                type="spin"
                color="white"
                height="20px"
                width="20px"
              />
            ) : (
              "→"
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnswerPage;
