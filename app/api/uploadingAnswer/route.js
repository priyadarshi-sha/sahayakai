import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";
import { getServerSession } from "next-auth";
import { authOptions } from "../auth/[...nextauth]/route";

const prisma = new PrismaClient();

export async function POST(req) {
  try {
    const session = await getServerSession(authOptions);

    if (!session || !session.user?.uid) {
      return NextResponse.json(
        { error: "Unauthorized" },
        { status: 401 }
      );
    }

    const body = await req.json();

    await prisma.questions.create({
      data: {
        question_id: body.id,
        question: body.question,
        answer: body.answer,
        sources: JSON.stringify(body.sources || []),
        youtube: JSON.stringify(body.youtube || []),
        notebook_id: body.notebookId,
        user_id: session.user.uid, // ✅ ALWAYS from session
      },
    });

    return NextResponse.json({ message: "Saved successfully" });

  } catch (error) {
    console.error("Upload error:", error);
    return NextResponse.json(
      { error: "Database error" },
      { status: 500 }
    );
  }
}
