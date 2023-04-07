import { useMemo } from "react";
import { Stack } from "@fluentui/react";

import styles from "./Answer.module.css";

import { Sparkle28Filled, ThumbLike20Filled, ThumbDislike20Filled } from "@fluentui/react-icons";

import { AskResponse, FeedbackString, DocumentResult } from "../../api";
import { parseAnswerToJsx } from "./AnswerParser";

interface Props {
***REMOVED***answer: AskResponse;
***REMOVED***onCitationClicked: (citedDocument: DocumentResult) => void;
***REMOVED***onThoughtProcessClicked: () => void;
***REMOVED***onSupportingContentClicked: () => void;
***REMOVED***onLikeResponseClicked: () => void;
***REMOVED***onDislikeResponseClicked: () => void;
}

export const Answer = ({
***REMOVED***answer,
***REMOVED***onCitationClicked,
***REMOVED***onLikeResponseClicked,
***REMOVED***onDislikeResponseClicked
}: Props) => {
***REMOVED***const parsedAnswer = useMemo(() => parseAnswerToJsx(answer, onCitationClicked), [answer]);

***REMOVED***return (
***REMOVED***<>
***REMOVED******REMOVED***<Stack className={styles.answerContainer} verticalAlign="space-between">
***REMOVED******REMOVED***<Stack.Item>
***REMOVED******REMOVED******REMOVED***<Stack horizontal horizontalAlign="space-between">
***REMOVED******REMOVED******REMOVED***<Sparkle28Filled aria-hidden="true" aria-label="Answer logo" />
***REMOVED******REMOVED******REMOVED***<div>
***REMOVED******REMOVED******REMOVED******REMOVED***<ThumbLike20Filled
***REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="false"
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Like this response"
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={() => onLikeResponseClicked()}
***REMOVED******REMOVED******REMOVED******REMOVED***style={answer.feedback == FeedbackString.ThumbsUp ? { color: "darkgreen" } : { color: "slategray" }}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***<ThumbDislike20Filled
***REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="false"
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label="Dislike this response"
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={() => onDislikeResponseClicked()}
***REMOVED******REMOVED******REMOVED******REMOVED***style={answer.feedback == FeedbackString.ThumbsDown ? { color: "darkred" } : { color: "slategray" }}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</div>
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
