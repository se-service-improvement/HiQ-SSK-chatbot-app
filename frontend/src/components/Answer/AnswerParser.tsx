import { AskResponse, Citation } from "../../api";
import { cloneDeep } from "lodash-es";


type ParsedAnswer = {
***REMOVED***citations: Citation[];
***REMOVED***markdownFormatText: string;
};

export function parseAnswer(answer: AskResponse): ParsedAnswer {
***REMOVED***let answerText = answer.answer;
***REMOVED***const citationLinks = answerText.match(/\[(doc\d\d?\d?)]/g);

***REMOVED***const lengthDocN = "[doc".length;

***REMOVED***let filteredCitations = [] as Citation[];
***REMOVED***let citationReindex = 0;
***REMOVED***citationLinks?.forEach(link => {
***REMOVED***// Replacing the links/citations with number
***REMOVED***let citationIndex = link.slice(lengthDocN, link.length - 1);
***REMOVED***let citation = cloneDeep(answer.citations[Number(citationIndex) - 1]) as Citation;
***REMOVED***if (!filteredCitations.find((c) => c.id === citationIndex)) {
***REMOVED***  answerText = answerText.replaceAll(link, ` ^${++citationReindex}^ `);
***REMOVED***  citation.id = citationIndex; // original doc index to de-dupe
***REMOVED***  citation.reindex_id = citationReindex.toString(); // reindex from 1 for display
***REMOVED***  filteredCitations.push(citation);
***REMOVED***
***REMOVED***)


***REMOVED***return {
***REMOVED***citations: filteredCitations,
***REMOVED***markdownFormatText: answerText
***REMOVED***;
}
