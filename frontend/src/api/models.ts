export type AskResponse = {
***REMOVED***answer: string;
***REMOVED***thoughts: string | null;
***REMOVED***data_points: string[];
***REMOVED***top_docs: DocumentResult[];
***REMOVED***error?: string;
};

export type MessageContent = {
***REMOVED***content_type: string;
***REMOVED***parts: string[];
***REMOVED***top_docs: DocumentResult[];
***REMOVED***intent: string | null;
};

export type DocumentResult = {
***REMOVED***content: string;
***REMOVED***id: string;
***REMOVED***title: string | null;
***REMOVED***filepath: string | null;
***REMOVED***url: string | null;
***REMOVED***metadata: string | null;
***REMOVED***chunk_id: string | null;
}

export type ChatMessage = {
***REMOVED***message_id: string;
***REMOVED***parent_message_id: string | null;
***REMOVED***role: string;
***REMOVED***content: MessageContent;
};

export type ConversationRequest = {
***REMOVED***messages: ChatMessage[];
};
