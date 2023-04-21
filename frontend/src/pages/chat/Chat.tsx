import { useRef, useState, useEffect } from "react";
import { Pivot, PivotItem } from "@fluentui/react";
import { Sparkle28Filled, Sparkle48Filled } from "@fluentui/react-icons";

import styles from "./Chat.module.css";

import {
***REMOVED***ChatMessage,
***REMOVED***ConversationRequest,
***REMOVED***conversationApi,
***REMOVED***MessageContent,
***REMOVED***DocumentResult
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
import { SupportingContent } from "../../components/SupportingContent";
import { ClearChatButton } from "../../components/ClearChatButton";

enum Tabs {
***REMOVED***SupportingContentTab = "supportingContent",
***REMOVED***CitationTab = "citation"
}

const Chat = () => {
***REMOVED***const lastQuestionRef = useRef<string>("");
***REMOVED***const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null);

***REMOVED***const [isLoading, setIsLoading] = useState<boolean>(false);

***REMOVED***const [activeCitation, setActiveCitation] = useState<[content: string, id: string, title: string, filepath: string, url: string, metadata: string]>();
***REMOVED***const [activeTab, setActiveTab] = useState<Tabs | undefined>(undefined);

***REMOVED***const [currentAnswer, setCurrentAnswer] = useState<number>(0);
***REMOVED***const [answers, setAnswers] = useState<[message_id: string, parent_message_id: string, role: string, content: MessageContent][]>(
***REMOVED***[]
***REMOVED***);

***REMOVED***const makeApiRequest = async (question: string) => {
***REMOVED***lastQuestionRef.current = question;

***REMOVED***setIsLoading(true);
***REMOVED***setActiveCitation(undefined);
***REMOVED***setActiveTab(undefined);

***REMOVED***try {
***REMOVED******REMOVED***const prevMessages: ChatMessage[] = answers.map(a => ({
***REMOVED******REMOVED***message_id: a[0],
***REMOVED******REMOVED***parent_message_id: a[1] ?? "",
***REMOVED******REMOVED***role: a[2],
***REMOVED******REMOVED***content: a[3]
***REMOVED***));
***REMOVED******REMOVED***const userMessage: ChatMessage = {
***REMOVED******REMOVED***message_id: crypto.randomUUID(),
***REMOVED******REMOVED***parent_message_id: prevMessages.length > 0 ? prevMessages[prevMessages.length - 1].message_id : "",
***REMOVED******REMOVED***role: "user",
***REMOVED******REMOVED***content: {
***REMOVED******REMOVED******REMOVED***content_type: "text",
***REMOVED******REMOVED******REMOVED***parts: [question],
***REMOVED******REMOVED******REMOVED***top_docs: [],
***REMOVED******REMOVED******REMOVED***intent: ""
***REMOVED******REMOVED***
***REMOVED***;

***REMOVED******REMOVED***const request: ConversationRequest = {
***REMOVED******REMOVED***messages: [...prevMessages, userMessage]
***REMOVED***;

***REMOVED******REMOVED***const result = await conversationApi(request);

***REMOVED******REMOVED***setAnswers([
***REMOVED******REMOVED***...answers,
***REMOVED******REMOVED***[userMessage.message_id, userMessage.parent_message_id ?? "", userMessage.role, userMessage.content],
***REMOVED******REMOVED***[result.message_id, result.parent_message_id ?? "", result.role, result.content]
***REMOVED******REMOVED***]);
***REMOVED*** finally {
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED***
***REMOVED***;

***REMOVED***const clearChat = () => {
***REMOVED***lastQuestionRef.current = "";
***REMOVED***setActiveCitation(undefined);
***REMOVED***setAnswers([]);
***REMOVED***;

***REMOVED***useEffect(() => chatMessageStreamEnd.current?.scrollIntoView({ behavior: "smooth" }), [isLoading]);

***REMOVED***const onShowCitation = (citation: DocumentResult, index: number) => {
***REMOVED***setCurrentAnswer(index);
***REMOVED***if (activeCitation && activeCitation[1] === citation.id && activeTab === Tabs.CitationTab) {
***REMOVED******REMOVED***setActiveTab(undefined);
***REMOVED***
***REMOVED******REMOVED***setActiveCitation([citation.content, citation.id, citation.title ?? "", citation.filepath ?? "", "", ""]);
***REMOVED******REMOVED***setActiveTab(Tabs.CitationTab);
***REMOVED***
***REMOVED***;

***REMOVED***const isDisabledCitationTab: boolean = !activeCitation;

***REMOVED***return (
***REMOVED***<div className={styles.container}>
***REMOVED******REMOVED***<div className={styles.commandsContainer}>
***REMOVED******REMOVED***<ClearChatButton className={styles.commandButton} onClick={clearChat} disabled={!lastQuestionRef.current || isLoading} />
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***<div className={styles.chatRoot}>
***REMOVED******REMOVED***<div className={styles.chatContainer}>
***REMOVED******REMOVED******REMOVED***{!lastQuestionRef.current ? (
***REMOVED******REMOVED******REMOVED***<div className={styles.chatEmptyState}>
***REMOVED******REMOVED******REMOVED******REMOVED***<Sparkle48Filled aria-hidden="true" className={styles.chatSparkleIcon}/>
***REMOVED******REMOVED******REMOVED******REMOVED***<h1 className={styles.chatEmptyStateTitle}>Start chatting</h1>
***REMOVED******REMOVED******REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle}>This chatbot is configured to answer your questions.</h2>
***REMOVED******REMOVED******REMOVED***</div>
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
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageGptLoading}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Sparkle28Filled aria-hidden="true" aria-label="Answer logo" />
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<p>Generating answer...</p>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED******REMOVED***</>
***REMOVED******REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED******REMOVED***<div ref={chatMessageStreamEnd} />
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***)}

***REMOVED******REMOVED******REMOVED***<div className={styles.chatInput}>
***REMOVED******REMOVED******REMOVED***<QuestionInput
***REMOVED******REMOVED******REMOVED******REMOVED***clearOnSend
***REMOVED******REMOVED******REMOVED******REMOVED***placeholder="Type a new question..."
***REMOVED******REMOVED******REMOVED******REMOVED***disabled={isLoading}
***REMOVED******REMOVED******REMOVED******REMOVED***onSend={question => makeApiRequest(question)}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***</div>

***REMOVED******REMOVED***{!isLoading && answers.length > 0 && activeTab && (
***REMOVED******REMOVED******REMOVED***<Pivot
***REMOVED******REMOVED******REMOVED***className={styles.chatAnalysisPanel}
***REMOVED******REMOVED******REMOVED***selectedKey={activeTab}
***REMOVED******REMOVED******REMOVED***onLinkClick={pivotItem => pivotItem && setActiveTab(pivotItem.props.itemKey! as Tabs)}
***REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED***<PivotItem
***REMOVED******REMOVED******REMOVED******REMOVED***itemKey={Tabs.CitationTab}
***REMOVED******REMOVED******REMOVED******REMOVED***headerText="Citation"
***REMOVED******REMOVED******REMOVED******REMOVED***headerButtonProps={isDisabledCitationTab ? { disabled: true, style: { color: "grey" } } : undefined}
***REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED***{ activeCitation && <SupportingContent supportingContent={{
***REMOVED******REMOVED******REMOVED******REMOVED***content: activeCitation[0], 
***REMOVED******REMOVED******REMOVED******REMOVED***id: activeCitation[1],
***REMOVED******REMOVED******REMOVED******REMOVED***title: activeCitation[2],
***REMOVED******REMOVED******REMOVED******REMOVED***filepath: activeCitation[3],
***REMOVED******REMOVED******REMOVED******REMOVED***url: activeCitation[4],
***REMOVED******REMOVED******REMOVED******REMOVED***metadata: activeCitation[5]
***REMOVED******REMOVED******REMOVED***} />}
***REMOVED******REMOVED******REMOVED***</PivotItem>
***REMOVED******REMOVED******REMOVED***</Pivot>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***</div>
***REMOVED***</div>
***REMOVED***);
};

export default Chat;
