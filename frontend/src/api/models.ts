export type AskResponse = {
***REMOVED***answer: string;
***REMOVED***citations: Citation[];
***REMOVED***error?: string;
};

export type Citation = {
***REMOVED***content: string;
***REMOVED***id: string;
***REMOVED***title: string | null;
***REMOVED***filepath: string | null;
***REMOVED***url: string | null;
***REMOVED***metadata: string | null;
***REMOVED***chunk_id: string | null;
***REMOVED***reindex_id: string | null;
}

export type ToolMessageContent = {
***REMOVED***citations: Citation[];
***REMOVED***intent: string;
}

export type ChatMessage = {
***REMOVED***role: string;
***REMOVED***content: string;
***REMOVED***end_turn?: boolean;
};

export enum ChatCompletionType {
***REMOVED***ChatCompletion = "chat.completion",
***REMOVED***ChatCompletionChunk = "chat.completion.chunk"
}

export type ChatResponseChoice = {
***REMOVED***messages: ChatMessage[];
}

export type ChatResponse = {
***REMOVED***id: string;
***REMOVED***model: string;
***REMOVED***created: number;
***REMOVED***object: ChatCompletionType;
***REMOVED***choices: ChatResponseChoice[];
}

export type ConversationRequest = {
***REMOVED***messages: ChatMessage[];
};

export type UserInfo = {
***REMOVED***access_token: string;
***REMOVED***expires_on: string;
***REMOVED***id_token: string;
***REMOVED***provider_name: string;
***REMOVED***user_claims: any[];
***REMOVED***user_id: string;
};