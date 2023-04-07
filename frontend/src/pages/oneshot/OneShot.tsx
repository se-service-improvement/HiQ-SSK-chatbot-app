import { useRef, useState } from "react";
import { Pivot, PivotItem, Spinner} from "@fluentui/react";

import styles from "./OneShot.module.css";

import { 
***REMOVED***ChatMessage, 
***REMOVED***ConversationRequest, 
***REMOVED***conversationApi, 
***REMOVED***MessageContent, 
***REMOVED***FeedbackString, 
***REMOVED***FeedbackRequest, 
***REMOVED***feedbackApi, 
***REMOVED***DocumentResult 
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
import { SupportingContent } from "../../components/SupportingContent";

enum Tabs {
***REMOVED***ThoughtProcessTab = "thoughtProcess",
***REMOVED***SupportingContentTab = "supportingContent",
***REMOVED***CitationTab = "citation"
}

const OneShot = () => {
***REMOVED***const lastQuestionRef = useRef<string>("");

***REMOVED***const [error, setError] = useState<unknown>();
***REMOVED***const [isLoading, setIsLoading] = useState<boolean>(false);
***REMOVED***const [answer, setAnswer] = useState<[message_id: string, parent_message_id: string, role: string, content: MessageContent, feedback: FeedbackString]>();
***REMOVED***const [activeCitation, setActiveCitation] = useState<[content: string, id: string, title: string, filepath: string, url: string, metadata: string]>();
***REMOVED***const [activeTab, setActiveTab] = useState<Tabs | undefined>(undefined);

***REMOVED***const makeApiRequest = async (question: string) => {
***REMOVED***lastQuestionRef.current = question;

***REMOVED***error && setError(undefined);

***REMOVED***setIsLoading(true);
***REMOVED***setActiveCitation(undefined);
***REMOVED***setActiveTab(undefined);

***REMOVED***try {
***REMOVED******REMOVED***
***REMOVED******REMOVED***const userMessage: ChatMessage = {
***REMOVED******REMOVED***message_id: crypto.randomUUID(),
***REMOVED******REMOVED***parent_message_id: "", 
***REMOVED******REMOVED***role: "user",
***REMOVED******REMOVED***content: {
***REMOVED******REMOVED******REMOVED***content_type: "text",
***REMOVED******REMOVED******REMOVED***parts: [question],
***REMOVED******REMOVED******REMOVED***top_docs: [],
***REMOVED******REMOVED******REMOVED***intent: ""
***REMOVED******REMOVED***
***REMOVED***;

***REMOVED******REMOVED***const request: ConversationRequest = {
***REMOVED******REMOVED***messages: [userMessage]
***REMOVED***;

***REMOVED******REMOVED***const result = await conversationApi(request);

***REMOVED******REMOVED***setAnswer([result.message_id, result.parent_message_id ?? "", result.role, result.content, FeedbackString.Neutral]);
***REMOVED*** finally {
***REMOVED******REMOVED***setIsLoading(false);
***REMOVED***
***REMOVED***;

***REMOVED***const makeFeedbackRequest = async (message_id: string, feedback: FeedbackString) => {
***REMOVED***const request: FeedbackRequest = {
***REMOVED******REMOVED***message_id: message_id,
***REMOVED******REMOVED***feedback: feedback
***REMOVED***;

***REMOVED***await feedbackApi(request);

***REMOVED***return;
***REMOVED***;

***REMOVED***const onShowCitation = (citation: DocumentResult) => {
***REMOVED***if (activeCitation && activeCitation[1] === citation.id && activeTab === Tabs.CitationTab) {
***REMOVED******REMOVED***setActiveTab(undefined);
***REMOVED***
***REMOVED******REMOVED***setActiveCitation([citation.content, citation.id, citation.title ?? "", citation.filepath ?? "", "", ""]);
***REMOVED******REMOVED***setActiveTab(Tabs.CitationTab);
***REMOVED***
***REMOVED***;

***REMOVED***const onToggleTab = (tab: Tabs) => {
***REMOVED***if (activeTab === tab) {
***REMOVED******REMOVED***setActiveTab(undefined);
***REMOVED***
***REMOVED******REMOVED***setActiveTab(tab);
***REMOVED***
***REMOVED***;

***REMOVED***const onLikeResponse = () => {
***REMOVED***if (answer) {
***REMOVED******REMOVED***let newFeedback = answer[4] === FeedbackString.ThumbsUp ? FeedbackString.Neutral : FeedbackString.ThumbsUp;
***REMOVED******REMOVED***setAnswer([answer[0], answer[1], answer[2], answer[3], newFeedback]);
***REMOVED******REMOVED***if (newFeedback === FeedbackString.ThumbsUp) {
***REMOVED******REMOVED***makeFeedbackRequest(answer[0], newFeedback);
***REMOVED***
***REMOVED******REMOVED***console.log("Liked response");
***REMOVED***
***REMOVED***;

***REMOVED***const onDislikeResponse = () => {
***REMOVED***if (answer) {
***REMOVED******REMOVED***let newFeedback = answer[4] === FeedbackString.ThumbsDown ? FeedbackString.Neutral : FeedbackString.ThumbsDown;
***REMOVED******REMOVED***setAnswer([answer[0], answer[1], answer[2], answer[3], newFeedback]);
***REMOVED******REMOVED***if (newFeedback === FeedbackString.ThumbsDown) {
***REMOVED******REMOVED***makeFeedbackRequest(answer[0], newFeedback);
***REMOVED***
***REMOVED******REMOVED***console.log("Disliked response");
***REMOVED***
***REMOVED***;

***REMOVED***const isDisabledCitationTab: boolean = !activeCitation;

***REMOVED***return (
***REMOVED***<div className={styles.oneshotContainer}>
***REMOVED******REMOVED***<div className={styles.oneshotTopSection}>
***REMOVED******REMOVED***<h1 className={styles.oneshotTitle}>Ask your data</h1>
***REMOVED******REMOVED***<div className={styles.oneshotQuestionInput}>
***REMOVED******REMOVED******REMOVED***<QuestionInput
***REMOVED******REMOVED******REMOVED***placeholder={!lastQuestionRef.current ? "Type your question here" : lastQuestionRef.current}
***REMOVED******REMOVED******REMOVED***disabled={isLoading}
***REMOVED******REMOVED******REMOVED***onSend={question => makeApiRequest(question)}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***<div className={styles.oneshotBottomSection}>
***REMOVED******REMOVED***{isLoading && <Spinner label="Generating answer" />}
***REMOVED******REMOVED***{!isLoading && answer && ( 
***REMOVED******REMOVED******REMOVED***<div className={styles.oneshotAnswerContainer}>
***REMOVED******REMOVED******REMOVED***<Answer
***REMOVED******REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED******REMOVED***answer: answer[3].parts[0],
***REMOVED******REMOVED******REMOVED******REMOVED***thoughts: null,
***REMOVED******REMOVED******REMOVED******REMOVED***data_points: [],
***REMOVED******REMOVED******REMOVED******REMOVED***feedback: answer[4],
***REMOVED******REMOVED******REMOVED******REMOVED***top_docs: answer[3].top_docs
***REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED******REMOVED***onCitationClicked={x => onShowCitation(x)}
***REMOVED******REMOVED******REMOVED******REMOVED***onThoughtProcessClicked={() => onToggleTab(Tabs.ThoughtProcessTab)}
***REMOVED******REMOVED******REMOVED******REMOVED***onSupportingContentClicked={() => onToggleTab(Tabs.SupportingContentTab)}
***REMOVED******REMOVED******REMOVED******REMOVED***onLikeResponseClicked={() => onLikeResponse()}
***REMOVED******REMOVED******REMOVED******REMOVED***onDislikeResponseClicked={() => onDislikeResponse()}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***{!isLoading && answer && activeTab && (
***REMOVED******REMOVED******REMOVED***<Pivot
***REMOVED******REMOVED******REMOVED***className={styles.oneshotAnalysisPanel}
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

export default OneShot;
