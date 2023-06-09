import { UserInfo, ConversationRequest } from "./models";

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

export async function getUserInfo(): Promise<UserInfo[]> {
***REMOVED***const response = await fetch('/.auth/me');
***REMOVED***if (!response.ok) {
***REMOVED***console.log("No identity provider found. Access to chat will be blocked.")
***REMOVED***return [];
***REMOVED***

***REMOVED***const payload = await response.json();
***REMOVED***return payload;
}