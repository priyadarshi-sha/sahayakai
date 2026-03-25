import React from "react";
import { PrismaClient } from "@prisma/client";
import { redirect } from "next/navigation";

import { v4 } from "uuid";
function generateActivationCodeWithUUID() {
  const uuid = v4();
  const code = uuid.replace(/-/g, "");
  return code.substring(0, 15);
}

const prisma = new PrismaClient();
const page = async () => {
  const emails = await prisma.users.findMany({
    select: {
      email: true,
    },
  });

  const memberships = await prisma.membership.findMany({
    select: {
      email: true,
      activation_code: true,
    },
  });

  const submitHandler = async (formData) => {
    "use server";
    const email = formData.get("email");
    const activationCode = generateActivationCodeWithUUID();
    const startDate = new Date();
    const endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + 30);
    const resp = await prisma.membership.create({
      data: {
        email: email,
        activation_code: activationCode,
        duration_days: 30,
        start_date: startDate,
        end_date: endDate,
      },
    });
    redirect("/admin/membership");
  };
  return (
    <div className="p-10 w-full justify-center">
      <h1 className="text-xl text-center font-bold mb-10">Membership Dashboard</h1>
      <div className="w-[90%] mx-auto flex flex-col justify-center items-center gap-5 bg-white/30 py-10">
        {emails.map((user, i) => (
          <div key={i} className="">
            <form action={submitHandler} className="flex gap-10 w-full">
              <input
                name="email"
                readOnly={true}
                className="w-96 p-2 bg-transparent border-2 rounded-xl border-gray-700"
                value={user.email}
              ></input>
              <input
                className="p-3"
                value={
                  memberships.filter((obj) => obj.email == user.email)[0]
                    ?.activation_code
                }
                readOnly = {true}
              ></input>
              <button type="submit" className="border-2 border-black p-2">
                generate activation code
              </button>
            </form>
          </div>
        ))}
      </div>
    </div>
  );
};

export default page;
