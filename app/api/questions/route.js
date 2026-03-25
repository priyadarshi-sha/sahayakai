import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";
import { getServerSession } from "next-auth";
import { authOptions } from "../auth/[...nextauth]/route";

const prisma = new PrismaClient();

/* =========================
   GET → Fetch saved questions
========================= */
export async function GET(req) {
  try {
    const session = await getServerSession(authOptions);

    if (!session) {
      return NextResponse.json([], { status: 401 });
    }

    const { searchParams } = new URL(req.url);
    const notebookId = searchParams.get("notebookId");

    if (!notebookId) {
      return NextResponse.json([], { status: 400 });
    }

    const questions = await prisma.questions.findMany({
      where: {
        notebook_id: notebookId,
        user_id: session.user.uid,
      },
      orderBy: {
        time_created: "asc",
      },
    });

    return NextResponse.json(questions);
  } catch (error) {
    console.error("GET /api/questions error:", error);
    return NextResponse.json([], { status: 500 });
  }
}

/* =========================
   POST → Ask FastAPI
========================= */
export async function POST(req) {
  try {
    const session = await getServerSession(authOptions);

    if (!session) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    const body = await req.json();
    const { question } = body;

    if (!question) {
      return NextResponse.json(
        { error: "Question required" },
        { status: 400 }
      );
    }

    const response = await fetch(
      "http://127.0.0.1:8000/api/chat/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: session.user.uid,
          question: question,
        }),
      }
    );

    const data = await response.json();
    console.log("FastAPI returned:", data);

    return NextResponse.json({
      question: question,
      answer: data.answer ?? data.result ?? "",
      sources:
        data.sources ??
        data.source_documents ??
        [],
      youtube:
        data.youtube ??
        data.youtube_videos ??
        data.videos ??
        [],
    });
  } catch (error) {
    console.error("POST /api/questions error:", error);
    return NextResponse.json(
      { error: "Backend error" },
      { status: 500 }
    );
  }
}
