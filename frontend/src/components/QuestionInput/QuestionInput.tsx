import { useState } from "react";
import { Stack, TextField } from "@fluentui/react";
import { Sparkle28Filled } from "@fluentui/react-icons";

import styles from "./QuestionInput.module.css";

interface Props {
***REMOVED***onSend: (question: string) => void;
***REMOVED***disabled: boolean;
***REMOVED***placeholder?: string;
***REMOVED***clearOnSend?: boolean;
}

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend }: Props) => {
***REMOVED***const [question, setQuestion] = useState<string>("");

***REMOVED***const sendQuestion = () => {
***REMOVED***if (disabled || !question.trim()) {
***REMOVED******REMOVED***return;
***REMOVED***

***REMOVED***onSend(question);

***REMOVED***if (clearOnSend) {
***REMOVED******REMOVED***setQuestion("");
***REMOVED***
***REMOVED***;

***REMOVED***const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
***REMOVED***if (ev.key === "Enter" && !ev.shiftKey) {
***REMOVED******REMOVED***ev.preventDefault();
***REMOVED******REMOVED***sendQuestion();
***REMOVED***
***REMOVED***;

***REMOVED***const onQuestionChange = (_ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
***REMOVED***setQuestion(newValue || "");
***REMOVED***;

***REMOVED***const sendQuestionDisabled = disabled || !question.trim();

***REMOVED***return (
***REMOVED***<Stack horizontal className={styles.questionInputContainer}>
***REMOVED******REMOVED***<TextField
***REMOVED******REMOVED***className={styles.questionInputTextArea}
***REMOVED******REMOVED***placeholder={placeholder}
***REMOVED******REMOVED***multiline
***REMOVED******REMOVED***resizable={false}
***REMOVED******REMOVED***borderless
***REMOVED******REMOVED***value={question}
***REMOVED******REMOVED***onChange={onQuestionChange}
***REMOVED******REMOVED***onKeyDown={onEnterPress}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***<div className={styles.questionInputButtonsContainer}>
***REMOVED******REMOVED***<div
***REMOVED******REMOVED******REMOVED***className={`${styles.questionInputSendButton} ${sendQuestionDisabled ? styles.questionInputSendButtonDisabled : ""}`}
***REMOVED******REMOVED******REMOVED***aria-label="Ask question button"
***REMOVED******REMOVED******REMOVED***onClick={sendQuestion}
***REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED***<Sparkle28Filled />
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***</div>
***REMOVED***</Stack>
***REMOVED***);
};
