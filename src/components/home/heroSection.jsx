"use client";
import React from "react";
import { Spotlight } from "../ui/spotLight";
import { ChatbotInterface } from "./chatbotInterface";
import Navbar from "../layout/navbar";
import { useRouter } from "next/navigation";

export function HeroSection() {
  const router = useRouter();
  const navigateToAuth = (isLogin) => {
    router.push(`/authentication?form=${isLogin ? "login" : "register"}`);
  };

  return (
    <div>
      <Navbar></Navbar>
      <div className="h-screen w-full flex md:items-center md:justify-center bg-black antialiased bg-grid-white/[0.02] relative overflow-hidden montserrat-font-medium">
        <Spotlight />
        <div className="p-4 max-w-7xl mx-auto relative z-10 w-full pt-24">
          <h1 className="text-8xl font-bold text-center bg-clip-text text-transparent bg-gradient-to-b from-neutral-50 to-neutral-400 bg-opacity-50">
            AI-powered automation <br /> to replace{" "}
            <span className="zodiak-italic-font"> Accountants.</span>
          </h1>
          <p className="mt-8 font-normal text-neutral-300 max-w-xl text-center mx-auto text-2xl">
            We're building a fully automated AI solution that eliminates the
            need for manual accounting — faster, smarter, and cost-effective.
          </p>

          {/* CTA Button Centered */}
          <div className="mt-10 flex justify-center">
            <button
              onClick={() => navigateToAuth(false)}
              className="px-6 py-3 text-lg text-white bg-blue-600 border border-blue-600 rounded-xl hover:bg-blue-700 transition duration-200 montserrat-font-medium"
            >
              Get Started
            </button>
          </div>
        </div>

        <ChatbotInterface></ChatbotInterface>
      </div>
    </div>
  );
}
