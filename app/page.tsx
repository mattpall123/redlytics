"use client";

import { Silkscreen } from "next/font/google";
import React, { useState, useRef, useEffect } from "react";
import { Typewriter } from "react-simple-typewriter";
import "pixel-retroui/dist/fonts.css";
import { Button, Card } from "pixel-retroui";
import { Input } from "pixel-retroui";
import { ProgressBar } from 'pixel-retroui';


const silkscreenFont = Silkscreen({
  subsets: ["latin"],
  weight: "400",
});

export default function Home() {
  const [progress, setProgress] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const [insight, setInsight] = useState("");
  const [subreddit, setSubreddit] = useState("BuyItForLife");


  const handleClick = () => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    setProgress(0);

    intervalRef.current = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(intervalRef.current!);
          return 100;
        }
        return prev + 2;
      });
    }, 80);

    fetch(`http://127.0.0.1:8000/insight?subreddit=${subreddit}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Received from API:", data);
        setInsight(data.insight);
      })
      .catch((err) => console.error("Fetch failed:", err));
      
  };

  return (
    <div className="pt-10 pl-100 pr-100 pb-10">
      <div className={silkscreenFont.className}>
        <Card
          bg="#fefcd0"
          textColor="black"
          borderColor="black"
          shadowColor="#c381b5"
          className="p-4 text-center"
        >
          <div
            className={`flex justify-start text-9xl text-red-500 drop-shadow-[2px_2px_0_#000] ${silkscreenFont.className}`}
            style={{ width: "full", height: "400px", overflow: "hidden" }}
          >
            <Typewriter
              words={["REDLYTICS", "Whats Trending On Reddit?", "What Should Your Company Build?","REDLYTICS"]}
              loop={1}
              cursor
              cursorStyle="_"
              typeSpeed={70}
              deleteSpeed={50}
              delaySpeed={1000}
            />
          </div>
        </Card>
      </div>

      <div className=" flex justify-center text-5xl pt-10">
        <Card
          bg="#fefcd0"
          textColor="black"
          borderColor="black"
          shadowColor="#c381b5"
          className="p-4 text-center w-full"
        >
          <div className="p-10 text-3xl">
            Enter Your Subreddit Of Interest Here
          </div>

          <Input
            bg="white"
            textColor="black"
            borderColor="black"
            placeholder="subredditofinterest..."
            onChange={(e) => setSubreddit(e.target.value)}
            className="w-full"
          />
        </Card>
        
        
      </div>
      <div className="flex justify-center pt-10 text-5xl">
        <Button
          bg="#ff6251"
          textColor="#ffecd5"
          borderColor="#000000"
          shadow="#232323"
          className="text-center w-full h-40 py-3 tracking-wide text-5xl hover:scale-[1.03] transition-transform duration-150"
          onClick={handleClick}
        >
          Find Whats Trending!
        </Button>
      </div>
      <div className="flex justify-center pt-5">
        <ProgressBar
          progress={progress}
          height={30}
          bg="#1a1a1a"
          fill="#ff6251"
          border="#000000"
        />
      </div>
      <div className="flex justify-center pt-10 text-5xl">

        <Card
          bg="#fefcd0"
          textColor="black"
          borderColor="black"
          shadowColor="#c381b5"
          className="p-4 w-full h-80"
        >
          <div className="italic text-gray-500">
            <p className="text-xl">{insight || "Waiting for subreddit insight..."}</p>
          </div>
         
        </Card>
      </div>

      <div className="flex justify-center pt-10">
        <Card
          bg="#fefcd0"
          textColor="black"
          borderColor="black"
          shadowColor="#c381b5"
          className="p-4 w-full h-30"
        >
          <h1>Footer</h1>
         
        </Card>
      </div>
      
    </div>
  );
}
