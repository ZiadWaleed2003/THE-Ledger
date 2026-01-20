import { useState, useCallback, useRef, useEffect } from "react";
import { ChatMessage } from "@/types/asset";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";
const WS_URL = `${API_BASE.replace(/^http/, "ws")}/ws/chat`;

export function useWebSocket() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const streamingIntervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      setIsConnected(true);
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      let content = "";
      let sources: string[] = [];

      try {
        const data = JSON.parse(event.data);
        content = data.answer || data.message || "No response";
        // Clean up any escaped newlines that might have been sent as literal characters
        content = content.replace(/\\n/g, '\n');
        sources = data.sources || [];
      } catch {
        content = event.data;
      }

      setIsLoading(false);
      const messageId = crypto.randomUUID();

      setMessages((prev) => [
        ...prev,
        {
          id: messageId,
          role: "assistant",
          content: "",
          sources,
          timestamp: new Date(),
        },
      ]);

      if (streamingIntervalRef.current) {
        clearInterval(streamingIntervalRef.current);
      }

      let currentIndex = 0;
      streamingIntervalRef.current = setInterval(() => {
        if (currentIndex < content.length) {
          setMessages((prev) =>
            prev.map((msg) =>
              msg.id === messageId
                ? { ...msg, content: content.slice(0, currentIndex + 1) }
                : msg
            )
          );
          currentIndex++;
        } else {
          if (streamingIntervalRef.current) {
            clearInterval(streamingIntervalRef.current);
            streamingIntervalRef.current = null;
          }
        }
      }, 20);
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log("WebSocket disconnected");
      if (streamingIntervalRef.current) {
        clearInterval(streamingIntervalRef.current);
        streamingIntervalRef.current = null;
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setIsConnected(false);
      setIsLoading(false);
      if (streamingIntervalRef.current) {
        clearInterval(streamingIntervalRef.current);
        streamingIntervalRef.current = null;
      }
    };

    wsRef.current = ws;
  }, []);

  const disconnect = useCallback(() => {
    if (streamingIntervalRef.current) {
      clearInterval(streamingIntervalRef.current);
      streamingIntervalRef.current = null;
    }
    wsRef.current?.close();
    wsRef.current = null;
  }, []);

  const sendMessage = useCallback((content: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.error("WebSocket is not connected");
      return;
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    wsRef.current.send(content);
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    messages,
    isConnected,
    isLoading,
    connect,
    disconnect,
    sendMessage,
    clearMessages: () => setMessages([]),
  };
}
