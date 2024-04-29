import { useState } from 'react'
import { Stack, TextField } from '@fluentui/react'
import { SendRegular } from '@fluentui/react-icons'

import Send from '../../assets/Send.svg'

import styles from './QuestionInput.module.css'

interface Props {
  onSend: (question: string, id?: string) => void
  disabled: boolean
  placeholder?: string
  clearOnSend?: boolean
  conversationId?: string
}

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend, conversationId }: Props) => {
  const [question, setQuestion] = useState<string>('')

  const sendQuestion = () => {
***REMOVED***if (disabled || !question.trim()) {
***REMOVED***  return
***REMOVED***

***REMOVED***if (conversationId) {
***REMOVED***  onSend(question, conversationId)
***REMOVED***
***REMOVED***  onSend(question)
***REMOVED***

***REMOVED***if (clearOnSend) {
***REMOVED***  setQuestion('')
***REMOVED***
  }

  const onEnterPress = (ev: React.KeyboardEvent<Element>) => {
***REMOVED***if (ev.key === 'Enter' && !ev.shiftKey && !(ev.nativeEvent?.isComposing === true)) {
***REMOVED***  ev.preventDefault()
***REMOVED***  sendQuestion()
***REMOVED***
  }

  const onQuestionChange = (_ev: React.FormEvent<HTMLInputElement | HTMLTextAreaElement>, newValue?: string) => {
***REMOVED***setQuestion(newValue || '')
  }

  const sendQuestionDisabled = disabled || !question.trim()

  return (
***REMOVED***<Stack horizontal className={styles.questionInputContainer}>
***REMOVED***  <TextField
***REMOVED***className={styles.questionInputTextArea}
***REMOVED***placeholder={placeholder}
***REMOVED***multiline
***REMOVED***resizable={false}
***REMOVED***borderless
***REMOVED***value={question}
***REMOVED***onChange={onQuestionChange}
***REMOVED***onKeyDown={onEnterPress}
***REMOVED***  />
***REMOVED***  <div
***REMOVED***className={styles.questionInputSendButtonContainer}
***REMOVED***role="button"
***REMOVED***tabIndex={0}
***REMOVED***aria-label="Ask question button"
***REMOVED***onClick={sendQuestion}
***REMOVED***onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? sendQuestion() : null)}>
***REMOVED***{sendQuestionDisabled ? (
***REMOVED***  <SendRegular className={styles.questionInputSendButtonDisabled} />
***REMOVED***) : (
***REMOVED***  <img src={Send} className={styles.questionInputSendButton} alt="Send Button" />
***REMOVED***)}
***REMOVED***  </div>
***REMOVED***  <div className={styles.questionInputBottomBorder} />
***REMOVED***</Stack>
  )
}
