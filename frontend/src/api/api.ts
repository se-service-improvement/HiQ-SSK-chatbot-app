import { UserInfo, ConversationRequest, Conversation, ChatMessage, CosmosDBHealth, CosmosDBStatus } from "./models";
import { chatHistorySampleData } from "../constants/chatHistory";

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

// export const fetchChatHistoryInit = async (): Promise<Conversation[] | null> => {
export const fetchChatHistoryInit = (): Conversation[] | null => {
***REMOVED***// Make initial API call here

***REMOVED***// return null;
***REMOVED***return chatHistorySampleData;
}

export const historyList = async (): Promise<Conversation[] | null> => {
***REMOVED***const response = await fetch("/history/list", {
***REMOVED***method: "GET",
***REMOVED***).then(async (res) => {
***REMOVED***const payload = await res.json();
***REMOVED***if (!Array.isArray(payload)) {
***REMOVED******REMOVED***console.error("There was an issue fetching your data.");
***REMOVED******REMOVED***return null;
***REMOVED***
***REMOVED***const conversations: Conversation[] = await Promise.all(payload.map(async (conv: any) => {
***REMOVED******REMOVED***let convMessages: ChatMessage[] = [];
***REMOVED******REMOVED***convMessages = await historyRead(conv.id)
***REMOVED******REMOVED***.then((res) => {
***REMOVED******REMOVED***return res
***REMOVED***)
***REMOVED******REMOVED***.catch((err) => {
***REMOVED******REMOVED***console.error("error fetching messages: ", err)
***REMOVED******REMOVED***return []
***REMOVED***)
***REMOVED******REMOVED***const conversation: Conversation = {
***REMOVED******REMOVED***id: conv.id,
***REMOVED******REMOVED***title: conv.title,
***REMOVED******REMOVED***date: conv.createdAt,
***REMOVED******REMOVED***messages: convMessages
***REMOVED***;
***REMOVED******REMOVED***return conversation;
***REMOVED***));
***REMOVED***return conversations;
***REMOVED***).catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***return null
***REMOVED***)

***REMOVED***return response
}

export const historyRead = async (convId: string): Promise<ChatMessage[]> => {
***REMOVED***const response = await fetch("/history/read", {
***REMOVED***method: "POST",
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***conversation_id: convId
***REMOVED***),
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***)
***REMOVED***.then(async (res) => {
***REMOVED***if(!res){
***REMOVED******REMOVED***return []
***REMOVED***
***REMOVED***const payload = await res.json();
***REMOVED***let messages: ChatMessage[] = [];
***REMOVED***if(payload?.messages){
***REMOVED******REMOVED***payload.messages.forEach((msg: any) => {
***REMOVED******REMOVED***const message: ChatMessage = {
***REMOVED******REMOVED******REMOVED***id: msg.id,
***REMOVED******REMOVED******REMOVED***role: msg.role,
***REMOVED******REMOVED******REMOVED***date: msg.createdAt,
***REMOVED******REMOVED******REMOVED***content: msg.content,
***REMOVED******REMOVED***
***REMOVED******REMOVED***messages.push(message)
***REMOVED***);
***REMOVED***
***REMOVED***return messages;
***REMOVED***).catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***return []
***REMOVED***)
***REMOVED***return response
}

export const historyGenerate = async (options: ConversationRequest, abortSignal: AbortSignal, convId?: string): Promise<Response> => {
***REMOVED***let body;
***REMOVED***if(convId){
***REMOVED***body = JSON.stringify({
***REMOVED******REMOVED***conversation_id: convId,
***REMOVED******REMOVED***messages: options.messages
***REMOVED***)
***REMOVED***else{
***REMOVED***body = JSON.stringify({
***REMOVED******REMOVED***messages: options.messages
***REMOVED***)
***REMOVED***
***REMOVED***const response = await fetch("/history/generate", {
***REMOVED***method: "POST",
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***body: body,
***REMOVED***signal: abortSignal
***REMOVED***).then((res) => {
***REMOVED***return res
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***return new Response;
***REMOVED***)
***REMOVED***return response
}

export const historyUpdate = async (messages: ChatMessage[], convId: string): Promise<Response> => {
***REMOVED***const response = await fetch("/history/update", {
***REMOVED***method: "POST",
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***conversation_id: convId,
***REMOVED******REMOVED***messages: messages
***REMOVED***),
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***).then(async (res) => {
***REMOVED***return res
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***let errRes: Response = {
***REMOVED******REMOVED***...new Response,
***REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED***status: 500,
***REMOVED***
***REMOVED***return errRes;
***REMOVED***)
***REMOVED***return response
}

export const historyDelete = async (convId: string) : Promise<Response> => {
***REMOVED***const response = await fetch("/history/delete", {
***REMOVED***method: "DELETE",
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***conversation_id: convId,
***REMOVED***),
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***)
***REMOVED***.then((res) => {
***REMOVED***return res
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***let errRes: Response = {
***REMOVED******REMOVED***...new Response,
***REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED***status: 500,
***REMOVED***
***REMOVED***return errRes;
***REMOVED***)
***REMOVED***return response;
}

export const historyDeleteAll = async () : Promise<Response> => {
***REMOVED***const response = await fetch("/history/delete_all", {
***REMOVED***method: "DELETE",
***REMOVED***body: JSON.stringify({}),
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***)
***REMOVED***.then((res) => {
***REMOVED***return res
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***let errRes: Response = {
***REMOVED******REMOVED***...new Response,
***REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED***status: 500,
***REMOVED***
***REMOVED***return errRes;
***REMOVED***)
***REMOVED***return response;
}

export const historyClear = async (convId: string) : Promise<Response> => {
***REMOVED***const response = await fetch("/history/clear", {
***REMOVED***method: "POST",
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***conversation_id: convId,
***REMOVED***),
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***)
***REMOVED***.then((res) => {
***REMOVED***return res
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***let errRes: Response = {
***REMOVED******REMOVED***...new Response,
***REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED***status: 500,
***REMOVED***
***REMOVED***return errRes;
***REMOVED***)
***REMOVED***return response;
}

export const historyRename = async (convId: string, title: string) : Promise<Response> => {
***REMOVED***const response = await fetch("/history/rename", {
***REMOVED***method: "POST",
***REMOVED***body: JSON.stringify({
***REMOVED******REMOVED***conversation_id: convId,
***REMOVED******REMOVED***title: title
***REMOVED***),
***REMOVED***headers: {
***REMOVED******REMOVED***"Content-Type": "application/json"
***REMOVED***,
***REMOVED***)
***REMOVED***.then((res) => {
***REMOVED***return res
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***let errRes: Response = {
***REMOVED******REMOVED***...new Response,
***REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED***status: 500,
***REMOVED***
***REMOVED***return errRes;
***REMOVED***)
***REMOVED***return response;
}

export const historyEnsure = async (): Promise<CosmosDBHealth> => {
***REMOVED***const response = await fetch("/history/ensure", {
***REMOVED***method: "GET",
***REMOVED***)
***REMOVED***.then(async res => {
***REMOVED***let respJson = await res.json();
***REMOVED***let formattedResponse;
***REMOVED***if(respJson.message){
***REMOVED******REMOVED***formattedResponse = CosmosDBStatus.Working
***REMOVED***else{
***REMOVED******REMOVED***if(res.status === 500){
***REMOVED******REMOVED***formattedResponse = CosmosDBStatus.NotWorking
***REMOVED***else{
***REMOVED******REMOVED***formattedResponse = CosmosDBStatus.NotConfigured
***REMOVED***
***REMOVED***
***REMOVED***if(!res.ok){
***REMOVED******REMOVED***return {
***REMOVED******REMOVED***cosmosDB: false,
***REMOVED******REMOVED***status: formattedResponse
***REMOVED***
***REMOVED***else{
***REMOVED******REMOVED***return {
***REMOVED******REMOVED***cosmosDB: true,
***REMOVED******REMOVED***status: formattedResponse
***REMOVED***
***REMOVED***
***REMOVED***)
***REMOVED***.catch((err) => {
***REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***return {
***REMOVED******REMOVED***cosmosDB: false,
***REMOVED******REMOVED***status: err
***REMOVED***
***REMOVED***)
***REMOVED***return response;
}

