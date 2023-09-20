import { useRef, useState, useEffect, useContext, useLayoutEffect } from "react";
import { CommandBarButton, IconButton, Dialog, DialogType, Stack } from "@fluentui/react";
import { DismissRegular, SquareRegular, ShieldLockRegular, ErrorCircleRegular } from "@fluentui/react-icons";

import ReactMarkdown from "react-markdown";
import remarkGfm from 'remark-gfm'
import rehypeRaw from "rehype-raw";
import uuid from 'react-uuid';

import styles from "./Chat.module.css";
import Azure from "../../assets/Azure.svg";

import {
***REMOVED***ChatMessage,
***REMOVED***ConversationRequest,
***REMOVED***conversationApi,
***REMOVED***Citation,
***REMOVED***ToolMessageContent,
***REMOVED***ChatResponse,
***REMOVED***getUserInfo,
***REMOVED***Conversation,
***REMOVED***historyGenerate,
***REMOVED***historyUpdate,
***REMOVED***historyClear,
***REMOVED***ChatHistoryLoadingState,
***REMOVED***CosmosDBStatus,
***REMOVED***ErrorMessage
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
import { ChatHistoryPanel } from "../../components/ChatHistory/ChatHistoryPanel";
import { AppStateContext } from "../../state/AppProvider";
import { useBoolean } from "@fluentui/react-hooks";

const enum messageStatus {
***REMOVED***NotRunning = "Not Running",
***REMOVED***Processing = "Processing",
***REMOVED***Done = "Done"
}

const Chat = () => {
***REMOVED***const appStateContext = useContext(AppStateContext)
***REMOVED***const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);
***REMOVED***const [isLoading, setIsLoading] = useState<boolean>(false);
***REMOVED***const [showLoadingMessage, setShowLoadingMessage] = useState<boolean>(false);
***REMOVED***const [activeCitation, setActiveCitation] = useState<[content: string, id: string, title: string, filepath: string, url: string, metadata: string]>();
***REMOVED***const [isCitationPanelOpen, setIsCitationPanelOpen] = useState<boolean>(false);
***REMOVED***const abortFuncs = useRef([] as AbortController[]);
***REMOVED***const [showAuthMessage, setShowAuthMessage] = useState<boolean>(true);
***REMOVED***const [messages, setMessages] = useState<ChatMessage[]>([])
***REMOVED***const [processMessages, setProcessMessages] = useState<messageStatus>(messageStatus.NotRunning);
***REMOVED***const [clearingChat, setClearingChat] = useState<boolean>(false);
***REMOVED***const [hideErrorDialog, { toggle: toggleErrorDialog }] = useBoolean(true);
***REMOVED***const [errorMsg, setErrorMsg] = useState<ErrorMessage | null>()

***REMOVED***const errorDialogContentProps = {
***REMOVED***type: DialogType.close,
***REMOVED***title: errorMsg?.title,
***REMOVED***closeButtonAriaLabel: 'Close',
***REMOVED***subText: errorMsg?.subtitle,
***REMOVED***;

***REMOVED***const modalProps = {
***REMOVED***titleAriaId: 'labelId',
***REMOVED***subtitleAriaId: 'subTextId',
***REMOVED***isBlocking: true,
***REMOVED***styles: { main: { maxWidth: 450 } },
***REMOVED***

***REMOVED***useEffect(() => {
***REMOVED***if(appStateContext?.state.isCosmosDBAvailable?.status === CosmosDBStatus.NotWorking && appStateContext.state.chatHistoryLoadingState === ChatHistoryLoadingState.Fail && hideErrorDialog){
***REMOVED******REMOVED***let subtitle = `${appStateContext.state.isCosmosDBAvailable.status}. Please contact the site administrator.`
***REMOVED******REMOVED***setErrorMsg({
***REMOVED******REMOVED***title: "Chat history is not enabled",
***REMOVED******REMOVED***subtitle: subtitle
***REMOVED***)
***REMOVED******REMOVED***toggleErrorDialog();
***REMOVED***
***REMOVED***, [appStateContext?.state.isCosmosDBAvailable]);

***REMOVED***const handleErrorDialogClose = () => {
***REMOVED***toggleErrorDialog()
***REMOVED***setTimeout(() => {
***REMOVED******REMOVED***setErrorMsg(null)
***REMOVED***, 500);
***REMOVED***
***REMOVED***
***REMOVED***const getUserInfoList = async () => {
***REMOVED***const userInfoList = await getUserInfo();
***REMOVED***if (userInfoList.length === 0 && window.location.hostname !== "127.0.0.1") {
***REMOVED******REMOVED***setShowAuthMessage(true);
***REMOVED***
***REMOVED***else {
***REMOVED******REMOVED***setShowAuthMessage(false);
***REMOVED***
***REMOVED***

***REMOVED***const makeApiRequestWithoutCosmosDB = async (question: string, conversationId?: string) => {
***REMOVED***setIsLoading(true);
***REMOVED***setShowLoadingMessage(true);
***REMOVED***const abortController = new AbortController();
***REMOVED***abortFuncs.current.unshift(abortController);

***REMOVED***const userMessage: ChatMessage = {
***REMOVED******REMOVED***id: uuid(),
***REMOVED******REMOVED***role: "user",
***REMOVED******REMOVED***content: question,
***REMOVED******REMOVED***date: new Date().toISOString(),
***REMOVED***;

***REMOVED***let conversation: Conversation | null | undefined;
***REMOVED***if(!conversationId){
***REMOVED******REMOVED***conversation = {
***REMOVED******REMOVED***id: conversationId ?? uuid(),
***REMOVED******REMOVED***title: question,
***REMOVED******REMOVED***messages: [userMessage],
***REMOVED******REMOVED***date: new Date().toISOString(),
***REMOVED***
***REMOVED***else{
***REMOVED******REMOVED***conversation = appStateContext?.state?.currentChat
***REMOVED******REMOVED***if(!conversation){
***REMOVED******REMOVED***console.error("Conversation not found.");
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED***return;
***REMOVED***else{
***REMOVED******REMOVED***conversation.messages.push(userMessage);
***REMOVED***
***REMOVED***

***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: conversation });
***REMOVED***setMessages(conversation.messages)
***REMOVED***
***REMOVED***const request: ConversationRequest = {
***REMOVED******REMOVED***messages: [...conversation.messages.filter((answer) => answer.role !== "error")]
***REMOVED******REMOVED***// messages: [...conversation.messages.filter((answer) => answer.role === "error")]
***REMOVED***;

***REMOVED***let result = {} as ChatResponse;
***REMOVED***try {
***REMOVED******REMOVED***const response = await conversationApi(request, abortController.signal);
***REMOVED******REMOVED***if (response?.body) {
***REMOVED******REMOVED***const reader = response.body.getReader();
***REMOVED******REMOVED***let runningText = "";

***REMOVED******REMOVED***while (true) {
***REMOVED******REMOVED******REMOVED***setProcessMessages(messageStatus.Processing)
***REMOVED******REMOVED******REMOVED***const {done, value} = await reader.read();
***REMOVED******REMOVED******REMOVED***if (done) break;

***REMOVED******REMOVED******REMOVED***var text = new TextDecoder("utf-8").decode(value);
***REMOVED******REMOVED******REMOVED***const objects = text.split("\n");
***REMOVED******REMOVED******REMOVED***objects.forEach((obj) => {
***REMOVED******REMOVED******REMOVED***try {
***REMOVED******REMOVED******REMOVED******REMOVED***runningText += obj;
***REMOVED******REMOVED******REMOVED******REMOVED***result = JSON.parse(runningText);
***REMOVED******REMOVED******REMOVED******REMOVED***result.choices[0].messages.forEach((obj) => {
***REMOVED******REMOVED******REMOVED******REMOVED***obj.id = uuid();
***REMOVED******REMOVED******REMOVED******REMOVED***obj.date = new Date().toISOString();
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED******REMOVED***setMessages([...messages, ...result.choices[0].messages]);
***REMOVED******REMOVED******REMOVED******REMOVED***runningText = "";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***catch { }
***REMOVED******REMOVED***);
***REMOVED******REMOVED***
***REMOVED******REMOVED***conversation.messages.push(...result.choices[0].messages)
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: conversation });
***REMOVED******REMOVED***setMessages([...messages, ...result.choices[0].messages]);
***REMOVED***
***REMOVED******REMOVED***
***REMOVED*** catch ( e )  {
***REMOVED******REMOVED***if (!abortController.signal.aborted) {
***REMOVED******REMOVED***let errorMessage = "An error occurred. Please try again. If the problem persists, please contact the site administrator.";
***REMOVED******REMOVED***if (result.error?.message) {
***REMOVED******REMOVED******REMOVED***errorMessage = result.error.message;
***REMOVED******REMOVED***
***REMOVED******REMOVED***else if (typeof result.error === "string") {
***REMOVED******REMOVED******REMOVED***errorMessage = result.error;
***REMOVED******REMOVED***
***REMOVED******REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED******REMOVED******REMOVED***id: uuid(),
***REMOVED******REMOVED******REMOVED***role: "error",
***REMOVED******REMOVED******REMOVED***content: errorMessage,
***REMOVED******REMOVED******REMOVED***date: new Date().toISOString()
***REMOVED******REMOVED***
***REMOVED******REMOVED***conversation.messages.push(errorChatMsg);
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: conversation });
***REMOVED******REMOVED***setMessages([...messages, errorChatMsg]);
***REMOVED******REMOVED***
***REMOVED******REMOVED***setMessages([...messages, userMessage])
***REMOVED***
***REMOVED*** finally {
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED***setProcessMessages(messageStatus.Done)
***REMOVED***

***REMOVED***return abortController.abort();
***REMOVED***;

***REMOVED***const makeApiRequestWithCosmosDB = async (question: string, conversationId?: string) => {
***REMOVED***setIsLoading(true);
***REMOVED***setShowLoadingMessage(true);
***REMOVED***const abortController = new AbortController();
***REMOVED***abortFuncs.current.unshift(abortController);

***REMOVED***const userMessage: ChatMessage = {
***REMOVED******REMOVED***id: uuid(),
***REMOVED******REMOVED***role: "user",
***REMOVED******REMOVED***content: question,
***REMOVED******REMOVED***date: new Date().toISOString(),
***REMOVED***;

***REMOVED***//api call params set here (generate)
***REMOVED***let request: ConversationRequest;
***REMOVED***let conversation;
***REMOVED***if(conversationId){
***REMOVED******REMOVED***conversation = appStateContext?.state?.chatHistory?.find((conv) => conv.id === conversationId)
***REMOVED******REMOVED***if(!conversation){
***REMOVED******REMOVED***console.error("Conversation not found.");
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED***return;
***REMOVED***else{
***REMOVED******REMOVED***conversation.messages.push(userMessage);
***REMOVED******REMOVED***request = {
***REMOVED******REMOVED******REMOVED***messages: [...conversation.messages.filter((answer) => answer.role !== "error")]
***REMOVED******REMOVED***;
***REMOVED***
***REMOVED***else{
***REMOVED******REMOVED***request = {
***REMOVED******REMOVED***messages: [userMessage].filter((answer) => answer.role !== "error")
***REMOVED***;
***REMOVED******REMOVED***setMessages(request.messages)
***REMOVED***
***REMOVED***let result = {} as ChatResponse;
***REMOVED***try {
***REMOVED******REMOVED***const response = conversationId ? await historyGenerate(request, abortController.signal, conversationId) : await historyGenerate(request, abortController.signal);
***REMOVED******REMOVED***if(!response?.ok){
***REMOVED******REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED******REMOVED******REMOVED***id: uuid(),
***REMOVED******REMOVED******REMOVED***role: "error",
***REMOVED******REMOVED******REMOVED***content: "There was an error generating a response. Chat history can't be saved at this time. If the problem persists, please contact the site administrator.",
***REMOVED******REMOVED******REMOVED***date: new Date().toISOString()
***REMOVED******REMOVED***
***REMOVED******REMOVED***let resultConversation;
***REMOVED******REMOVED***if(conversationId){
***REMOVED******REMOVED******REMOVED***resultConversation = appStateContext?.state?.chatHistory?.find((conv) => conv.id === conversationId)
***REMOVED******REMOVED******REMOVED***if(!resultConversation){
***REMOVED******REMOVED******REMOVED***console.error("Conversation not found.");
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***resultConversation.messages.push(errorChatMsg);
***REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED***setMessages([...messages, userMessage, errorChatMsg])
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: resultConversation });
***REMOVED******REMOVED***setMessages([...resultConversation.messages]);
***REMOVED******REMOVED***return;
***REMOVED***
***REMOVED******REMOVED***if (response?.body) {
***REMOVED******REMOVED***const reader = response.body.getReader();
***REMOVED******REMOVED***let runningText = "";

***REMOVED******REMOVED***while (true) {
***REMOVED******REMOVED******REMOVED***setProcessMessages(messageStatus.Processing)
***REMOVED******REMOVED******REMOVED***const {done, value} = await reader.read();
***REMOVED******REMOVED******REMOVED***if (done) break;

***REMOVED******REMOVED******REMOVED***var text = new TextDecoder("utf-8").decode(value);
***REMOVED******REMOVED******REMOVED***const objects = text.split("\n");
***REMOVED******REMOVED******REMOVED***objects.forEach((obj) => {
***REMOVED******REMOVED******REMOVED***try {
***REMOVED******REMOVED******REMOVED******REMOVED***runningText += obj;
***REMOVED******REMOVED******REMOVED******REMOVED***result = JSON.parse(runningText);
***REMOVED******REMOVED******REMOVED******REMOVED***result.choices[0].messages.forEach((obj) => {
***REMOVED******REMOVED******REMOVED******REMOVED***obj.id = uuid();
***REMOVED******REMOVED******REMOVED******REMOVED***obj.date = new Date().toISOString();
***REMOVED******REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED******REMOVED***if(!conversationId){
***REMOVED******REMOVED******REMOVED******REMOVED***setMessages([...messages, userMessage, ...result.choices[0].messages]);
***REMOVED******REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED******REMOVED***setMessages([...messages, ...result.choices[0].messages]);
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***runningText = "";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***catch { }
***REMOVED******REMOVED***);
***REMOVED******REMOVED***

***REMOVED******REMOVED***let resultConversation;
***REMOVED******REMOVED***if(conversationId){
***REMOVED******REMOVED******REMOVED***resultConversation = appStateContext?.state?.chatHistory?.find((conv) => conv.id === conversationId)
***REMOVED******REMOVED******REMOVED***if(!resultConversation){
***REMOVED******REMOVED******REMOVED***console.error("Conversation not found.");
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***resultConversation.messages.push(...result.choices[0].messages);
***REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED***resultConversation = {
***REMOVED******REMOVED******REMOVED***id: result.history_metadata.conversation_id,
***REMOVED******REMOVED******REMOVED***title: result.history_metadata.title,
***REMOVED******REMOVED******REMOVED***messages: [userMessage],
***REMOVED******REMOVED******REMOVED***date: result.history_metadata.date
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***resultConversation.messages.push(...result.choices[0].messages);
***REMOVED******REMOVED***
***REMOVED******REMOVED***if(!resultConversation){
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: resultConversation });
***REMOVED******REMOVED***setMessages([...messages, ...result.choices[0].messages]);
***REMOVED***
***REMOVED******REMOVED***
***REMOVED*** catch ( e )  {
***REMOVED******REMOVED***if (!abortController.signal.aborted) {
***REMOVED******REMOVED***let errorMessage = "An error occurred. Please try again. If the problem persists, please contact the site administrator.";
***REMOVED******REMOVED***if (result.error?.message) {
***REMOVED******REMOVED******REMOVED***errorMessage = result.error.message;
***REMOVED******REMOVED***
***REMOVED******REMOVED***else if (typeof result.error === "string") {
***REMOVED******REMOVED******REMOVED***errorMessage = result.error;
***REMOVED******REMOVED***
***REMOVED******REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED******REMOVED******REMOVED***id: uuid(),
***REMOVED******REMOVED******REMOVED***role: "error",
***REMOVED******REMOVED******REMOVED***content: errorMessage,
***REMOVED******REMOVED******REMOVED***date: new Date().toISOString()
***REMOVED******REMOVED***
***REMOVED******REMOVED***let resultConversation;
***REMOVED******REMOVED***if(conversationId){
***REMOVED******REMOVED******REMOVED***resultConversation = appStateContext?.state?.chatHistory?.find((conv) => conv.id === conversationId)
***REMOVED******REMOVED******REMOVED***if(!resultConversation){
***REMOVED******REMOVED******REMOVED***console.error("Conversation not found.");
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***resultConversation.messages.push(errorChatMsg);
***REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED***if(!result.history_metadata){
***REMOVED******REMOVED******REMOVED***console.error("Error retrieving data.", result);
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***resultConversation = {
***REMOVED******REMOVED******REMOVED***id: result.history_metadata.conversation_id,
***REMOVED******REMOVED******REMOVED***title: result.history_metadata.title,
***REMOVED******REMOVED******REMOVED***messages: [userMessage],
***REMOVED******REMOVED******REMOVED***date: result.history_metadata.date
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***resultConversation.messages.push(errorChatMsg);
***REMOVED******REMOVED***
***REMOVED******REMOVED***if(!resultConversation){
***REMOVED******REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED******REMOVED***return;
***REMOVED******REMOVED***
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: resultConversation });
***REMOVED******REMOVED***setMessages([...messages, errorChatMsg]);
***REMOVED******REMOVED***
***REMOVED******REMOVED***setMessages([...messages, userMessage])
***REMOVED***
***REMOVED*** finally {
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED******REMOVED***setProcessMessages(messageStatus.Done)
***REMOVED***
***REMOVED***return abortController.abort();

***REMOVED***

***REMOVED***const clearChat = async () => {
***REMOVED***setClearingChat(true)
***REMOVED***if(appStateContext?.state.currentChat?.id && appStateContext?.state.isCosmosDBAvailable.cosmosDB){
***REMOVED******REMOVED***let response = await historyClear(appStateContext?.state.currentChat.id)
***REMOVED******REMOVED***if(!response.ok){
***REMOVED******REMOVED***setErrorMsg({
***REMOVED******REMOVED******REMOVED***title: "Error clearing current chat",
***REMOVED******REMOVED******REMOVED***subtitle: "Please try again. If the problem persists, please contact the site administrator.",
***REMOVED******REMOVED***)
***REMOVED******REMOVED***toggleErrorDialog();
***REMOVED***else{
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'DELETE_CURRENT_CHAT_MESSAGES', payload: appStateContext?.state.currentChat.id});
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CHAT_HISTORY', payload: appStateContext?.state.currentChat});
***REMOVED******REMOVED***setActiveCitation(undefined);
***REMOVED******REMOVED***setIsCitationPanelOpen(false);
***REMOVED******REMOVED***setMessages([])
***REMOVED***
***REMOVED***
***REMOVED***setClearingChat(false)
***REMOVED***;

***REMOVED***const newChat = () => {
***REMOVED***setProcessMessages(messageStatus.Processing)
***REMOVED***setMessages([])
***REMOVED***setIsCitationPanelOpen(false);
***REMOVED***setActiveCitation(undefined);
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: null });
***REMOVED***setProcessMessages(messageStatus.Done)
***REMOVED***;

***REMOVED***const stopGenerating = () => {
***REMOVED***abortFuncs.current.forEach(a => a.abort());
***REMOVED***setShowLoadingMessage(false);
***REMOVED***setIsLoading(false);
***REMOVED***

***REMOVED***useEffect(() => {
***REMOVED***if (appStateContext?.state.currentChat) {

***REMOVED******REMOVED***setMessages(appStateContext.state.currentChat.messages)
***REMOVED***else{
***REMOVED******REMOVED***setMessages([])
***REMOVED***
***REMOVED***, [appStateContext?.state.currentChat]);
***REMOVED***
***REMOVED***useLayoutEffect(() => {
***REMOVED***const saveToDB = async (messages: ChatMessage[], id: string) => {
***REMOVED******REMOVED***const response = await historyUpdate(messages, id)
***REMOVED******REMOVED***return response
***REMOVED***

***REMOVED***if (appStateContext && appStateContext.state.currentChat && processMessages === messageStatus.Done) {
***REMOVED******REMOVED***if(appStateContext.state.isCosmosDBAvailable.cosmosDB){
***REMOVED******REMOVED******REMOVED***if(!appStateContext?.state.currentChat?.messages){
***REMOVED******REMOVED******REMOVED***console.error("Failure fetching current chat state.")
***REMOVED******REMOVED******REMOVED***return 
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***saveToDB(appStateContext.state.currentChat.messages, appStateContext.state.currentChat.id)
***REMOVED******REMOVED******REMOVED***.then((res) => {
***REMOVED******REMOVED******REMOVED***if(!res.ok){
***REMOVED******REMOVED******REMOVED******REMOVED***let errorMessage = "An error occurred. Answers can't be saved at this time. If the problem persists, please contact the site administrator.";
***REMOVED******REMOVED******REMOVED******REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED******REMOVED******REMOVED******REMOVED***id: uuid(),
***REMOVED******REMOVED******REMOVED******REMOVED***role: "error",
***REMOVED******REMOVED******REMOVED******REMOVED***content: errorMessage,
***REMOVED******REMOVED******REMOVED******REMOVED***date: new Date().toISOString()
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***if(!appStateContext?.state.currentChat?.messages){
***REMOVED******REMOVED******REMOVED******REMOVED***let err: Error = {
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***...new Error,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***message: "Failure fetching current chat state."
***REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***throw err
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***setMessages([...appStateContext?.state.currentChat?.messages, errorChatMsg])
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return res as Response
***REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED***.catch((err) => {
***REMOVED******REMOVED******REMOVED***console.error("Error: ", err)
***REMOVED******REMOVED******REMOVED***let errRes: Response = {
***REMOVED******REMOVED******REMOVED******REMOVED***...new Response,
***REMOVED******REMOVED******REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED******REMOVED******REMOVED***status: 500,
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***return errRes;
***REMOVED******REMOVED***)
***REMOVED******REMOVED***else{
***REMOVED******REMOVED***
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CHAT_HISTORY', payload: appStateContext.state.currentChat });
***REMOVED******REMOVED***setMessages(appStateContext.state.currentChat.messages)
***REMOVED******REMOVED***setProcessMessages(messageStatus.NotRunning)
***REMOVED***
***REMOVED***, [processMessages]);

***REMOVED***useEffect(() => {
***REMOVED***getUserInfoList();
***REMOVED***, []);

***REMOVED***useLayoutEffect(() => {
***REMOVED***chatMessageStreamEnd.current?.scrollIntoView({ behavior: "smooth" })
***REMOVED***, [showLoadingMessage, processMessages]);

***REMOVED***const onShowCitation = (citation: Citation) => {
***REMOVED***setActiveCitation([citation.content, citation.id, citation.title ?? "", citation.filepath ?? "", "", ""]);
***REMOVED***setIsCitationPanelOpen(true);
***REMOVED***;

***REMOVED***const parseCitationFromMessage = (message: ChatMessage) => {
***REMOVED***if (message?.role && message?.role === "tool") {
***REMOVED******REMOVED***try {
***REMOVED******REMOVED***const toolMessage = JSON.parse(message.content) as ToolMessageContent;
***REMOVED******REMOVED***return toolMessage.citations;
***REMOVED***
***REMOVED******REMOVED***catch {
***REMOVED******REMOVED***return [];
***REMOVED***
***REMOVED***
***REMOVED***return [];
***REMOVED***

***REMOVED***const disabledButton = () => {
***REMOVED***return isLoading || (messages && messages.length === 0) || clearingChat || appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Loading
***REMOVED***

***REMOVED***return (
***REMOVED***<div className={styles.container} role="main">
***REMOVED******REMOVED***{showAuthMessage ? (
***REMOVED******REMOVED***<Stack className={styles.chatEmptyState}>
***REMOVED******REMOVED******REMOVED***<ShieldLockRegular className={styles.chatIcon} style={{color: 'darkorange', height: "200px", width: "200px"}}/>
***REMOVED******REMOVED******REMOVED***<h1 className={styles.chatEmptyStateTitle}>Authentication Not Configured</h1>
***REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle}>
***REMOVED******REMOVED******REMOVED***This app does not have authentication configured. Please add an identity provider by finding your app in the 
***REMOVED******REMOVED******REMOVED***<a href="https://portal.azure.com/" target="_blank"> Azure Portal </a>
***REMOVED******REMOVED******REMOVED***and following 
***REMOVED******REMOVED******REMOVED*** <a href="https://learn.microsoft.com/en-us/azure/app-service/scenario-secure-app-authentication-app-service#3-configure-authentication-and-authorization" target="_blank"> these instructions</a>.
***REMOVED******REMOVED******REMOVED***</h2>
***REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle} style={{fontSize: "20px"}}><strong>Authentication configuration takes a few minutes to apply. </strong></h2>
***REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle} style={{fontSize: "20px"}}><strong>If you deployed in the last 10 minutes, please wait and reload the page after 10 minutes.</strong></h2>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***) : (
***REMOVED******REMOVED***<Stack horizontal className={styles.chatRoot}>
***REMOVED******REMOVED******REMOVED***<div className={styles.chatContainer}>
***REMOVED******REMOVED******REMOVED***{!messages || messages.length < 1 ? (
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack className={styles.chatEmptyState}>
***REMOVED******REMOVED******REMOVED******REMOVED***<img
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***src={Azure}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.chatIcon}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="true"
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***<h1 className={styles.chatEmptyStateTitle}>Start chatting</h1>
***REMOVED******REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle}>This chatbot is configured to answer your questions</h2>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***) : (
***REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageStream} style={{ marginBottom: isLoading ? "40px" : "0px"}} role="log">
***REMOVED******REMOVED******REMOVED******REMOVED***{messages.map((answer, index) => (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{answer.role === "user" ? (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUser} tabIndex={0}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>{answer.content}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***) : (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer.role === "assistant" ? <div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer: answer.content,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***citations: parseCitationFromMessage(messages[index - 1]),
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onCitationClicked={c => onShowCitation(c)}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div> : answer.role === "error" ? <div className={styles.chatMessageError}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.chatMessageErrorContent}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<ErrorCircleRegular className={styles.errorIcon} style={{color: "rgba(182, 52, 67, 1)"}} />
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span>Error</span>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span className={styles.chatMessageErrorContent}>{answer.content}</span>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div> : null
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</>
***REMOVED******REMOVED******REMOVED******REMOVED***))}
***REMOVED******REMOVED******REMOVED******REMOVED***{showLoadingMessage && (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer: "Generating answer...",
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***citations: []
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onCitationClicked={() => null}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</>
***REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED***<div ref={chatMessageStreamEnd} />
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***)}

***REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.chatInput}>
***REMOVED******REMOVED******REMOVED******REMOVED***{isLoading && (
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***horizontal
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.stopGeneratingContainer}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Stop generating"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={stopGenerating}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? stopGenerating() : null}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<SquareRegular className={styles.stopGeneratingIcon} aria-hidden="true"/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span className={styles.stopGeneratingText} aria-hidden="true">Stop generating</span>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***{appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured && <CommandBarButton
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***styles={{ 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***icon: { 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***color: '#FFFFFF',
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***root: {
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***color: '#FFFFFF',
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***background: "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***rootDisabled: {
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***background: "#BDBDBD"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.newChatIcon}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'Add' }}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={newChat}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***disabled={disabledButton()}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label="start a new chat button"
***REMOVED******REMOVED******REMOVED******REMOVED***/>}
***REMOVED******REMOVED******REMOVED******REMOVED***<CommandBarButton
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***styles={{ 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***icon: { 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***color: '#FFFFFF',
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***root: {
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***color: '#FFFFFF',
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***background: disabledButton() ? "#BDBDBD" : "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)",
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***cursor: disabledButton() ? "" : "pointer"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured ? styles.clearChatBroom : styles.clearChatBroomNoCosmos}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'Broom' }}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured ? clearChat : newChat}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***disabled={disabledButton()}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label="clear chat button"
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***<Dialog
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***hidden={hideErrorDialog}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onDismiss={handleErrorDialogClose}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***dialogContentProps={errorDialogContentProps}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***modalProps={modalProps}
***REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED***</Dialog>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***<QuestionInput
***REMOVED******REMOVED******REMOVED******REMOVED***clearOnSend
***REMOVED******REMOVED******REMOVED******REMOVED***placeholder="Type a new question..."
***REMOVED******REMOVED******REMOVED******REMOVED***disabled={isLoading}
***REMOVED******REMOVED******REMOVED******REMOVED***onSend={(question, id) => {
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***appStateContext?.state.isCosmosDBAvailable?.cosmosDB ? makeApiRequestWithCosmosDB(question, id) : makeApiRequestWithoutCosmosDB(question, id)
***REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED***conversationId={appStateContext?.state.currentChat?.id ? appStateContext?.state.currentChat?.id : undefined}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***{messages && messages.length > 0 && isCitationPanelOpen && activeCitation && (
***REMOVED******REMOVED******REMOVED***<Stack.Item className={styles.citationPanel} tabIndex={0} role="tabpanel" aria-label="Citations Panel">
***REMOVED******REMOVED******REMOVED***<Stack aria-label="Citations Panel Header Container" horizontal className={styles.citationPanelHeaderContainer} horizontalAlign="space-between" verticalAlign="center">
***REMOVED******REMOVED******REMOVED******REMOVED***<span aria-label="Citations" className={styles.citationPanelHeader}>Citations</span>
***REMOVED******REMOVED******REMOVED******REMOVED***<IconButton iconProps={{ iconName: 'Cancel'}} aria-label="Close citations panel" onClick={() => setIsCitationPanelOpen(false)}/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***<h5 className={styles.citationPanelTitle} tabIndex={0}>{activeCitation[2]}</h5>
***REMOVED******REMOVED******REMOVED***<div tabIndex={0}> 
***REMOVED******REMOVED******REMOVED***<ReactMarkdown 
***REMOVED******REMOVED******REMOVED******REMOVED***linkTarget="_blank"
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.citationPanelContent}
***REMOVED******REMOVED******REMOVED******REMOVED***children={activeCitation[0]} 
***REMOVED******REMOVED******REMOVED******REMOVED***remarkPlugins={[remarkGfm]} 
***REMOVED******REMOVED******REMOVED******REMOVED***rehypePlugins={[rehypeRaw]}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***{(appStateContext?.state.isChatHistoryOpen && appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured) && <ChatHistoryPanel/>}
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***)}
***REMOVED***</div>
***REMOVED***);
};

export default Chat;
