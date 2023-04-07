import { AskResponse, DocumentResult } from "../../api";

type JsxParsedAnswer = {
***REMOVED***answerJsx: (string | JSX.Element)[];
***REMOVED***citations: DocumentResult[];
};

export function parseAnswerToJsx(answer: AskResponse, onCitationClicked: (citedDocument: DocumentResult) => void): JsxParsedAnswer {
***REMOVED***let citationIndex = 0;
***REMOVED***const citations: DocumentResult[] = [];

***REMOVED***const answerText = answer.answer;
***REMOVED***const parts = answerText.split(/\[doc([\d]+)\]/g);

***REMOVED***const fragments: (string | JSX.Element)[] = parts.map((part, index) => {
***REMOVED***if (index % 2 === 0) {
***REMOVED******REMOVED***return part;
***REMOVED***
***REMOVED******REMOVED***// match the citation to the top docs
***REMOVED******REMOVED***let citationNumber = parseInt(part.slice(-1));
***REMOVED******REMOVED***if (isNaN(citationNumber) || citationNumber > answer.top_docs.length || citationNumber <= 0) {
***REMOVED******REMOVED***return `[doc${part}]`;
***REMOVED***
***REMOVED******REMOVED***let citedDocument = answer.top_docs[citationNumber - 1];

***REMOVED******REMOVED***citations.push(citedDocument);
***REMOVED******REMOVED***citationIndex++;

***REMOVED******REMOVED***return (
***REMOVED******REMOVED***<a className="supContainer" title={citedDocument.filepath ?? ""} onClick={() => onCitationClicked(citedDocument)}>
***REMOVED******REMOVED******REMOVED***<sup>{citationIndex}</sup>
***REMOVED******REMOVED***</a>
***REMOVED******REMOVED***);
***REMOVED***
***REMOVED***);

***REMOVED***return {
***REMOVED***answerJsx: fragments,
***REMOVED***citations
***REMOVED***;
}
