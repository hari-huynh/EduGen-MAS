"use client";

import { useUser } from "@clerk/nextjs";
import { useSearchParams } from "next/navigation";
import { SignedIn, SignedOut, SignInButton, UserButton, ClerkProvider } from '@clerk/nextjs';

export default function WelcomePage() {
  const { isLoaded, isSignedIn, user } = useUser();
  const params = useSearchParams();
  const userId = params.get("id");

  if (!isLoaded) {
    return <div>Loading...</div>;
  }

  // Nếu có thể, lấy tên, nếu không thì lấy user id
  let nameOrId = user?.firstName
    ? user.firstName
    : userId
    ? userId
    : "User";

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold">Xin chào, {nameOrId}!</h1>
      <p>Chào mừng bạn đến với hệ thống của chúng tôi.</p>

                        <header className="flex items-center gap-4">
                    <SignedIn>
                      <UserButton />
                    </SignedIn>
                  </header>
    </div>
  );
}