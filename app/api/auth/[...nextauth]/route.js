import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
  ],

  session: {
    strategy: "jwt",
  },

  pages: {
    signIn: "/signin",
    error: "/signin",
  },

  callbacks: {
    async signIn({ user, account }) {
      if (!user?.email) return false;

      const existingUser = await prisma.users.findUnique({
        where: { email: user.email },
      });

      if (!existingUser) {
        await prisma.users.create({
          data: {
            uid: account.providerAccountId,   // ✅ always available
            email: user.email,
            name: user.name ?? "",
            phone: null,
            usn: null,
          },
        });
      }

      return true;
    },

    async session({ session }) {
      if (session.user?.email) {
        const dbUser = await prisma.users.findUnique({
          where: { email: session.user.email },
        });

        if (dbUser) {
          session.user.uid = dbUser.uid;   // ✅ VERY IMPORTANT
        }
      }

      return session;
    },
  },
};

const handler = NextAuth(authOptions);

export { handler as GET, handler as POST };
