import { ChatResponse, ConversationRequest } from "./models";

export async function conversationApi(options: ConversationRequest, abortSignal: AbortSignal): Promise<Response> {
***REMOVED***const response = await fetch("/conversation", {
***REMOVED***method: "POST",
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***messages: options.messages
***REMOVED***),
***REMOVED***signal: abortSignal
***REMOVED***);

***REMOVED***return response;
}
