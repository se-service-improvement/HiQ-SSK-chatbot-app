import { useContext, useState } from 'react'
import { FontIcon, Stack, TextField } from '@fluentui/react'
import { SendRegular } from '@fluentui/react-icons'

import Send from '../../assets/Send.svg'

import styles from './QuestionInput.module.css'
import { ChatMessage } from '../../api'
import { AppStateContext } from '../../state/AppProvider'

interface Props {
  onSend: (question: ChatMessage['content'], id?: string) => void
  disabled: boolean
  placeholder?: string
  clearOnSend?: boolean
  conversationId?: string
}

export const QuestionInput = ({ onSend, disabled, placeholder, clearOnSend, conversationId }: Props) => {
  const [question, setQuestion] = useState<string>('')
  const [base64Image, setBase64Image] = useState<string | null>(null);

  const appStateContext = useContext(AppStateContext)
  const OYD_ENABLED = appStateContext?.state.frontendSettings?.oyd_enabled || false;

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
***REMOVED***const file = event.target.files?.[0];

***REMOVED***if (file) {
***REMOVED***  await convertToBase64(file);
***REMOVED***
  };

  const convertToBase64 = async (file: Blob) => {
***REMOVED***const reader = new FileReader();

***REMOVED***reader.readAsDataURL(file);

***REMOVED***reader.onloadend = () => {
***REMOVED***  setBase64Image(reader.result as string);
***REMOVED***;

***REMOVED***reader.onerror = (error) => {
***REMOVED***  console.error('Error: ', error);
***REMOVED***;
  };

  const sendQuestion = () => {
***REMOVED***if (disabled || !question.trim()) {
***REMOVED***  return
***REMOVED***

***REMOVED***const questionTest: ChatMessage["content"] = base64Image ? [{ type: "text", text: question }, { type: "image_url", image_url: { url: base64Image } }] : question.toString();

***REMOVED***if (conversationId && questionTest !== undefined) {
***REMOVED***  onSend(questionTest, conversationId)
***REMOVED***  setBase64Image(null)
***REMOVED***
***REMOVED***  onSend(questionTest)
***REMOVED***  setBase64Image(null)
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
***REMOVED***  {!OYD_ENABLED && (
***REMOVED***<div className={styles.fileInputContainer}>
***REMOVED***  <input
***REMOVED******REMOVED***type="file"
***REMOVED******REMOVED***id="fileInput"
***REMOVED******REMOVED***onChange={(event) => handleImageUpload(event)}
***REMOVED******REMOVED***accept="image/*"
***REMOVED******REMOVED***className={styles.fileInput}
***REMOVED***  />
***REMOVED***  <label htmlFor="fileInput" className={styles.fileLabel} aria-label='Upload Image'>
***REMOVED******REMOVED***<FontIcon
***REMOVED******REMOVED***  className={styles.fileIcon}
***REMOVED******REMOVED***  iconName={'PhotoCollection'}
***REMOVED******REMOVED***  aria-label='Upload Image'
***REMOVED******REMOVED***/>
***REMOVED***  </label>
***REMOVED***</div>)}
***REMOVED***  {base64Image && <img className={styles.uploadedImage} src={base64Image} alt="Uploaded Preview" />}
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
