import { useEffect, useRef, useState } from "react";
import { Send, Bot, User, Wifi, WifiOff, Loader2, Trash2 } from "lucide-react";

import { useWebSocket } from "@/hooks/useWebSocket";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";

export default function AIAssistant() {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { messages, isConnected, isLoading, connect, disconnect, sendMessage, clearMessages } =
    useWebSocket();

  useEffect(() => {
    connect();
    return () => disconnect();
  }, [connect, disconnect]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !isConnected || isLoading) return;
    sendMessage(input.trim());
    setInput("");
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">AI Assistant</h1>
          <p className="text-muted-foreground mt-1">
            Chat with your intelligent asset management assistant
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge
            variant={isConnected ? "default" : "secondary"}
            className="flex items-center gap-1.5"
          >
            {isConnected ? (
              <>
                <Wifi className="h-3 w-3" />
                Connected
              </>
            ) : (
              <>
                <WifiOff className="h-3 w-3" />
                Disconnected
              </>
            )}
          </Badge>
          {messages.length > 0 && (
            <Button variant="outline" size="sm" onClick={clearMessages}>
              <Trash2 className="h-4 w-4 mr-2" />
              Clear Chat
            </Button>
          )}
        </div>
      </div>

      <div className="flex-1 border border-border rounded-lg bg-card flex flex-col overflow-hidden">
        <ScrollArea className="flex-1 p-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full min-h-[300px] text-muted-foreground">
              <Bot className="h-16 w-16 mb-4 opacity-50" />
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm text-center max-w-md mt-2">
                Ask me anything about your assets, inventory management, or let me help you analyze your data.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "flex items-start gap-3",
                    message.role === "user" ? "flex-row-reverse" : "flex-row"
                  )}
                >
                  <div
                    className={cn(
                      "flex items-center justify-center h-8 w-8 rounded-full shrink-0",
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted text-muted-foreground"
                    )}
                  >
                    {message.role === "user" ? (
                      <User className="h-4 w-4" />
                    ) : (
                      <Bot className="h-4 w-4" />
                    )}
                  </div>
                  <div
                    className={cn(
                      "max-w-[75%] rounded-lg px-4 py-3",
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted/50 text-foreground"
                    )}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    {message.sources && message.sources.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3 pt-3 border-t border-border/30">
                        {message.sources.map((source, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs">
                            Source: {source}
                          </Badge>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex items-start gap-3">
                  <div className="flex items-center justify-center h-8 w-8 rounded-full bg-muted text-muted-foreground shrink-0">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div className="bg-muted/50 rounded-lg px-4 py-3">
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span className="text-sm">Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </ScrollArea>

        <form
          onSubmit={handleSubmit}
          className="border-t border-border p-4 flex items-center gap-3"
        >
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              isConnected
                ? "Type your message..."
                : "Connecting to server..."
            }
            disabled={!isConnected || isLoading}
            className="flex-1"
          />
          <Button type="submit" disabled={!isConnected || isLoading || !input.trim()}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </div>
  );
}
