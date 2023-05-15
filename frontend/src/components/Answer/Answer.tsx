import { useEffect, useMemo, useState } from "react";
import { useBoolean } from "@fluentui/react-hooks"
import { FontIcon, Stack, Text } from "@fluentui/react";

import styles from "./Answer.module.css";

import { AskResponse, DocumentResult } from "../../api";
import { parseAnswerToJsx } from "./AnswerParser";

interface Props {
***REMOVED***answer: AskResponse;
***REMOVED***onCitationClicked: (citedDocument: DocumentResult) => void;
}

export const Answer = ({
***REMOVED***answer,
***REMOVED***onCitationClicked
}: Props) => {
***REMOVED***const [isRefAccordionOpen, { toggle: toggleIsRefAccordionOpen }] = useBoolean(false);
***REMOVED***const onInlineCitationClicked = () => {
***REMOVED***if (!isRefAccordionOpen) {
***REMOVED******REMOVED***toggleIsRefAccordionOpen();
***REMOVED***
***REMOVED***;

***REMOVED***const parsedAnswer = useMemo(() => parseAnswerToJsx(answer, onInlineCitationClicked), [answer]);
***REMOVED***const [chevronIsExpanded, setChevronIsExpanded] = useState(isRefAccordionOpen);

***REMOVED***const handleChevronClick = () => {
***REMOVED***setChevronIsExpanded(!chevronIsExpanded);
***REMOVED***toggleIsRefAccordionOpen();
  ***REMOVED***;

***REMOVED***useEffect(() => {
***REMOVED***setChevronIsExpanded(isRefAccordionOpen);
***REMOVED***, [isRefAccordionOpen]);

***REMOVED***const createCitationFilepath = (citation: DocumentResult) => {
***REMOVED***let citationDisplay = "";

***REMOVED***if (citation.filepath) {
***REMOVED******REMOVED***citationDisplay = citation.filepath;
***REMOVED***
***REMOVED***else if (citation.title) {
***REMOVED******REMOVED***citationDisplay = citation.title;
***REMOVED***

***REMOVED***if (citation.chunk_id !== null) {
***REMOVED******REMOVED***citationDisplay += ` - Part ${parseInt(citation.chunk_id) + 1}`;
***REMOVED***
***REMOVED***return citationDisplay;
***REMOVED***

***REMOVED***return (
***REMOVED***<>
***REMOVED******REMOVED***<Stack className={styles.answerContainer}>
***REMOVED******REMOVED***<Stack.Item grow>
***REMOVED******REMOVED******REMOVED***<p className={styles.answerText}>{parsedAnswer.answerJsx}</p>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***<Stack horizontal className={styles.answerFooter}>
***REMOVED******REMOVED***{!!parsedAnswer.citations.length && (
***REMOVED******REMOVED******REMOVED***<Stack.Item aria-label="References">
***REMOVED******REMOVED******REMOVED***<Stack style={{width: "100%"}} >
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack horizontal horizontalAlign='start' verticalAlign='center'>
***REMOVED******REMOVED******REMOVED******REMOVED***<Text
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***className={styles.accordionTitle}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onClick={toggleIsRefAccordionOpen}
***REMOVED******REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED******REMOVED***<span>{parsedAnswer.citations.length > 1 ? parsedAnswer.citations.length + " references" : "1 reference"}</span>
***REMOVED******REMOVED******REMOVED******REMOVED***</Text>
***REMOVED******REMOVED******REMOVED******REMOVED***<FontIcon className={styles.accordionIcon}
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={handleChevronClick} iconName={chevronIsExpanded ? 'ChevronDown' : 'ChevronRight'}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***<Stack.Item className={styles.answerDisclaimerContainer}>
***REMOVED******REMOVED******REMOVED***<span className={styles.answerDisclaimer}>AI-generated content may be incorrect</span>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***{chevronIsExpanded && 
***REMOVED******REMOVED******REMOVED***<div style={{ marginTop: 8, display: "flex", flexFlow: "wrap column", maxHeight: "150px", gap: "4px" }}>
***REMOVED******REMOVED******REMOVED***{parsedAnswer.citations.map((citation, idx) => {
***REMOVED******REMOVED******REMOVED******REMOVED***return (
***REMOVED******REMOVED******REMOVED******REMOVED***<span key={idx} onClick={() => onCitationClicked(citation)} className={styles.citationContainer}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.citation}>{++idx}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{createCitationFilepath(citation)}
***REMOVED******REMOVED******REMOVED******REMOVED***</span>);
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***
***REMOVED******REMOVED***</Stack>
***REMOVED***</>
***REMOVED***);
};
