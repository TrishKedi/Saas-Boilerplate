"use client"

import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";

export default function Home() {
  const router = useRouter()

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-500 to-purple-600 text-white">
      <motion.h1
        className="text-5xl font-bold"
        initial={{opacity:0, y: -50}}
        animate={{opacity: 1, y: 0}}
        transition={{duration: 1}}
      >
        Patricia's AI Powered Saas Platform

      </motion.h1>

      <motion.p
        className="mt-4 text-lg"
        initial={{opacity:0, y: 20}}
        animate={{opacity: 1, y: 0}}
        transition={{delay: 0.5, duration: 1}}
      >
        AI-driven solutions to boost productivity and efficiency.

      </motion.p>
      
      <motion.div
          className="mt-6 flex space-x-4"
         initial={{opacity:0}}
         animate={{opacity: 1}}
         transition={{delay:1, duration: 1}}
      >
        <Button onClick={() => router.push('/auth/login')} variant="outline" className="text-black border-white hover:bg-white hover:text-indigo-600">Get Started</Button>
      </motion.div>

    </div>

  );
}
