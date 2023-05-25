import { ChatResponse, ConversationRequest } from "./models";

export async function conversationApi(options: ConversationRequest, abortSignal: AbortSignal): Promise<ChatResponse> {
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

***REMOVED***const parsedResponse: ChatResponse = await response.json();
***REMOVED***
***REMOVED***if (response.status > 299 || !response.ok) {
***REMOVED***console.log("Error response from /conversation", parsedResponse)
***REMOVED***const message = "An error occurred. Please try again. If the problem persists, please contact the site administrator.";
***REMOVED***alert(message);
***REMOVED***throw Error(message);
***REMOVED***

***REMOVED***return parsedResponse;
}
