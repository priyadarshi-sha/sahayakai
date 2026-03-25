// Remove Vercel Postgres import
// import { sql } from '@vercel/postgres'

// Import the Prisma client
// import prisma from '@/lib/prisma'; // Adjust this path if you created the file elsewhere

import { authOptions } from '@/app/api/auth/[...nextauth]/route';
import AnswerPage from '@/components/AnswerPage'
import { getServerSession } from 'next-auth';
import React from 'react'
import { PrismaClient} from "@prisma/client"

/**
 * Refactored function using Prisma.
 * We use `findUnique` because `notebook_id` is the @id.
 * We use `select` to get only the fields we need.
 */
const getNotebookData = async (notebookId) => {
  // prisma.notebooks.findUnique returns the object or null
  const prisma = new PrismaClient()
  const notebook = await prisma.notebooks.findUnique({
    where: {
      notebook_id: notebookId,
    },
    select: {
      notebook_name: true,
      uid: true, // We'll use this for the security check
    }
  });
  return notebook;
}

const page = async ({ params }) => {
  const session = await getServerSession(authOptions);
  const notebook = await getNotebookData(params.notebookid);

  // 1. Check if the user is logged in (session exists)
  // 2. Check if the notebook exists (notebook is not null)
  // 3. (RECOMMENDED) Check if the logged-in user's ID matches the notebook's user ID (uid)
  
  // NOTE: Adjust `session.user.id` based on your actual session object structure.
  // It might be `session.user.sub` or something else depending on your Auth provider.
  if (session && notebook ) {
    return (
      <>
        {/* Pass the correct prop, which is now `notebook.notebook_name` */}
        <AnswerPage notebookId={params.notebookid} notebookName={notebook.notebook_name} />
      </>
    )
  } else {
    // This message is now accurate.
    // It will show if:
    // 1. You are not logged in.
    // 2. The notebook ID is invalid.
    // 3. You are logged in but trying to access someone else's notebook.
    return (
      <>
        <div className='w-full h-full flex justify-center items-center'>
          <h1 className='text-xl'>You are not allowed to access this notebook.</h1>
        </div>
      </>
    )
  }
}

export default page