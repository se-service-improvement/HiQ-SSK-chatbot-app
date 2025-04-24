import { FormEvent, useContext, useEffect, useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { nord } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Checkbox, DefaultButton, Dialog, FontIcon, Stack, Text } from '@fluentui/react'
import { useBoolean } from '@fluentui/react-hooks'
import { ThumbDislike20Filled, ThumbLike20Filled } from '@fluentui/react-icons'
import DOMPurify from 'dompurify'
import remarkGfm from 'remark-gfm'
import supersub from 'remark-supersub'
import { AskResponse, Citation, Feedback, historyMessageFeedback } from '../../api'
import { XSSAllowTags, XSSAllowAttributes } from '../../constants/sanatizeAllowables'
import { AppStateContext } from '../../state/AppProvider'

import { parseAnswer } from './AnswerParser'

import styles from './Answer.module.css'

interface Props {
  answer: AskResponse
  onCitationClicked: (citedDocument: Citation) => void
  onExectResultClicked: (answerId: string) => void
}

export const Answer = ({ answer, onCitationClicked, onExectResultClicked }: Props) => {
  const initializeAnswerFeedback = (answer: AskResponse) => {
***REMOVED***if (answer.message_id == undefined) return undefined
***REMOVED***if (answer.feedback == undefined) return undefined
***REMOVED***if (answer.feedback.split(',').length > 1) return Feedback.Negative
***REMOVED***if (Object.values(Feedback).includes(answer.feedback)) return answer.feedback
***REMOVED***return Feedback.Neutral
  }

  const [isRefAccordionOpen, { toggle: toggleIsRefAccordionOpen }] = useBoolean(false)
  const filePathTruncationLimit = 50

  const parsedAnswer = useMemo(() => parseAnswer(answer), [answer])
  const [chevronIsExpanded, setChevronIsExpanded] = useState(isRefAccordionOpen)
  const [feedbackState, setFeedbackState] = useState(initializeAnswerFeedback(answer))
  const [isFeedbackDialogOpen, setIsFeedbackDialogOpen] = useState(false)
  const [showReportInappropriateFeedback, setShowReportInappropriateFeedback] = useState(false)
  const [negativeFeedbackList, setNegativeFeedbackList] = useState<Feedback[]>([])
  const appStateContext = useContext(AppStateContext)
  const FEEDBACK_ENABLED =
***REMOVED***appStateContext?.state.frontendSettings?.feedback_enabled && appStateContext?.state.isCosmosDBAvailable?.cosmosDB
  const SANITIZE_ANSWER = appStateContext?.state.frontendSettings?.sanitize_answer

  const handleChevronClick = () => {
***REMOVED***setChevronIsExpanded(!chevronIsExpanded)
***REMOVED***toggleIsRefAccordionOpen()
  }

  useEffect(() => {
***REMOVED***setChevronIsExpanded(isRefAccordionOpen)
  }, [isRefAccordionOpen])

  useEffect(() => {
***REMOVED***if (answer.message_id == undefined) return

***REMOVED***let currentFeedbackState
***REMOVED***if (appStateContext?.state.feedbackState && appStateContext?.state.feedbackState[answer.message_id]) {
***REMOVED***  currentFeedbackState = appStateContext?.state.feedbackState[answer.message_id]
***REMOVED***
***REMOVED***  currentFeedbackState = initializeAnswerFeedback(answer)
***REMOVED***
***REMOVED***setFeedbackState(currentFeedbackState)
  }, [appStateContext?.state.feedbackState, feedbackState, answer.message_id])

  const createCitationFilepath = (citation: Citation, index: number, truncate: boolean = false) => {
***REMOVED***let citationFilename = ''

***REMOVED***if (citation.filepath) {
***REMOVED***  const part_i = citation.part_index ?? (citation.chunk_id ? parseInt(citation.chunk_id) + 1 : '')
***REMOVED***  if (truncate && citation.filepath.length > filePathTruncationLimit) {
***REMOVED***const citationLength = citation.filepath.length
***REMOVED***citationFilename = `${citation.filepath.substring(0, 20)}...${citation.filepath.substring(citationLength - 20)} - Part ${part_i}`
  ***REMOVED***
***REMOVED***citationFilename = `${citation.filepath} - Part ${part_i}`
  ***REMOVED***
***REMOVED*** else if (citation.filepath && citation.reindex_id) {
***REMOVED***  citationFilename = `${citation.filepath} - Part ${citation.reindex_id}`
***REMOVED***
***REMOVED***  citationFilename = `Citation ${index}`
***REMOVED***
***REMOVED***return citationFilename
  }

  const onLikeResponseClicked = async () => {
***REMOVED***if (answer.message_id == undefined) return

***REMOVED***let newFeedbackState = feedbackState
***REMOVED***// Set or unset the thumbs up state
***REMOVED***if (feedbackState == Feedback.Positive) {
***REMOVED***  newFeedbackState = Feedback.Neutral
***REMOVED***
***REMOVED***  newFeedbackState = Feedback.Positive
***REMOVED***
***REMOVED***appStateContext?.dispatch({
***REMOVED***  type: 'SET_FEEDBACK_STATE',
***REMOVED***  payload: { answerId: answer.message_id, feedback: newFeedbackState }
***REMOVED***)
***REMOVED***setFeedbackState(newFeedbackState)

***REMOVED***// Update message feedback in db
***REMOVED***await historyMessageFeedback(answer.message_id, newFeedbackState)
  }

  const onDislikeResponseClicked = async () => {
***REMOVED***if (answer.message_id == undefined) return

***REMOVED***let newFeedbackState = feedbackState
***REMOVED***if (feedbackState === undefined || feedbackState === Feedback.Neutral || feedbackState === Feedback.Positive) {
***REMOVED***  newFeedbackState = Feedback.Negative
***REMOVED***  setFeedbackState(newFeedbackState)
***REMOVED***  setIsFeedbackDialogOpen(true)
***REMOVED***
***REMOVED***  // Reset negative feedback to neutral
***REMOVED***  newFeedbackState = Feedback.Neutral
***REMOVED***  setFeedbackState(newFeedbackState)
***REMOVED***  await historyMessageFeedback(answer.message_id, Feedback.Neutral)
***REMOVED***
***REMOVED***appStateContext?.dispatch({
***REMOVED***  type: 'SET_FEEDBACK_STATE',
***REMOVED***  payload: { answerId: answer.message_id, feedback: newFeedbackState }
***REMOVED***)
  }

  const updateFeedbackList = (ev?: FormEvent<HTMLElement | HTMLInputElement>, checked?: boolean) => {
***REMOVED***if (answer.message_id == undefined) return
***REMOVED***const selectedFeedback = (ev?.target as HTMLInputElement)?.id as Feedback

***REMOVED***let feedbackList = negativeFeedbackList.slice()
***REMOVED***if (checked) {
***REMOVED***  feedbackList.push(selectedFeedback)
***REMOVED***
***REMOVED***  feedbackList = feedbackList.filter(f => f !== selectedFeedback)
***REMOVED***

***REMOVED***setNegativeFeedbackList(feedbackList)
  }

  const onSubmitNegativeFeedback = async () => {
***REMOVED***if (answer.message_id == undefined) return
***REMOVED***await historyMessageFeedback(answer.message_id, negativeFeedbackList.join(','))
***REMOVED***resetFeedbackDialog()
  }

  const resetFeedbackDialog = () => {
***REMOVED***setIsFeedbackDialogOpen(false)
***REMOVED***setShowReportInappropriateFeedback(false)
***REMOVED***setNegativeFeedbackList([])
  }

  const UnhelpfulFeedbackContent = () => {
***REMOVED***return (
***REMOVED***  <>
***REMOVED***<div>Why wasn't this response helpful?</div>
***REMOVED***<Stack tokens={{ childrenGap: 4 }}>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Citations are missing"
***REMOVED******REMOVED***id={Feedback.MissingCitation}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.MissingCitation)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Citations are wrong"
***REMOVED******REMOVED***id={Feedback.WrongCitation}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.WrongCitation)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="The response is not from my data"
***REMOVED******REMOVED***id={Feedback.OutOfScope}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.OutOfScope)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Inaccurate or irrelevant"
***REMOVED******REMOVED***id={Feedback.InaccurateOrIrrelevant}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.InaccurateOrIrrelevant)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Other"
***REMOVED******REMOVED***id={Feedback.OtherUnhelpful}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.OtherUnhelpful)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***</Stack>
***REMOVED***<div onClick={() => setShowReportInappropriateFeedback(true)} style={{ color: '#115EA3', cursor: 'pointer' }}>
***REMOVED***  Report inappropriate content
***REMOVED***</div>
***REMOVED***  </>
***REMOVED***)
  }

  const ReportInappropriateFeedbackContent = () => {
***REMOVED***return (
***REMOVED***  <>
***REMOVED***<div>
***REMOVED***  The content is <span style={{ color: 'red' }}>*</span>
***REMOVED***</div>
***REMOVED***<Stack tokens={{ childrenGap: 4 }}>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Hate speech, stereotyping, demeaning"
***REMOVED******REMOVED***id={Feedback.HateSpeech}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.HateSpeech)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Violent: glorification of violence, self-harm"
***REMOVED******REMOVED***id={Feedback.Violent}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.Violent)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Sexual: explicit content, grooming"
***REMOVED******REMOVED***id={Feedback.Sexual}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.Sexual)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Manipulative: devious, emotional, pushy, bullying"
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.Manipulative)}
***REMOVED******REMOVED***id={Feedback.Manipulative}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***  <Checkbox
***REMOVED******REMOVED***label="Other"
***REMOVED******REMOVED***id={Feedback.OtherHarmful}
***REMOVED******REMOVED***defaultChecked={negativeFeedbackList.includes(Feedback.OtherHarmful)}
***REMOVED******REMOVED***onChange={updateFeedbackList}></Checkbox>
***REMOVED***</Stack>
***REMOVED***  </>
***REMOVED***)
  }

  const components = {
***REMOVED***code({ node, ...props }: { node: any;[key: string]: any }) {
***REMOVED***  let language
***REMOVED***  if (props.className) {
***REMOVED***const match = props.className.match(/language-(\w+)/)
***REMOVED***language = match ? match[1] : undefined
  ***REMOVED***
***REMOVED***  const codeString = node.children[0].value ?? ''
***REMOVED***  return (
***REMOVED***<SyntaxHighlighter style={nord} language={language} PreTag="div" {...props}>
***REMOVED***  {codeString}
***REMOVED***</SyntaxHighlighter>
***REMOVED***  )
***REMOVED***
  }
  return (
***REMOVED***<>
***REMOVED***  <Stack className={styles.answerContainer} tabIndex={0}>
***REMOVED***<Stack.Item>
***REMOVED***  <Stack horizontal grow>
***REMOVED******REMOVED***<Stack.Item grow>
***REMOVED******REMOVED***  {parsedAnswer && <ReactMarkdown
***REMOVED******REMOVED***linkTarget="_blank"
***REMOVED******REMOVED***remarkPlugins={[remarkGfm, supersub]}
***REMOVED******REMOVED***children={
***REMOVED******REMOVED***  SANITIZE_ANSWER
***REMOVED******REMOVED******REMOVED***? DOMPurify.sanitize(parsedAnswer?.markdownFormatText, { ALLOWED_TAGS: XSSAllowTags, ALLOWED_ATTR: XSSAllowAttributes })
***REMOVED******REMOVED******REMOVED***: parsedAnswer?.markdownFormatText
***REMOVED******REMOVED***
***REMOVED******REMOVED***className={styles.answerText}
***REMOVED******REMOVED***components={components}
***REMOVED******REMOVED***  />}
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***<Stack.Item className={styles.answerHeader}>
***REMOVED******REMOVED***  {FEEDBACK_ENABLED && answer.message_id !== undefined && (
***REMOVED******REMOVED***<Stack horizontal horizontalAlign="space-between">
***REMOVED******REMOVED***  <ThumbLike20Filled
***REMOVED******REMOVED******REMOVED***aria-hidden="false"
***REMOVED******REMOVED******REMOVED***aria-label="Like this response"
***REMOVED******REMOVED******REMOVED***onClick={() => onLikeResponseClicked()}
***REMOVED******REMOVED******REMOVED***style={
***REMOVED******REMOVED******REMOVED***  feedbackState === Feedback.Positive ||
***REMOVED******REMOVED******REMOVED***appStateContext?.state.feedbackState[answer.message_id] === Feedback.Positive
***REMOVED******REMOVED******REMOVED***? { color: 'darkgreen', cursor: 'pointer' }
***REMOVED******REMOVED******REMOVED***: { color: 'slategray', cursor: 'pointer' }
***REMOVED******REMOVED***
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***  <ThumbDislike20Filled
***REMOVED******REMOVED******REMOVED***aria-hidden="false"
***REMOVED******REMOVED******REMOVED***aria-label="Dislike this response"
***REMOVED******REMOVED******REMOVED***onClick={() => onDislikeResponseClicked()}
***REMOVED******REMOVED******REMOVED***style={
***REMOVED******REMOVED******REMOVED***  feedbackState !== Feedback.Positive &&
***REMOVED******REMOVED******REMOVED***feedbackState !== Feedback.Neutral &&
***REMOVED******REMOVED******REMOVED***feedbackState !== undefined
***REMOVED******REMOVED******REMOVED***? { color: 'darkred', cursor: 'pointer' }
***REMOVED******REMOVED******REMOVED***: { color: 'slategray', cursor: 'pointer' }
***REMOVED******REMOVED***
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  )}
***REMOVED******REMOVED***</Stack.Item>
***REMOVED***  </Stack>
***REMOVED***</Stack.Item>
***REMOVED***{parsedAnswer?.generated_chart !== null && (
***REMOVED***  <Stack className={styles.answerContainer}>
***REMOVED******REMOVED***<Stack.Item grow>
***REMOVED******REMOVED***  <img src={`data:image/png;base64, ${parsedAnswer?.generated_chart}`} />
***REMOVED******REMOVED***</Stack.Item>
***REMOVED***  </Stack>
***REMOVED***)}
***REMOVED***<Stack horizontal className={styles.answerFooter}>
***REMOVED***  {!!parsedAnswer?.citations.length && (
***REMOVED******REMOVED***<Stack.Item onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? toggleIsRefAccordionOpen() : null)}>
***REMOVED******REMOVED***  <Stack style={{ width: '100%' }}>
***REMOVED******REMOVED***<Stack horizontal horizontalAlign="start" verticalAlign="center">
***REMOVED******REMOVED***  <Text
***REMOVED******REMOVED******REMOVED***className={styles.accordionTitle}
***REMOVED******REMOVED******REMOVED***onClick={toggleIsRefAccordionOpen}
***REMOVED******REMOVED******REMOVED***aria-label="Open references"
***REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED***role="button">
***REMOVED******REMOVED******REMOVED***<span>
***REMOVED******REMOVED******REMOVED***  {parsedAnswer.citations.length > 1
***REMOVED******REMOVED******REMOVED***? parsedAnswer.citations.length + ' references'
***REMOVED******REMOVED******REMOVED***: '1 reference'}
***REMOVED******REMOVED******REMOVED***</span>
***REMOVED******REMOVED***  </Text>
***REMOVED******REMOVED***  <FontIcon
***REMOVED******REMOVED******REMOVED***className={styles.accordionIcon}
***REMOVED******REMOVED******REMOVED***onClick={handleChevronClick}
***REMOVED******REMOVED******REMOVED***iconName={chevronIsExpanded ? 'ChevronDown' : 'ChevronRight'}
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED***  )}
***REMOVED***  <Stack.Item className={styles.answerDisclaimerContainer}>
***REMOVED******REMOVED***<span className={styles.answerDisclaimer}>Content generate by AI may be incorrect</span>
***REMOVED***  </Stack.Item>
***REMOVED***  {!!answer.exec_results?.length && (
***REMOVED******REMOVED***<Stack.Item onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? toggleIsRefAccordionOpen() : null)}>
***REMOVED******REMOVED***  <Stack style={{ width: '100%' }}>
***REMOVED******REMOVED***<Stack horizontal horizontalAlign="start" verticalAlign="center">
***REMOVED******REMOVED***  <Text
***REMOVED******REMOVED******REMOVED***className={styles.accordionTitle}
***REMOVED******REMOVED******REMOVED***onClick={() => onExectResultClicked(answer.message_id ?? '')}
***REMOVED******REMOVED******REMOVED***aria-label="Open Intents"
***REMOVED******REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED******REMOVED***role="button">
***REMOVED******REMOVED******REMOVED***<span>
***REMOVED******REMOVED******REMOVED***  Show Intents
***REMOVED******REMOVED******REMOVED***</span>
***REMOVED******REMOVED***  </Text>
***REMOVED******REMOVED***  <FontIcon
***REMOVED******REMOVED******REMOVED***className={styles.accordionIcon}
***REMOVED******REMOVED******REMOVED***onClick={handleChevronClick}
***REMOVED******REMOVED******REMOVED***iconName={'ChevronRight'}
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED***  )}
***REMOVED***</Stack>
***REMOVED***{chevronIsExpanded && (
***REMOVED***  <div className={styles.citationWrapper}>
***REMOVED******REMOVED***{parsedAnswer?.citations.map((citation, idx) => {
***REMOVED******REMOVED***  return (
***REMOVED******REMOVED***<span
***REMOVED******REMOVED***  title={createCitationFilepath(citation, ++idx)}
***REMOVED******REMOVED***  tabIndex={0}
***REMOVED******REMOVED***  role="link"
***REMOVED******REMOVED***  key={idx}
***REMOVED******REMOVED***  onClick={() => onCitationClicked(citation)}
***REMOVED******REMOVED***  onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? onCitationClicked(citation) : null)}
***REMOVED******REMOVED***  className={styles.citationContainer}
***REMOVED******REMOVED***  aria-label={createCitationFilepath(citation, idx)}>
***REMOVED******REMOVED***  <div className={styles.citation}>{idx}</div>
***REMOVED******REMOVED***  {createCitationFilepath(citation, idx, true)}
***REMOVED******REMOVED***</span>
***REMOVED******REMOVED***  )
***REMOVED***)}
***REMOVED***  </div>
***REMOVED***)}
***REMOVED***  </Stack>
***REMOVED***  <Dialog
***REMOVED***onDismiss={() => {
***REMOVED***  resetFeedbackDialog()
***REMOVED***  setFeedbackState(Feedback.Neutral)
***REMOVED***}
***REMOVED***hidden={!isFeedbackDialogOpen}
***REMOVED***styles={{
***REMOVED***  main: [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***  selectors: {
***REMOVED******REMOVED***['@media (min-width: 480px)']: {
***REMOVED******REMOVED***  maxWidth: '600px',
***REMOVED******REMOVED***  background: '#FFFFFF',
***REMOVED******REMOVED***  boxShadow: '0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)',
***REMOVED******REMOVED***  borderRadius: '8px',
***REMOVED******REMOVED***  maxHeight: '600px',
***REMOVED******REMOVED***  minHeight: '100px'
***REMOVED******REMOVED***
  ***REMOVED***
***REMOVED***
***REMOVED***  ]
***REMOVED***}
***REMOVED***dialogContentProps={{
***REMOVED***  title: 'Submit Feedback',
***REMOVED***  showCloseButton: true
***REMOVED***}>
***REMOVED***<Stack tokens={{ childrenGap: 4 }}>
***REMOVED***  <div>Your feedback will improve this experience.</div>

***REMOVED***  {!showReportInappropriateFeedback ? <UnhelpfulFeedbackContent /> : <ReportInappropriateFeedbackContent />}

***REMOVED***  <div>By pressing submit, your feedback will be visible to the application owner.</div>

***REMOVED***  <DefaultButton disabled={negativeFeedbackList.length < 1} onClick={onSubmitNegativeFeedback}>
***REMOVED******REMOVED***Submit
***REMOVED***  </DefaultButton>
***REMOVED***</Stack>
***REMOVED***  </Dialog>
***REMOVED***</>
  )
}
