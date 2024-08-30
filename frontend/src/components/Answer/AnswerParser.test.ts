import { cloneDeep } from 'lodash'

import { AskResponse, Citation } from '../../api' // Ensure this path matches the location of your types

import { enumerateCitations, parseAnswer, ParsedAnswer } from './AnswerParser' // Update the path accordingly

const sampleCitations: Citation[] = [
  {
***REMOVED***id: 'doc1',
***REMOVED***filepath: 'file1.pdf',
***REMOVED***part_index: undefined,
***REMOVED***content: '',
***REMOVED***title: null,
***REMOVED***url: null,
***REMOVED***metadata: null,
***REMOVED***chunk_id: null,
***REMOVED***reindex_id: null
  },
  {
***REMOVED***id: 'doc2',
***REMOVED***filepath: 'file1.pdf',
***REMOVED***part_index: undefined,
***REMOVED***content: '',
***REMOVED***title: null,
***REMOVED***url: null,
***REMOVED***metadata: null,
***REMOVED***chunk_id: null,
***REMOVED***reindex_id: null
  },
  {
***REMOVED***id: 'doc3',
***REMOVED***filepath: 'file2.pdf',
***REMOVED***part_index: undefined,
***REMOVED***content: '',
***REMOVED***title: null,
***REMOVED***url: null,
***REMOVED***metadata: null,
***REMOVED***chunk_id: null,
***REMOVED***reindex_id: null
  }
]

const sampleAnswer: AskResponse = {
  answer: 'This is an example answer with citations [doc1] and [doc2].',
  citations: cloneDeep(sampleCitations),
  generated_chart: null
}

describe('enumerateCitations', () => {
  it('assigns unique part_index based on filepath', () => {
***REMOVED***const results = enumerateCitations(cloneDeep(sampleCitations))
***REMOVED***expect(results[0].part_index).toEqual(1)
***REMOVED***expect(results[1].part_index).toEqual(2)
***REMOVED***expect(results[2].part_index).toEqual(1)
  })
})

describe('parseAnswer', () => {
  it('reformats the answer text and reindexes citations', () => {
***REMOVED***const parsed: ParsedAnswer = parseAnswer(sampleAnswer)
***REMOVED***expect(parsed.markdownFormatText).toBe('This is an example answer with citations  ^1^  and  ^2^ .')
***REMOVED***expect(parsed.citations.length).toBe(2)
***REMOVED***expect(parsed.citations[0].id).toBe('1')
***REMOVED***expect(parsed.citations[0].reindex_id).toBe('1')
***REMOVED***expect(parsed.citations[1].id).toBe('2')
***REMOVED***expect(parsed.citations[1].reindex_id).toBe('2')
***REMOVED***expect(parsed.citations[0].part_index).toBe(1)
***REMOVED***expect(parsed.citations[1].part_index).toBe(2)
  })
})
