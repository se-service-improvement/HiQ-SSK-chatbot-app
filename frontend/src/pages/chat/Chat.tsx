import { useRef, useState, useEffect } from "react";
import { Stack } from "@fluentui/react";
import { BroomRegular, DismissRegular, SquareRegular } from "@fluentui/react-icons";

import styles from "./Chat.module.css";
import Sparkle from "../../assets/sparkle.svg";
import {
***REMOVED***ChatMessage,
***REMOVED***ConversationRequest,
***REMOVED***conversationApi,
***REMOVED***MessageContent,
***REMOVED***DocumentResult
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";

const Chat = () => {
***REMOVED***const lastQuestionRef = useRef<string>("");
***REMOVED***const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);
***REMOVED***const [isLoading, setIsLoading] = useState<boolean>(false);
***REMOVED***const [activeCitation, setActiveCitation] = useState<[content: string, id: string, title: string, filepath: string, url: string, metadata: string]>();
***REMOVED***const [isCitationPanelOpen, setIsCitationPanelOpen] = useState<boolean>(false);
***REMOVED***const [answers, setAnswers] = useState<[message_id: string, parent_message_id: string, role: string, content: MessageContent][]>([]);
***REMOVED***const abortFuncs = useRef([] as AbortController[]);

***REMOVED***const makeApiRequest = async (question: string) => {
***REMOVED***lastQuestionRef.current = question;

***REMOVED***setIsLoading(true);
***REMOVED***setActiveCitation(undefined);
***REMOVED***setIsCitationPanelOpen(false);
***REMOVED***const abortController = new AbortController();
***REMOVED***abortFuncs.current.unshift(abortController);

***REMOVED***const prevMessages: ChatMessage[] = answers.map(a => ({
***REMOVED******REMOVED***message_id: a[0],
***REMOVED******REMOVED***parent_message_id: a[1] ?? "",
***REMOVED******REMOVED***role: a[2],
***REMOVED******REMOVED***content: a[3]
***REMOVED***));
***REMOVED***const userMessage: ChatMessage = {
***REMOVED******REMOVED***message_id: crypto.randomUUID(),
***REMOVED******REMOVED***parent_message_id: prevMessages.length > 0 ? prevMessages[prevMessages.length - 1].message_id : "",
***REMOVED******REMOVED***role: "user",
***REMOVED******REMOVED***content: {
***REMOVED******REMOVED***content_type: "text",
***REMOVED******REMOVED***parts: [question],
***REMOVED******REMOVED***top_docs: [],
***REMOVED******REMOVED***intent: ""
***REMOVED***
***REMOVED***;

***REMOVED***const request: ConversationRequest = {
***REMOVED******REMOVED***messages: [...prevMessages, userMessage]
***REMOVED***;

***REMOVED***try {
***REMOVED******REMOVED***const result = await conversationApi(request, abortController.signal);
***REMOVED******REMOVED***setAnswers([
***REMOVED******REMOVED***...answers,
***REMOVED******REMOVED***[userMessage.message_id, userMessage.parent_message_id ?? "", userMessage.role, userMessage.content],
***REMOVED******REMOVED***[result.message_id, result.parent_message_id ?? "", result.role, result.content]
***REMOVED******REMOVED***]);
***REMOVED*** catch {
***REMOVED******REMOVED***setAnswers([
***REMOVED******REMOVED***...answers,
***REMOVED******REMOVED***[userMessage.message_id, userMessage.parent_message_id ?? "", userMessage.role, userMessage.content]
***REMOVED******REMOVED***]);
***REMOVED*** finally {
***REMOVED******REMOVED***setIsLoading(false);
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
***REMOVED***setIsLoading(false);
***REMOVED***

***REMOVED***useEffect(() => chatMessageStreamEnd.current?.scrollIntoView({ behavior: "smooth" }), [isLoading]);

***REMOVED***const onShowCitation = (citation: DocumentResult, index: number) => {
***REMOVED***if (activeCitation && activeCitation[1] === citation.id && isCitationPanelOpen) {
***REMOVED******REMOVED***setIsCitationPanelOpen(false);
***REMOVED***
***REMOVED******REMOVED***setActiveCitation([citation.content, citation.id, citation.title ?? "", citation.filepath ?? "", "", ""]);
***REMOVED******REMOVED***setIsCitationPanelOpen(true);
***REMOVED***
***REMOVED***;

***REMOVED***return (
***REMOVED***<div className={styles.container}>
***REMOVED******REMOVED***<Stack horizontal className={styles.chatRoot}>
***REMOVED******REMOVED***<div className={styles.chatContainer}>
***REMOVED******REMOVED******REMOVED***{!lastQuestionRef.current ? (
***REMOVED******REMOVED******REMOVED***<Stack className={styles.chatEmptyState}>
***REMOVED******REMOVED******REMOVED******REMOVED***<img
***REMOVED******REMOVED******REMOVED******REMOVED***src={Sparkle}
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.chatSparkleIcon}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="true"
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***<h1 className={styles.chatEmptyStateTitle}>Start chatting</h1>
***REMOVED******REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle}>This chatbot is configured to answer your questions.</h2>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***) : (
***REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageStream}>
***REMOVED******REMOVED******REMOVED******REMOVED***{answers.map((answer, index) => (
***REMOVED******REMOVED******REMOVED******REMOVED***<>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{answer[2] === "user" ? (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUser}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>{answer[3].parts[0]}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***) : (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer: answer[3].parts[0],
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***thoughts: null,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***data_points: [],
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***top_docs: answer[3].top_docs
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onCitationClicked={c => onShowCitation(c, index)}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED***</>
***REMOVED******REMOVED******REMOVED******REMOVED***))}
***REMOVED******REMOVED******REMOVED******REMOVED***{isLoading && (
***REMOVED******REMOVED******REMOVED******REMOVED***<>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUser}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>{lastQuestionRef.current}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***answer: "Generating answer...",
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***thoughts: null,
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***data_points: [],
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***top_docs: []
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
***REMOVED******REMOVED***{!isLoading && answers.length > 0 && isCitationPanelOpen && activeCitation && (
***REMOVED******REMOVED***<Stack.Item className={styles.citationPanel}>
***REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.citationPanelHeaderContainer} horizontalAlign="space-between" verticalAlign="center">
***REMOVED******REMOVED******REMOVED***<span className={styles.citationPanelHeader}>Citations</span>
***REMOVED******REMOVED******REMOVED***<DismissRegular className={styles.citationPanelDismiss} onClick={() => setIsCitationPanelOpen(false)}/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***<h5 className={styles.citationPanelTitle}>{activeCitation[2]}</h5>
***REMOVED******REMOVED******REMOVED***<p className={styles.citationPanelContent} dangerouslySetInnerHTML={{__html: activeCitation[0]}}></p>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***
***REMOVED***</div>
***REMOVED***);
};

export default Chat;
