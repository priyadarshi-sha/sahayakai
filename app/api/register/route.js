import { PrismaClient } from "@prisma/client";
import { NextResponse } from "next/server";

const prisma = new PrismaClient();

export async function POST(req) {
  try {
    const body = await req.json();
    const { email, name, phone, usn } = body;

    if (!email || !name || !phone || !usn) {
      return NextResponse.json(
        { message: "All fields are required" },
        { status: 400 }
      );
    }

    const user = await prisma.users.create({
      data: {
        email,
        name,
        phone,
        usn,
      },
    });

    return NextResponse.json(
      { message: "User registered successfully", user },
      { status: 201 }
    );

  } catch (error) {
    // ✅ HANDLE DUPLICATE USN / EMAIL
    if (error.code === "P2002") {
      return NextResponse.json(
        { message: "User with this USN already exists" },
        { status: 409 }
      );
    }

    console.error("Register error:", error);

    return NextResponse.json(
      { message: "Internal server error" },
      { status: 500 }
    );
  }
}
