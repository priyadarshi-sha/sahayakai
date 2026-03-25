import Postsignin from '@/components/Postsignin'
import React from 'react'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/app/api/auth/[...nextauth]/route'
import { PrismaClient } from '@prisma/client'
import { redirect } from 'next/navigation'



const page = async () => {
  const session = await getServerSession(authOptions)
  const prisma = new PrismaClient();
  const resp = await prisma.users.findMany({
    where : {
      email : session.user.email
    }
  })
  if(resp.length > 0){
    redirect('/')
  }else{
    return (
      <Postsignin/>
    )
  }
  
}

export default page