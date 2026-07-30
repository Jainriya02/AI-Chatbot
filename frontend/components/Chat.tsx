"use client";

import { useState } from "react";
import Message from "./Message";
import { MessageType, ChatResponse } from "../types";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<MessageType[]>([]);

  async function sendMessage() {
    if (!question.trim()) return;

    const userMessage: MessageType = {
      role: "user",
      content: question,
    };

    setMessages([userMessage]);

    setLoading(true);

    try {
      const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

const response = await fetch(`${API_URL}/chat`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    question,
  }),
});
      

      const data: ChatResponse = await response.json();

      const assistantMessage: MessageType = {
        role: "assistant",
        content: data.answer,
        response: data,
      };

      setMessages([userMessage, assistantMessage]);
    } catch (err) {
      setMessages([
        userMessage,
        {
          role: "assistant",
          content: "Something went wrong.",
        },
      ]);
    }

    setLoading(false);
    setQuestion("");
  }

  return (
    <div className="max-w-4xl mx-auto p-8">

      <h1 className="text-3xl font-bold mb-8">
        AI Chatbot
      </h1>

      <div className="space-y-5 mb-8">

        {messages.map((message, index) => (
          <Message
            key={index}
            message={message}
          />
        ))}

      </div>

      {loading && (
        <p>Thinking...</p>
      )}

      <div className="flex gap-3">

        <input
          className="border rounded p-3 flex-1"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              void sendMessage();
            }
          }}
          placeholder="Ask a question..."
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-5 rounded"
        >
          Send
        </button>

      </div>

    </div>
  );
}