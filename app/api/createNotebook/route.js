import { nanoid } from "@reduxjs/toolkit";
import { NextResponse } from "next/server";
import { PrismaClient } from "@prisma/client";
import { getServerSession } from "next-auth";
import { authOptions } from "../auth/[...nextauth]/route";

export async function POST(req) {
  const prisma = new PrismaClient();

  const session = await getServerSession(authOptions);

  if (!session) {
    return NextResponse.json({ message: "Unauthorized" }, { status: 401 });
  }

  const request = await req.json();
  const userUid = session.user.uid;

  try {
    const checkIfNotebook = await prisma.notebooks.findMany({
      where: {
        uid: userUid,
        notebook_name: request.notebookName
      }
    });

    if (checkIfNotebook.length === 0) {
      const resp = await prisma.notebooks.create({
        data: {
          notebook_id: nanoid(),
          notebook_name: request.notebookName,
          users: {
            connect: {
              uid: userUid
            }
          }
        }
      });

      return NextResponse.json({
        message: "success",
        id: resp.notebook_id
      });
    } else {
      return NextResponse.json({ message: "failed" });
    }

  } catch (error) {
    console.log(error);
    return NextResponse.json({ message: "failed" });
  }
}
