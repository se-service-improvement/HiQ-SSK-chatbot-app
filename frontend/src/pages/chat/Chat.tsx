import { useRef, useState, useEffect } from "react";
import { Stack } from "@fluentui/react";
import { BroomRegular, DismissRegular, SquareRegular, ShieldLockRegular, ErrorCircleRegular } from "@fluentui/react-icons";

import ReactMarkdown from "react-markdown";
import remarkGfm from 'remark-gfm'
import rehypeRaw from "rehype-raw"; 

import styles from "./Chat.module.css";
import Azure from "../../assets/Azure.svg";

import {
***REMOVED***ChatMessage,
***REMOVED***ConversationRequest,
***REMOVED***conversationApi,
***REMOVED***Citation,
***REMOVED***ToolMessageContent,
***REMOVED***ChatResponse,
***REMOVED***getUserInfo
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";

const Chat = () => {
***REMOVED***const lastQuestionRef = useRef<string>("");
***REMOVED***const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);
***REMOVED***const [isLoading, setIsLoading] = useState<boolean>(false);
***REMOVED***const [showLoadingMessage, setShowLoadingMessage] = useState<boolean>(false);
***REMOVED***const [activeCitation, setActiveCitation] = useState<[content: string, id: string, title: string, filepath: string, url: string, metadata: string]>();
***REMOVED***const [isCitationPanelOpen, setIsCitationPanelOpen] = useState<boolean>(false);
***REMOVED***const [answers, setAnswers] = useState<ChatMessage[]>([]);
***REMOVED***const abortFuncs = useRef([] as AbortController[]);
***REMOVED***const [showAuthMessage, setShowAuthMessage] = useState<boolean>(true);
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

***REMOVED***const makeApiRequest = async (question: string) => {
***REMOVED***lastQuestionRef.current = question;

***REMOVED***setIsLoading(true);
***REMOVED***setShowLoadingMessage(true);
***REMOVED***const abortController = new AbortController();
***REMOVED***abortFuncs.current.unshift(abortController);

***REMOVED***const userMessage: ChatMessage = {
***REMOVED******REMOVED***role: "user",
***REMOVED******REMOVED***content: question
***REMOVED***;

***REMOVED***const request: ConversationRequest = {
***REMOVED******REMOVED***messages: [...answers.filter((answer) => answer.role !== "error"), userMessage]
***REMOVED***;

***REMOVED***let result = {} as ChatResponse;
***REMOVED***try {
***REMOVED******REMOVED***const response = await conversationApi(request, abortController.signal);
***REMOVED******REMOVED***if (response?.body) {
***REMOVED******REMOVED***
***REMOVED******REMOVED***const reader = response.body.getReader();
***REMOVED******REMOVED***let runningText = "";
***REMOVED******REMOVED***while (true) {
***REMOVED******REMOVED******REMOVED***const {done, value} = await reader.read();
***REMOVED******REMOVED******REMOVED***if (done) break;

***REMOVED******REMOVED******REMOVED***var text = new TextDecoder("utf-8").decode(value);
***REMOVED******REMOVED******REMOVED***const objects = text.split("\n");
***REMOVED******REMOVED******REMOVED***objects.forEach((obj) => {
***REMOVED******REMOVED******REMOVED***try {
***REMOVED******REMOVED******REMOVED******REMOVED***runningText += obj;
***REMOVED******REMOVED******REMOVED******REMOVED***result = JSON.parse(runningText);
***REMOVED******REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED******REMOVED***setAnswers([...answers, userMessage, ...result.choices[0].messages]);
***REMOVED******REMOVED******REMOVED******REMOVED***runningText = "";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***catch { }
***REMOVED******REMOVED***);
***REMOVED******REMOVED***
***REMOVED******REMOVED***setAnswers([...answers, userMessage, ...result.choices[0].messages]);
***REMOVED***
***REMOVED******REMOVED***
***REMOVED*** catch ( e )  {
***REMOVED******REMOVED***if (!abortController.signal.aborted) {
***REMOVED******REMOVED***console.error(result);
***REMOVED******REMOVED***let errorMessage = "An error occurred. Please try again. If the problem persists, please contact the site administrator.";
***REMOVED******REMOVED***if (result.error?.message) {
***REMOVED******REMOVED******REMOVED***errorMessage = result.error.message;
***REMOVED******REMOVED***
***REMOVED******REMOVED***else if (typeof result.error === "string") {
***REMOVED******REMOVED******REMOVED***errorMessage = result.error;
***REMOVED******REMOVED***
***REMOVED******REMOVED***setAnswers([...answers, userMessage, {
***REMOVED******REMOVED******REMOVED***role: "error",
***REMOVED******REMOVED******REMOVED***content: errorMessage
***REMOVED******REMOVED***]);
***REMOVED******REMOVED***
***REMOVED******REMOVED***setAnswers([...answers, userMessage]);
***REMOVED***
***REMOVED*** finally {
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController);
***REMOVED***

***REMOVED***return abortController.abort();
***REMOVED***;

***REMOVED***const clearChat = () => {
***REMOVED***lastQuestionRef.current = "";
***REMOVED***setActiveCitation(undefined);
***REMOVED***setAnswers([]);
***REMOVED***;

***REMOVED***const stopGenerating = () => {
***REMOVED***abortFuncs.current.forEach(a => a.abort());
***REMOVED***setShowLoadingMessage(false);
***REMOVED***setIsLoading(false);
***REMOVED***

***REMOVED***useEffect(() => {
***REMOVED***getUserInfoList();
***REMOVED***, []);

***REMOVED***useEffect(() => chatMessageStreamEnd.current?.scrollIntoView({ behavior: "smooth" }), [showLoadingMessage]);

***REMOVED***const onShowCitation = (citation: Citation) => {
***REMOVED***setActiveCitation([citation.content, citation.id, citation.title ?? "", citation.filepath ?? "", "", ""]);
***REMOVED***setIsCitationPanelOpen(true);
***REMOVED***;

***REMOVED***const parseCitationFromMessage = (message: ChatMessage) => {
***REMOVED***if (message.role === "tool") {
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
***REMOVED******REMOVED******REMOVED***{!lastQuestionRef.current ? (
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
***REMOVED******REMOVED******REMOVED******REMOVED***{answers.map((answer, index) => (
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
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***citations: parseCitationFromMessage(answers[index - 1]),
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
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUser}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>{lastQuestionRef.current}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
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
***REMOVED******REMOVED******REMOVED******REMOVED***<div
***REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={clearChat}
***REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? clearChat() : null}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Clear session"
***REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED***<BroomRegular
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.clearChatBroom}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***style={{ background: isLoading || answers.length === 0 ? "#BDBDBD" : "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)", 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***cursor: isLoading || answers.length === 0 ? "" : "pointer"}}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="true"
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***<QuestionInput
***REMOVED******REMOVED******REMOVED******REMOVED***clearOnSend
***REMOVED******REMOVED******REMOVED******REMOVED***placeholder="Type a new question..."
***REMOVED******REMOVED******REMOVED******REMOVED***disabled={isLoading}
***REMOVED******REMOVED******REMOVED******REMOVED***onSend={question => makeApiRequest(question)}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***{answers.length > 0 && isCitationPanelOpen && activeCitation && (
***REMOVED******REMOVED******REMOVED***<Stack.Item className={styles.citationPanel} tabIndex={0} role="tabpanel" aria-label="Citations Panel">
***REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.citationPanelHeaderContainer} horizontalAlign="space-between" verticalAlign="center">
***REMOVED******REMOVED******REMOVED******REMOVED***<span className={styles.citationPanelHeader}>Citations</span>
***REMOVED******REMOVED******REMOVED******REMOVED***<DismissRegular className={styles.citationPanelDismiss} onClick={() => setIsCitationPanelOpen(false)}/>
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
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***)}
***REMOVED***</div>
***REMOVED***);
};

export default Chat;
