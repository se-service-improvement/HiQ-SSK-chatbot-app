import { ChatMessage, ConversationRequest, FeedbackRequest } from "./models";

export async function conversationApi(options: ConversationRequest): Promise<ChatMessage> {
***REMOVED***const response = await fetch("/conversation", {
***REMOVED***method: "POST",
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***messages: options.messages
***REMOVED***)
***REMOVED***);

***REMOVED***const parsedResponse: ChatMessage = await response.json();
***REMOVED***if (response.status > 299 || !response.ok) {
***REMOVED***alert("Unknown error");
***REMOVED***throw Error("Unknown error");
***REMOVED***

***REMOVED***return parsedResponse;
}

export async function feedbackApi(request: FeedbackRequest): Promise<void> {
***REMOVED***const response = await fetch("/feedback", {
***REMOVED***method: "POST",
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***message_id: request.message_id,
***REMOVED******REMOVED***rating: request.feedback
***REMOVED***)
***REMOVED***);
***REMOVED***console.log("Feedback response: ", response.status, response.ok);

***REMOVED***if (response.status > 299 || !response.ok) {
***REMOVED***alert("Unknown error");
***REMOVED***throw Error("Unknown error");
***REMOVED***
}
