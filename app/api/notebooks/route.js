import { PrismaClient } from "@prisma/client";
import { getServerSession } from "next-auth";
import { authOptions } from "../auth/[...nextauth]/route";
import { NextResponse } from "next/server";

export async function GET() {
  const prisma = new PrismaClient();
  const session = await getServerSession(authOptions);

  if (!session) {
    return NextResponse.json([], { status: 401 });
  }

  const notebooks = await prisma.notebooks.findMany({
    where: {
      uid: session.user.uid
    }
  });

  return NextResponse.json(notebooks);
}
