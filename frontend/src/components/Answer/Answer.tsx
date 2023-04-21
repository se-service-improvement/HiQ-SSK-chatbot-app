import { useMemo } from "react";
import { Stack } from "@fluentui/react";

import styles from "./Answer.module.css";

import { Sparkle28Filled} from "@fluentui/react-icons";

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
***REMOVED***const parsedAnswer = useMemo(() => parseAnswerToJsx(answer, onCitationClicked), [answer]);

***REMOVED***return (
***REMOVED***<>
***REMOVED******REMOVED***<Stack className={styles.answerContainer}>
***REMOVED******REMOVED***<Stack.Item>
***REMOVED******REMOVED******REMOVED***<Stack horizontal horizontalAlign="space-between">
***REMOVED******REMOVED******REMOVED***<Sparkle28Filled aria-hidden="true" aria-label="Answer logo" />
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</Stack.Item>

***REMOVED******REMOVED***<Stack.Item grow>
***REMOVED******REMOVED******REMOVED***<p className={styles.answerText}>{parsedAnswer.answerJsx}</p>
***REMOVED******REMOVED***</Stack.Item>

***REMOVED******REMOVED***{!!parsedAnswer.citations.length && (
***REMOVED******REMOVED******REMOVED***<Stack.Item>
***REMOVED******REMOVED******REMOVED***<Stack horizontal wrap className={styles.citationsList} tokens={{ childrenGap: 5 }}>
***REMOVED******REMOVED******REMOVED******REMOVED***<span className={styles.citationLearnMore}>Citations:</span>
***REMOVED******REMOVED******REMOVED******REMOVED***{parsedAnswer.citations.map((x, i) => {
***REMOVED******REMOVED******REMOVED******REMOVED***return (
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<a key={i} className={styles.citation} title={x.filepath ?? ""} onClick={() => onCitationClicked(x)}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{`${++i}${x.filepath ? ". " + x.filepath : ""}`}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</a>
***REMOVED******REMOVED******REMOVED******REMOVED***);
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***</Stack>
***REMOVED***</>
***REMOVED***);
};
