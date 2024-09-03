import { cloneDeep } from 'lodash'

import { AskResponse, Citation } from '../../api'

export type ParsedAnswer = {
  citations: Citation[]
  markdownFormatText: string,
  generated_chart: string | null
} | null

export const enumerateCitations = (citations: Citation[]) => {
  const filepathMap = new Map()
  for (const citation of citations) {
***REMOVED***const { filepath } = citation
***REMOVED***let part_i = 1
***REMOVED***if (filepathMap.has(filepath)) {
***REMOVED***  part_i = filepathMap.get(filepath) + 1
***REMOVED***
***REMOVED***filepathMap.set(filepath, part_i)
***REMOVED***citation.part_index = part_i
  }
  return citations
}

export function parseAnswer(answer: AskResponse): ParsedAnswer {
  if (typeof answer.answer !== "string") return null
  let answerText = answer.answer
  const citationLinks = answerText.match(/\[(doc\d\d?\d?)]/g)

  const lengthDocN = '[doc'.length

  let filteredCitations = [] as Citation[]
  let citationReindex = 0
  citationLinks?.forEach(link => {
***REMOVED***// Replacing the links/citations with number
***REMOVED***const citationIndex = link.slice(lengthDocN, link.length - 1)
***REMOVED***const citation = cloneDeep(answer.citations[Number(citationIndex) - 1]) as Citation
***REMOVED***if (!filteredCitations.find(c => c.id === citationIndex) && citation) {
***REMOVED***  answerText = answerText.replaceAll(link, ` ^${++citationReindex}^ `)
***REMOVED***  citation.id = citationIndex // original doc index to de-dupe
***REMOVED***  citation.reindex_id = citationReindex.toString() // reindex from 1 for display
***REMOVED***  filteredCitations.push(citation)
***REMOVED***
  })

  filteredCitations = enumerateCitations(filteredCitations)

  return {
***REMOVED***citations: filteredCitations,
***REMOVED***markdownFormatText: answerText,
***REMOVED***generated_chart: answer.generated_chart
  }
}
