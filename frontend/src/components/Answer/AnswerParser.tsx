import { AskResponse, DocumentResult } from "../../api";
import styles from "./Answer.module.css";

type JsxParsedAnswer = {
***REMOVED***answerJsx: (string | JSX.Element)[];
***REMOVED***citations: DocumentResult[];
***REMOVED***markdownFormatText: string;
};

export function parseAnswerToJsx(answer: AskResponse, onInlineCitationClicked: (citedDocument: DocumentResult) => void): JsxParsedAnswer {
***REMOVED***let citationIndex = 0;
***REMOVED***const citations: DocumentResult[] = [];

***REMOVED***const answerText = answer.answer;
***REMOVED***const parts = answerText.split(/\[doc([\d]+)\]/g);
***REMOVED***
***REMOVED***let markdownFormatText = "";
***REMOVED***const fragments: (string | JSX.Element)[] = [];

***REMOVED***parts.forEach((part, index) => {
***REMOVED***if (index % 2 === 0) {
***REMOVED******REMOVED***fragments.push(part);
***REMOVED******REMOVED***markdownFormatText += part;
***REMOVED***
***REMOVED******REMOVED***// match the citation to the top docs
***REMOVED******REMOVED***let citationNumber = parseInt(part.slice(-1));
***REMOVED******REMOVED***if (isNaN(citationNumber) || citationNumber > answer.top_docs.length || citationNumber <= 0) {
***REMOVED******REMOVED***fragments.push(`[doc${part}]`);
***REMOVED******REMOVED***markdownFormatText += `[doc${part}]`;
***REMOVED***
***REMOVED******REMOVED***let citedDocument = answer.top_docs[citationNumber - 1];
***REMOVED******REMOVED***if (citedDocument.id === null) {
***REMOVED******REMOVED***citedDocument.id = crypto.randomUUID();
***REMOVED***

***REMOVED******REMOVED***if (!citations.find((c) => c.id === citedDocument.id)) {
***REMOVED******REMOVED***citations.push(citedDocument);
***REMOVED******REMOVED***citationIndex++;
***REMOVED***

***REMOVED******REMOVED***fragments.push(
***REMOVED******REMOVED***<a className={styles.citation} title={citedDocument.filepath ?? ""} onClick={() => onInlineCitationClicked(citedDocument)}>
***REMOVED******REMOVED******REMOVED***<sup className={styles.clickableSup}>{citationIndex}</sup>
***REMOVED******REMOVED***</a>
***REMOVED******REMOVED***);
***REMOVED******REMOVED***markdownFormatText += ` ^${citationIndex}^ `;
***REMOVED***
***REMOVED***);

***REMOVED***return {
***REMOVED***answerJsx: fragments,
***REMOVED***citations,
***REMOVED***markdownFormatText
***REMOVED***;
}
