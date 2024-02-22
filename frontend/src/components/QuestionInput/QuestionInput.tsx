import { useState } from "react";
import { Stack, TextField } from "@fluentui/react";
import { SendRegular } from "@fluentui/react-icons";
import Send from "../../assets/Send.svg";
import styles from "./QuestionInput.module.css";

interface Props {
***REMOVED***onSend: (question: string, id?: string) => void;
***REMOVED***disabled: boolean;
***REMOVED***placeholder?: string;
***REMOVED***clearOnSend?: boolean;
***REMOVED***conversationId?: string;
}

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend, conversationId }: Props) => {
***REMOVED***const [question, setQuestion] = useState<string>("");

***REMOVED***const sendQuestion = () => {
***REMOVED***if (disabled || !question.trim()) {
***REMOVED******REMOVED***return;
***REMOVED***

***REMOVED***if(conversationId){
***REMOVED******REMOVED***onSend(question, conversationId);
***REMOVED***else{
***REMOVED******REMOVED***onSend(question);
***REMOVED***

***REMOVED***if (clearOnSend) {
***REMOVED******REMOVED***setQuestion("");
***REMOVED***
***REMOVED***;

***REMOVED***const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
***REMOVED***if (ev.key === "Enter" && !ev.shiftKey && !(ev.nativeEvent?.isComposing === true)) {
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
***REMOVED******REMOVED***<div className={styles.questionInputSendButtonContainer} 
***REMOVED******REMOVED***role="button" 
***REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED***aria-label="Ask question button"
***REMOVED******REMOVED***onClick={sendQuestion}
***REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? sendQuestion() : null}
***REMOVED******REMOVED***>
***REMOVED******REMOVED***{ sendQuestionDisabled ? 
***REMOVED******REMOVED******REMOVED***<SendRegular className={styles.questionInputSendButtonDisabled}/>
***REMOVED******REMOVED******REMOVED***:
***REMOVED******REMOVED******REMOVED***<img src={Send} className={styles.questionInputSendButton}/>
***REMOVED******REMOVED***
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***<div className={styles.questionInputBottomBorder} />
***REMOVED***</Stack>
***REMOVED***);
};
