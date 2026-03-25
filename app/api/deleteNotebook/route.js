import { NextResponse } from "next/server";
// Import the Prisma client
import prisma from '@/lib/prisma'; // Make sure this path is correct

export async function POST(req, res) {
  try {
    const request = await req.json();

    // Replaced sql`delete` with prisma.notebooks.delete
    await prisma.notebooks.delete({
      where: {
        notebook_id: request.notebookId,
      }
    });

    return NextResponse.json({ message: "success" });

  } catch (error) {
    // Prisma's .delete() will throw an error if the record is not found.
    // We catch it here to return a more specific message.
    if (error.code === 'P2025') { 
      return NextResponse.json(
        { message: "Error: Notebook not found." },
        { status: 404 }
      );
    }

    // General server error
    return NextResponse.json(
      { message: "An error occurred." },
      { status: 500 }
    );
  }
}