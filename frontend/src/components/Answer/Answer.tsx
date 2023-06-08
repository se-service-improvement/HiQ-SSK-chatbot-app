import { useEffect, useMemo, useState } from "react";
import { useBoolean } from "@fluentui/react-hooks"
import { FontIcon, Stack, Text } from "@fluentui/react";

import styles from "./Answer.module.css";

import { AskResponse, Citation } from "../../api";
import { parseAnswer } from "./AnswerParser";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import supersub from 'remark-supersub'

interface Props {
***REMOVED***answer: AskResponse;
***REMOVED***onCitationClicked: (citedDocument: Citation) => void;
}

export const Answer = ({
***REMOVED***answer,
***REMOVED***onCitationClicked
}: Props) => {
***REMOVED***const [isRefAccordionOpen, { toggle: toggleIsRefAccordionOpen }] = useBoolean(false);
***REMOVED***const filePathTruncationLimit = 50;

***REMOVED***const parsedAnswer = useMemo(() => parseAnswer(answer), [answer]);
***REMOVED***const [chevronIsExpanded, setChevronIsExpanded] = useState(isRefAccordionOpen);

***REMOVED***const handleChevronClick = () => {
***REMOVED***setChevronIsExpanded(!chevronIsExpanded);
***REMOVED***toggleIsRefAccordionOpen();
  ***REMOVED***;

***REMOVED***useEffect(() => {
***REMOVED***setChevronIsExpanded(isRefAccordionOpen);
***REMOVED***, [isRefAccordionOpen]);

***REMOVED***const createCitationFilepath = (citation: Citation, index: number, truncate: boolean = false) => {
***REMOVED***let citationFilename = "";

***REMOVED***if (citation.filepath && citation.chunk_id) {
***REMOVED******REMOVED***if (truncate && citation.filepath.length > filePathTruncationLimit) {
***REMOVED******REMOVED***const citationLength = citation.filepath.length;
***REMOVED******REMOVED***citationFilename = `${citation.filepath.substring(0, 20)}...${citation.filepath.substring(citationLength -20)} - Part ${parseInt(citation.chunk_id) + 1}`;
***REMOVED***
***REMOVED******REMOVED***else {
***REMOVED******REMOVED***citationFilename = `${citation.filepath} - Part ${parseInt(citation.chunk_id) + 1}`;
***REMOVED***
***REMOVED***
***REMOVED***else {
***REMOVED******REMOVED***citationFilename = `Citation ${index}`;
***REMOVED***
***REMOVED***return citationFilename;
***REMOVED***

***REMOVED***return (
***REMOVED***<>
***REMOVED******REMOVED***<Stack className={styles.answerContainer}>
***REMOVED******REMOVED***<Stack.Item grow>
***REMOVED******REMOVED******REMOVED***<ReactMarkdown
***REMOVED******REMOVED******REMOVED***linkTarget="_blank"
***REMOVED******REMOVED******REMOVED***remarkPlugins={[remarkGfm, supersub]}
***REMOVED******REMOVED******REMOVED***children={parsedAnswer.markdownFormatText}
***REMOVED******REMOVED******REMOVED***className={styles.answerText}
***REMOVED******REMOVED******REMOVED***/>
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
***REMOVED******REMOVED******REMOVED******REMOVED***<span title={createCitationFilepath(citation, ++idx)} key={idx} onClick={() => onCitationClicked(citation)} className={styles.citationContainer}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<div className={styles.citation}>{idx}</div>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{createCitationFilepath(citation, idx, true)}
***REMOVED******REMOVED******REMOVED******REMOVED***</span>);
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***
***REMOVED******REMOVED***</Stack>
***REMOVED***</>
***REMOVED***);
};
