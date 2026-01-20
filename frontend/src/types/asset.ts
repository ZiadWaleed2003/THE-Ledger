export interface Asset {
  id: string;
  name: string;
  category: string;
  value: number;
  status: "Active" | "Maintenance" | "Retired";
  purchase_date: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: string[];
  timestamp: Date;
}
