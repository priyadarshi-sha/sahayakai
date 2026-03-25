'use client'
import React, { useState } from 'react';
import Link from 'next/link'
import { Textarea } from "@/components/ui/textarea"
import { useRouter } from 'next/navigation'
import Image from 'next/image';
import logo from '@/public/logo_vtu-gpt.png'
import { useSession } from 'next-auth/react';
import axios from 'axios';
const InputHome = ({ onAsk }) => {
  const router = useRouter();
  const session = useSession();
  const [question, setQuestion] = useState('');

  const handleAsk = async () => {
    if (session.status == 'unauthenticated') {
      router.push('/signin')
      return;
    }
    if (question.trim().length != 0) {
      const name = "notebook-" + Math.floor(Math.random() * 100000);
      const resp = await axios.post('/api/createNotebook', {
        
        notebookName: name
      })
      if(resp.data.message == 'success'){
        onAsk(question,resp.data.id);
        router.push(`/answer/${resp.data.id}`);
      }
    }
  }
  return (
    <>
      <div className='w-full border-3 border-gray-900'>
        <div className='homepage-main'>
          <div className="bg-image"></div>
          <Image className='logo absolute top-5 md:hidden' src={logo}></Image>
          <h1 className="mb-4">Where Knowledge begins</h1>
          <div className='text-area-div'>
            <Textarea
              placeholder='Ask a Question...'
              className='resize-none text-area bg-transparent text-black'
              style={{ fontSize: '16px', backgroundColor: 'white', marginBottom: 10, borderRadius: 20, padding: 20, outline: 0 }}  // Adjust the font size as needed
              onKeyDown={(e) => {
                if (e.key === "Enter") handleAsk()
              }}
              onChange={(e) => setQuestion(e.target.value)}
            />

            <Link href=''><button className='ask-btn' onClick={(e) => {
              e.preventDefault();
              handleAsk()
            }}><i className="ri-arrow-right-line text-white" ></i></button></Link>
          </div>
           
        </div>
      </div>
    </>


  )
}

export { InputHome };