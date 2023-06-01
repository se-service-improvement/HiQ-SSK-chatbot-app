import { useRef, useState, useEffect } from "react";
import { Stack } from "@fluentui/react";
import { BroomRegular, DismissRegular, SquareRegular } from "@fluentui/react-icons";

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
***REMOVED***ChatResponse
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
***REMOVED******REMOVED***messages: [...answers, userMessage]
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
***REMOVED******REMOVED******REMOVED***const objects = text.split("<newline>");
***REMOVED******REMOVED******REMOVED***objects.forEach((obj) => {
***REMOVED******REMOVED******REMOVED***try {
***REMOVED******REMOVED******REMOVED******REMOVED***runningText += obj;
***REMOVED******REMOVED******REMOVED******REMOVED***result = JSON.parse(runningText);
***REMOVED******REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false);
***REMOVED******REMOVED******REMOVED******REMOVED***setAnswers([...answers, userMessage, ...result.choices[0].messages]);
***REMOVED******REMOVED******REMOVED******REMOVED***runningText = "";
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***catch {
***REMOVED******REMOVED******REMOVED******REMOVED***console.log(runningText);
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED***);
***REMOVED******REMOVED***
***REMOVED******REMOVED***setAnswers([...answers, userMessage, ...result.choices[0].messages]);
***REMOVED***
***REMOVED******REMOVED***
***REMOVED*** catch ( e )  {
***REMOVED******REMOVED***if (!abortController.signal.aborted) {
***REMOVED******REMOVED***console.log(result);
***REMOVED******REMOVED***alert("An error occurred. Please try again. If the problem persists, please contact the site administrator.")
***REMOVED***
***REMOVED******REMOVED***setAnswers([...answers, userMessage]);
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
***REMOVED***<div className={styles.container}>
***REMOVED******REMOVED***<Stack horizontal className={styles.chatRoot}>
***REMOVED******REMOVED***<div className={styles.chatContainer}>
***REMOVED******REMOVED******REMOVED***{!lastQuestionRef.current ? (
***REMOVED******REMOVED******REMOVED***<Stack className={styles.chatEmptyState}>
***REMOVED******REMOVED******REMOVED******REMOVED***<img
***REMOVED******REMOVED******REMOVED******REMOVED***src={Azure}
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.chatIcon}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="true"
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***<h1 className={styles.chatEmptyStateTitle}>Start chatting</h1>
***REMOVED******REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle}>This chatbot is configured to answer your questions</h2>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***) : (
***REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageStream} style={{ marginBottom: isLoading ? "40px" : "0px"}}>
***REMOVED******REMOVED******REMOVED******REMOVED***{answers.map((answer, index) => (
***REMOVED******REMOVED******REMOVED******REMOVED***<>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{answer.role === "user" ? (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUser}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>{answer.content}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***) : (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer.role === "assistant" ? <div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer: answer.content,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***citations: parseCitationFromMessage(answers[index - 1]),
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onCitationClicked={c => onShowCitation(c)}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div> : null
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED***</>
***REMOVED******REMOVED******REMOVED******REMOVED***))}
***REMOVED******REMOVED******REMOVED******REMOVED***{showLoadingMessage && (
***REMOVED******REMOVED******REMOVED******REMOVED***<>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUser}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>{lastQuestionRef.current}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer: "Generating answer...",
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***citations: []
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onCitationClicked={() => null}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</>
***REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED***<div ref={chatMessageStreamEnd} />
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***)}

***REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.chatInput}>
***REMOVED******REMOVED******REMOVED***{isLoading && (
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack 
***REMOVED******REMOVED******REMOVED******REMOVED***horizontal
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.stopGeneratingContainer}
***REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Stop generating"
***REMOVED******REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={stopGenerating}
***REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? stopGenerating() : null}
***REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<SquareRegular className={styles.stopGeneratingIcon} aria-hidden="true"/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span className={styles.stopGeneratingText} aria-hidden="true">Stop generating</span>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***<BroomRegular
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.clearChatBroom}
***REMOVED******REMOVED******REMOVED******REMOVED***style={{ background: isLoading || answers.length === 0 ? "#BDBDBD" : "radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)", 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED*** cursor: isLoading || answers.length === 0 ? "" : "pointer"}}
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={clearChat}
***REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? clearChat() : null}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Clear session"
***REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***<QuestionInput
***REMOVED******REMOVED******REMOVED******REMOVED***clearOnSend
***REMOVED******REMOVED******REMOVED******REMOVED***placeholder="Type a new question..."
***REMOVED******REMOVED******REMOVED******REMOVED***disabled={isLoading}
***REMOVED******REMOVED******REMOVED******REMOVED***onSend={question => makeApiRequest(question)}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***{answers.length > 0 && isCitationPanelOpen && activeCitation && (
***REMOVED******REMOVED***<Stack.Item className={styles.citationPanel}>
***REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.citationPanelHeaderContainer} horizontalAlign="space-between" verticalAlign="center">
***REMOVED******REMOVED******REMOVED***<span className={styles.citationPanelHeader}>Citations</span>
***REMOVED******REMOVED******REMOVED***<DismissRegular className={styles.citationPanelDismiss} onClick={() => setIsCitationPanelOpen(false)}/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***<h5 className={styles.citationPanelTitle}>{activeCitation[2]}</h5>
***REMOVED******REMOVED******REMOVED***<ReactMarkdown className={styles.citationPanelContent} children={activeCitation[0]} remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeRaw]}/>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***
***REMOVED***</div>
***REMOVED***);
};

export default Chat;
