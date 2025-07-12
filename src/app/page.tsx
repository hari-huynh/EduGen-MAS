"use client"
import Image from "next/image";
import { GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";
import { SignedIn, SignedOut, SignInButton, UserButton, ClerkProvider } from '@clerk/nextjs';
import { useAuth } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useState, useEffect,useRef  } from "react"
import { useUser } from "@clerk/nextjs";
// import Cookies from "js-cookie";


export default function Home() {
  const router = useRouter();
  // const { isLoaded, user,isSignedIn } = useUser();
  //   if (!isLoaded) {
  //   return <div>Loading...</div>;
  // }


  const { isLoaded, isSignedIn, user } = useUser();

  const hasSentUser = useRef(false);
  useEffect(() => {
    if (isLoaded && isSignedIn && user && !hasSentUser.current) {
      hasSentUser.current = true; 

      fetch("http://localhost:8000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_id: user.id, 
          first_name: user.firstName,
          last_name: user.lastName,
          email: user.primaryEmailAddress?.emailAddress ?? "",
        }),
      })
      .then(res => res.json())
      .then(data => {
        console.log(data);

        // Save user_id to cookie
        document.cookie = `userId=${user.id}`
        router.push(`/workspace/${user.id}`);
      })
      .catch(error => {
        console.error("Lỗi gửi thông tin user:", error);
      });
    }
  }, [isLoaded, isSignedIn, user]);
  
  return (
    <div className="w-full h-full">

      <div className="flex sticky top-0 items-center justify-between p-3 bg-slate-200">
                <div className="flex items-center gap-2">
                  <div className="size-24 rounded-full bg-conic/decreasing from-violet-700 via-lime-300 to-violet-700 rounded-full w-12 h-12 flex items-center justify-center">
                    <GraduationCap className="w-8 h-8 text-white" />
                  </div>
                  <span className="text-lg font-semibold">Educational Multiagent System</span>
                </div>
                  <header className="flex items-center gap-4">
                    <SignedIn>
                      <UserButton />
                    </SignedIn>
                  </header>
      </div>
      <div className="flex grid grid-rows-2 items-center justify-center pt-10">
        <h1 className="text-5xl font-bold font-sans">Welcome to Educational Multiagent System</h1>
          
          <div className="flex justify-center items-center pt-20">
            <div className="flex space-x-4">
              <SignedOut>
                <SignInButton mode="modal">
                  <Button>
                    Đăng nhập để bắt đầu
                  </Button>
                </SignInButton>
              </SignedOut>
            </div>
          </div>

      </div>
  
    </div>
  );

}


