import { FormEvent, useEffect, useMemo, useState, useContext } from "react";
import { useBoolean } from "@fluentui/react-hooks"
import { Checkbox, DefaultButton, Dialog, FontIcon, Stack, Text } from "@fluentui/react";
import DOMPurify from 'dompurify';
import { AppStateContext } from '../../state/AppProvider';

import styles from "./Answer.module.css";

import { AskResponse, Citation, Feedback, historyMessageFeedback } from "../../api";
import { parseAnswer } from "./AnswerParser";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import supersub from 'remark-supersub'
import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
import { nord } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { ThumbDislike20Filled, ThumbLike20Filled } from "@fluentui/react-icons";
import { XSSAllowTags } from "../../constants/xssAllowTags";

interface Props {
***REMOVED***answer: AskResponse;
***REMOVED***onCitationClicked: (citedDocument: Citation) => void;
}

export const Answer = ({
***REMOVED***answer,
***REMOVED***onCitationClicked
}: Props) => {
***REMOVED***const initializeAnswerFeedback = (answer: AskResponse) => {
***REMOVED***if (answer.message_id == undefined) return undefined;
***REMOVED***if (answer.feedback == undefined) return undefined;
***REMOVED***if (answer.feedback.split(",").length > 1) return Feedback.Negative;
***REMOVED***if (Object.values(Feedback).includes(answer.feedback)) return answer.feedback;
***REMOVED***return Feedback.Neutral;
***REMOVED***

***REMOVED***const [isRefAccordionOpen, { toggle: toggleIsRefAccordionOpen }] = useBoolean(false);
***REMOVED***const filePathTruncationLimit = 50;

***REMOVED***const parsedAnswer = useMemo(() => parseAnswer(answer), [answer]);
***REMOVED***const [chevronIsExpanded, setChevronIsExpanded] = useState(isRefAccordionOpen);
***REMOVED***const [feedbackState, setFeedbackState] = useState(initializeAnswerFeedback(answer));
***REMOVED***const [isFeedbackDialogOpen, setIsFeedbackDialogOpen] = useState(false);
***REMOVED***const [showReportInappropriateFeedback, setShowReportInappropriateFeedback] = useState(false);
***REMOVED***const [negativeFeedbackList, setNegativeFeedbackList] = useState<Feedback[]>([]);
***REMOVED***const appStateContext = useContext(AppStateContext)
***REMOVED***const FEEDBACK_ENABLED = appStateContext?.state.frontendSettings?.feedback_enabled && appStateContext?.state.isCosmosDBAvailable?.cosmosDB; 
***REMOVED***const SANITIZE_ANSWER = appStateContext?.state.frontendSettings?.sanitize_answer 
***REMOVED***
***REMOVED***const handleChevronClick = () => {
***REMOVED***setChevronIsExpanded(!chevronIsExpanded);
***REMOVED***toggleIsRefAccordionOpen();
***REMOVED***;

***REMOVED***useEffect(() => {
***REMOVED***setChevronIsExpanded(isRefAccordionOpen);
***REMOVED***, [isRefAccordionOpen]);

***REMOVED***useEffect(() => {
***REMOVED***if (answer.message_id == undefined) return;
***REMOVED***
***REMOVED***let currentFeedbackState;
***REMOVED***if (appStateContext?.state.feedbackState && appStateContext?.state.feedbackState[answer.message_id]) {
***REMOVED******REMOVED***currentFeedbackState = appStateContext?.state.feedbackState[answer.message_id];
***REMOVED***
***REMOVED******REMOVED***currentFeedbackState = initializeAnswerFeedback(answer);
***REMOVED***
***REMOVED***setFeedbackState(currentFeedbackState)
***REMOVED***, [appStateContext?.state.feedbackState, feedbackState, answer.message_id]);

***REMOVED***const createCitationFilepath = (citation: Citation, index: number, truncate: boolean = false) => {
***REMOVED***let citationFilename = "";

***REMOVED***if (citation.filepath) {
***REMOVED******REMOVED***const part_i = citation.part_index ?? (citation.chunk_id ? parseInt(citation.chunk_id) + 1 : '');
***REMOVED******REMOVED***if (truncate && citation.filepath.length > filePathTruncationLimit) {
***REMOVED******REMOVED***const citationLength = citation.filepath.length;
***REMOVED******REMOVED***citationFilename = `${citation.filepath.substring(0, 20)}...${citation.filepath.substring(citationLength - 20)} - Part ${part_i}`;
***REMOVED***
***REMOVED******REMOVED***else {
***REMOVED******REMOVED***citationFilename = `${citation.filepath} - Part ${part_i}`;
***REMOVED***
***REMOVED***
***REMOVED***else if (citation.filepath && citation.reindex_id) {
***REMOVED******REMOVED***citationFilename = `${citation.filepath} - Part ${citation.reindex_id}`;
***REMOVED***
***REMOVED***else {
***REMOVED******REMOVED***citationFilename = `Citation ${index}`;
***REMOVED***
***REMOVED***return citationFilename;
***REMOVED***

***REMOVED***const onLikeResponseClicked = async () => {
***REMOVED***if (answer.message_id == undefined) return;

***REMOVED***let newFeedbackState = feedbackState;
***REMOVED***// Set or unset the thumbs up state
***REMOVED***if (feedbackState == Feedback.Positive) {
***REMOVED******REMOVED***newFeedbackState = Feedback.Neutral;
***REMOVED***
***REMOVED***else {
***REMOVED******REMOVED***newFeedbackState = Feedback.Positive;
***REMOVED***
***REMOVED***appStateContext?.dispatch({ type: 'SET_FEEDBACK_STATE', payload: { answerId: answer.message_id, feedback: newFeedbackState } });
***REMOVED***setFeedbackState(newFeedbackState);

***REMOVED***// Update message feedback in db
***REMOVED***await historyMessageFeedback(answer.message_id, newFeedbackState);
***REMOVED***

***REMOVED***const onDislikeResponseClicked = async () => {
***REMOVED***if (answer.message_id == undefined) return;

***REMOVED***let newFeedbackState = feedbackState;
***REMOVED***if (feedbackState === undefined || feedbackState === Feedback.Neutral || feedbackState === Feedback.Positive) {
***REMOVED******REMOVED***newFeedbackState = Feedback.Negative;
***REMOVED******REMOVED***setFeedbackState(newFeedbackState);
***REMOVED******REMOVED***setIsFeedbackDialogOpen(true);
***REMOVED***
***REMOVED******REMOVED***// Reset negative feedback to neutral
***REMOVED******REMOVED***newFeedbackState = Feedback.Neutral;
***REMOVED******REMOVED***setFeedbackState(newFeedbackState);
***REMOVED******REMOVED***await historyMessageFeedback(answer.message_id, Feedback.Neutral);
***REMOVED***
***REMOVED***appStateContext?.dispatch({ type: 'SET_FEEDBACK_STATE', payload: { answerId: answer.message_id, feedback: newFeedbackState }});
***REMOVED***

***REMOVED***const updateFeedbackList = (ev?: FormEvent<HTMLElement | HTMLInputElement>, checked?: boolean) => {
***REMOVED***if (answer.message_id == undefined) return;
***REMOVED***let selectedFeedback = (ev?.target as HTMLInputElement)?.id as Feedback;

***REMOVED***let feedbackList = negativeFeedbackList.slice();
***REMOVED***if (checked) {
***REMOVED******REMOVED***feedbackList.push(selectedFeedback);
***REMOVED***
***REMOVED******REMOVED***feedbackList = feedbackList.filter((f) => f !== selectedFeedback);
***REMOVED***

***REMOVED***setNegativeFeedbackList(feedbackList);
***REMOVED***;

***REMOVED***const onSubmitNegativeFeedback = async () => {
***REMOVED***if (answer.message_id == undefined) return;
***REMOVED***await historyMessageFeedback(answer.message_id, negativeFeedbackList.join(","));
***REMOVED***resetFeedbackDialog();
***REMOVED***

***REMOVED***const resetFeedbackDialog = () => {
***REMOVED***setIsFeedbackDialogOpen(false);
***REMOVED***setShowReportInappropriateFeedback(false);
***REMOVED***setNegativeFeedbackList([]);
***REMOVED***

***REMOVED***const UnhelpfulFeedbackContent = () => {
***REMOVED***return (<>
***REMOVED******REMOVED***<div>Why wasn't this response helpful?</div>
***REMOVED******REMOVED***<Stack tokens={{childrenGap: 4}}>
***REMOVED******REMOVED***<Checkbox label="Citations are missing" id={Feedback.MissingCitation} defaultChecked={negativeFeedbackList.includes(Feedback.MissingCitation)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED***<Checkbox label="Citations are wrong" id={Feedback.WrongCitation} defaultChecked={negativeFeedbackList.includes(Feedback.WrongCitation)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED***<Checkbox label="The response is not from my data" id={Feedback.OutOfScope} defaultChecked={negativeFeedbackList.includes(Feedback.OutOfScope)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED***<Checkbox label="Inaccurate or irrelevant" id={Feedback.InaccurateOrIrrelevant} defaultChecked={negativeFeedbackList.includes(Feedback.InaccurateOrIrrelevant)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED***<Checkbox label="Other" id={Feedback.OtherUnhelpful} defaultChecked={negativeFeedbackList.includes(Feedback.OtherUnhelpful)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***<div onClick={() => setShowReportInappropriateFeedback(true)} style={{ color: "#115EA3", cursor: "pointer"}}>Report inappropriate content</div>
***REMOVED***</>);
***REMOVED***

***REMOVED***const ReportInappropriateFeedbackContent = () => {
***REMOVED***return (
***REMOVED******REMOVED***<>
***REMOVED******REMOVED***<div>The content is <span style={{ color: "red" }} >*</span></div>
***REMOVED******REMOVED***<Stack tokens={{childrenGap: 4}}>
***REMOVED******REMOVED******REMOVED***<Checkbox label="Hate speech, stereotyping, demeaning" id={Feedback.HateSpeech} defaultChecked={negativeFeedbackList.includes(Feedback.HateSpeech)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED******REMOVED***<Checkbox label="Violent: glorification of violence, self-harm" id={Feedback.Violent} defaultChecked={negativeFeedbackList.includes(Feedback.Violent)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED******REMOVED***<Checkbox label="Sexual: explicit content, grooming" id={Feedback.Sexual} defaultChecked={negativeFeedbackList.includes(Feedback.Sexual)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED******REMOVED***<Checkbox label="Manipulative: devious, emotional, pushy, bullying" defaultChecked={negativeFeedbackList.includes(Feedback.Manipulative)} id={Feedback.Manipulative} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED******REMOVED***<Checkbox label="Other" id={Feedback.OtherHarmful} defaultChecked={negativeFeedbackList.includes(Feedback.OtherHarmful)} onChange={updateFeedbackList}></Checkbox>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</>
***REMOVED***);
***REMOVED***

***REMOVED***const components = {
***REMOVED***code({node, ...props}: {node: any, [key: string]: any}) {
***REMOVED******REMOVED***let language;
***REMOVED******REMOVED***if (props.className) {
***REMOVED******REMOVED***const match = props.className.match(/language-(\w+)/);
***REMOVED******REMOVED***language = match ? match[1] : undefined;
***REMOVED***
***REMOVED******REMOVED***const codeString = node.children[0].value ?? '';
***REMOVED******REMOVED***return (
***REMOVED******REMOVED***<SyntaxHighlighter style={nord} language={language} PreTag="div" {...props}>
***REMOVED******REMOVED******REMOVED***{codeString}
***REMOVED******REMOVED***</SyntaxHighlighter>
***REMOVED******REMOVED***);
***REMOVED***,
***REMOVED***;
***REMOVED***return (
***REMOVED***<>
***REMOVED******REMOVED***<Stack className={styles.answerContainer} tabIndex={0}>
***REMOVED******REMOVED***
***REMOVED******REMOVED***<Stack.Item>
***REMOVED******REMOVED******REMOVED***<Stack horizontal grow>
***REMOVED******REMOVED******REMOVED***<Stack.Item grow>
***REMOVED******REMOVED******REMOVED******REMOVED***<ReactMarkdown
***REMOVED******REMOVED******REMOVED******REMOVED***linkTarget="_blank"
***REMOVED******REMOVED******REMOVED******REMOVED***remarkPlugins={[remarkGfm, supersub]}
***REMOVED******REMOVED******REMOVED******REMOVED***children={SANITIZE_ANSWER ? DOMPurify.sanitize(parsedAnswer.markdownFormatText, {ALLOWED_TAGS: XSSAllowTags}) : parsedAnswer.markdownFormatText}
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.answerText}
***REMOVED******REMOVED******REMOVED******REMOVED***components={components}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED******REMOVED***<Stack.Item className={styles.answerHeader}>
***REMOVED******REMOVED******REMOVED******REMOVED***{FEEDBACK_ENABLED && answer.message_id !== undefined && <Stack horizontal horizontalAlign="space-between">
***REMOVED******REMOVED******REMOVED******REMOVED***<ThumbLike20Filled
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="false"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Like this response"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={() => onLikeResponseClicked()}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***style={feedbackState === Feedback.Positive || appStateContext?.state.feedbackState[answer.message_id] === Feedback.Positive ? 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{ color: "darkgreen", cursor: "pointer" } : 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{ color: "slategray", cursor: "pointer" }}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***<ThumbDislike20Filled
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="false"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Dislike this response"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={() => onDislikeResponseClicked()}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***style={(feedbackState !== Feedback.Positive && feedbackState !== Feedback.Neutral && feedbackState !== undefined) ? 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{ color: "darkred", cursor: "pointer" } : 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{ color: "slategray", cursor: "pointer" }}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>}
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***<Stack horizontal className={styles.answerFooter}>
***REMOVED******REMOVED******REMOVED***{!!parsedAnswer.citations.length && (
***REMOVED******REMOVED******REMOVED***<Stack.Item
***REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? toggleIsRefAccordionOpen() : null}
***REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack style={{ width: "100%" }} >
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack horizontal horizontalAlign='start' verticalAlign='center'>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Text
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.accordionTitle}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={toggleIsRefAccordionOpen}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Open references"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span>{parsedAnswer.citations.length > 1 ? parsedAnswer.citations.length + " references" : "1 reference"}</span>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</Text>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<FontIcon className={styles.accordionIcon}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={handleChevronClick} iconName={chevronIsExpanded ? 'ChevronDown' : 'ChevronRight'}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>

***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***<Stack.Item className={styles.answerDisclaimerContainer}>
***REMOVED******REMOVED******REMOVED***<span className={styles.answerDisclaimer}>AI-generated content may be incorrect</span>
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***{chevronIsExpanded &&
***REMOVED******REMOVED******REMOVED***<div className={styles.citationWrapper} >
***REMOVED******REMOVED******REMOVED***{parsedAnswer.citations.map((citation, idx) => {
***REMOVED******REMOVED******REMOVED******REMOVED***return (
***REMOVED******REMOVED******REMOVED******REMOVED***<span 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***title={createCitationFilepath(citation, ++idx)} 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***tabIndex={0} 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***role="link" 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***key={idx} 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={() => onCitationClicked(citation)} 
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? onCitationClicked(citation) : null}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.citationContainer}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***aria-label={createCitationFilepath(citation, idx)}
***REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.citation}>{idx}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{createCitationFilepath(citation, idx, true)}
***REMOVED******REMOVED******REMOVED******REMOVED***</span>);
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***<Dialog 
***REMOVED******REMOVED***onDismiss={() => {
***REMOVED******REMOVED******REMOVED***resetFeedbackDialog();
***REMOVED******REMOVED******REMOVED***setFeedbackState(Feedback.Neutral);
***REMOVED******REMOVED***}
***REMOVED******REMOVED***hidden={!isFeedbackDialogOpen}
***REMOVED******REMOVED***styles={{
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***main: [{
***REMOVED******REMOVED******REMOVED***selectors: {
***REMOVED******REMOVED******REMOVED***  ['@media (min-width: 480px)']: {
***REMOVED******REMOVED******REMOVED******REMOVED***maxWidth: '600px',
***REMOVED******REMOVED******REMOVED******REMOVED***background: "#FFFFFF",
***REMOVED******REMOVED******REMOVED******REMOVED***boxShadow: "0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)",
***REMOVED******REMOVED******REMOVED******REMOVED***borderRadius: "8px",
***REMOVED******REMOVED******REMOVED******REMOVED***maxHeight: '600px',
***REMOVED******REMOVED******REMOVED******REMOVED***minHeight: '100px',
***REMOVED******REMOVED***  ***REMOVED***
***REMOVED******REMOVED******REMOVED***
***REMOVED***  ***REMOVED***]
***REMOVED******REMOVED***}
***REMOVED******REMOVED***dialogContentProps={{
***REMOVED******REMOVED******REMOVED***title: "Submit Feedback",
***REMOVED******REMOVED******REMOVED***showCloseButton: true
***REMOVED******REMOVED***}
***REMOVED******REMOVED***>
***REMOVED******REMOVED***<Stack tokens={{childrenGap: 4}}>
***REMOVED******REMOVED******REMOVED***<div>Your feedback will improve this experience.</div>
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***{!showReportInappropriateFeedback ? <UnhelpfulFeedbackContent/> : <ReportInappropriateFeedbackContent/>}
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***<div>By pressing submit, your feedback will be visible to the application owner.</div>
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***<DefaultButton disabled={negativeFeedbackList.length < 1} onClick={onSubmitNegativeFeedback}>Submit</DefaultButton>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***
***REMOVED******REMOVED***</Dialog>
***REMOVED***</>
***REMOVED***);
};
