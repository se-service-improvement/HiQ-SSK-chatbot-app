import { AskResponse, Citation } from "../../api";
import { cloneDeep } from "lodash-es";


type ParsedAnswer = {
***REMOVED***citations: Citation[];
***REMOVED***markdownFormatText: string;
};

const enumerateCitations = (citations: Citation[]) => {
***REMOVED***const filepathMap = new Map();
***REMOVED***for (const citation of citations) {
***REMOVED***const { filepath } = citation;
***REMOVED***let part_i = 1
***REMOVED***if (filepathMap.has(filepath)) {
***REMOVED******REMOVED***part_i = filepathMap.get(filepath) + 1;
***REMOVED***
***REMOVED***filepathMap.set(filepath, part_i);
***REMOVED***citation.part_index = part_i;
***REMOVED***
***REMOVED***return citations;
}

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
***REMOVED***if (!filteredCitations.find((c) => c.id === citationIndex) && citation) {
***REMOVED***  answerText = answerText.replaceAll(link, ` ^${++citationReindex}^ `);
***REMOVED***  citation.id = citationIndex; // original doc index to de-dupe
***REMOVED***  citation.reindex_id = citationReindex.toString(); // reindex from 1 for display
***REMOVED***  filteredCitations.push(citation);
***REMOVED***
***REMOVED***)

***REMOVED***filteredCitations = enumerateCitations(filteredCitations);

***REMOVED***return {
***REMOVED***citations: filteredCitations,
***REMOVED***markdownFormatText: answerText
***REMOVED***;
}
