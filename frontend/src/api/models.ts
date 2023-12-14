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
***REMOVED***id: string;
***REMOVED***role: string;
***REMOVED***content: string;
***REMOVED***end_turn?: boolean;
***REMOVED***date: string;
};

export type Conversation = {
***REMOVED***id: string;
***REMOVED***title: string;
***REMOVED***messages: ChatMessage[];
***REMOVED***date: string;
}

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
***REMOVED***history_metadata: {
***REMOVED***conversation_id: string;
***REMOVED***title: string;
***REMOVED***date: string;
***REMOVED***
***REMOVED***error?: any;
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

export enum CosmosDBStatus {
***REMOVED***NotConfigured = "CosmosDB is not configured",
***REMOVED***NotWorking = "CosmosDB is not working",
***REMOVED***Working = "CosmosDB is configured and working",
}

export type CosmosDBHealth = {
***REMOVED***cosmosDB: boolean,
***REMOVED***status: string
}

export enum ChatHistoryLoadingState {
***REMOVED***Loading = "loading",
***REMOVED***Success = "success",
***REMOVED***Fail = "fail",
***REMOVED***NotStarted = "notStarted"
}

export type ErrorMessage = {
***REMOVED***title: string,
***REMOVED***subtitle: string
}

export type FrontendSettings = {
***REMOVED***auth_enabled?: string | null;
}