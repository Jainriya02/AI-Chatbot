export interface Citation {
  file: string;
  page: number;
}

export interface ChatResponse {
  tool: "RAG" | "SQL" | "MULTI_TOOL";
  answer: string;
  sql?: string;
  citations?: Citation[];
}

export interface MessageType {
  role: "user" | "assistant";
  content: string;
  response?: ChatResponse;
}