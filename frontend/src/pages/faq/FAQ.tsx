import { FormEvent, useRef, useState, useEffect, useContext, useLayoutEffect } from 'react'
import { CommandBarButton, IconButton, Dialog, DialogType, Stack, DefaultButton, TextField } from '@fluentui/react'
import { SquareRegular, ShieldLockRegular, ErrorCircleRegular } from '@fluentui/react-icons'

import { useParams } from 'react-router-dom'

import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'
import uuid from 'react-uuid'
import { isEmpty } from 'lodash'
import DOMPurify from 'dompurify'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { nord } from 'react-syntax-highlighter/dist/esm/styles/prism'

import styles from './FAQ.module.css'
import Contoso from '../../assets/Contoso.svg'
import { XSSAllowTags } from '../../constants/sanatizeAllowables'

import {
  ChatMessage,
  ConversationRequest,
  conversationApi,
  Citation,
  ToolMessageContent,
  AzureSqlServerExecResults,
  ChatResponse,
  getUserInfo,
  Conversation,
  historyGenerate,
  historyUpdate,
  historyClear,
  ChatHistoryLoadingState,
  CosmosDBStatus,
  ErrorMessage,
  ExecResults,
} from "../../api";
import { Answer } from "../../components/Answer";
import { QuestionInput } from "../../components/QuestionInput";
// import { ChatHistoryPanel } from "../../components/ChatHistory/ChatHistoryPanel";
import { AppStateContext } from "../../state/AppProvider";
import { useBoolean } from "@fluentui/react-hooks";

const enum messageStatus {
  NotRunning = 'Not Running',
  Processing = 'Processing',
  Done = 'Done'
}



const FAQ = () => {
  const { faq_id } = useParams();

  useEffect(() => {
***REMOVED***// console.log("useEffect Works");
***REMOVED***// console.log(faq_id);
***REMOVED***switch (faq_id) {
***REMOVED***  case "1":
***REMOVED***makeApiRequestWithCosmosDB("I have forgotten my ID card, can I still attend my exam?", );
***REMOVED***break;
***REMOVED***  case "2":
***REMOVED***makeApiRequestWithCosmosDB("How do I request an extension to my assignment?", );
***REMOVED***break;
***REMOVED***  default:
***REMOVED***break;
***REMOVED***
  }, [])

  const appStateContext = useContext(AppStateContext)
  const ui = appStateContext?.state.frontendSettings?.ui
  const AUTH_ENABLED = appStateContext?.state.frontendSettings?.auth_enabled
  const chatMessageStreamEnd = useRef<HTMLDivElement | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [showLoadingMessage, setShowLoadingMessage] = useState<boolean>(false)
  const [activeCitation, setActiveCitation] = useState<Citation>()
  const [isCitationPanelOpen, setIsCitationPanelOpen] = useState<boolean>(false)
  const [isIntentsPanelOpen, setIsIntentsPanelOpen] = useState<boolean>(false)
  const abortFuncs = useRef([] as AbortController[])
  const [showAuthMessage, setShowAuthMessage] = useState<boolean | undefined>()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [execResults, setExecResults] = useState<ExecResults[]>([])
  const [processMessages, setProcessMessages] = useState<messageStatus>(messageStatus.NotRunning)
  const [clearingChat, setClearingChat] = useState<boolean>(false)
  const [hideErrorDialog, { toggle: toggleErrorDialog }] = useBoolean(true)
  const [errorMsg, setErrorMsg] = useState<ErrorMessage | null>()
  const [logo, setLogo] = useState('')
  const [answerId, setAnswerId] = useState<string>('')




  const [exportEmail, setExportEmail] = useState('')
  const [isExportChatDialogOpen, setExportChatDialogOpen] = useState(false)




  const errorDialogContentProps = {
***REMOVED***type: DialogType.close,
***REMOVED***title: errorMsg?.title,
***REMOVED***closeButtonAriaLabel: 'Close',
***REMOVED***subText: errorMsg?.subtitle
  }

  const modalProps = {
***REMOVED***titleAriaId: 'labelId',
***REMOVED***subtitleAriaId: 'subTextId',
***REMOVED***isBlocking: true,
***REMOVED***styles: { main: { maxWidth: 450 } }
  }

  const [ASSISTANT, TOOL, ERROR] = ['assistant', 'tool', 'error']
  const NO_CONTENT_ERROR = 'No content in messages object.'

  useEffect(() => {
***REMOVED***if (
***REMOVED***  appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.Working &&
***REMOVED***  appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured &&
***REMOVED***  appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Fail &&
***REMOVED***  hideErrorDialog
***REMOVED***) {
***REMOVED***  let subtitle = `${appStateContext.state.isCosmosDBAvailable.status}. Please contact the site administrator.`
***REMOVED***  setErrorMsg({
***REMOVED***title: 'Chat history is not enabled',
***REMOVED***subtitle: subtitle
  ***REMOVED***)
***REMOVED***  toggleErrorDialog()
***REMOVED***
  }, [appStateContext?.state.isCosmosDBAvailable])

  const handleErrorDialogClose = () => {
***REMOVED***toggleErrorDialog()
***REMOVED***setTimeout(() => {
***REMOVED***  setErrorMsg(null)
***REMOVED***, 500)
  }

  useEffect(() => {
***REMOVED***if (!appStateContext?.state.isLoading) {
***REMOVED***  setLogo(ui?.chat_logo || ui?.logo || Contoso)
***REMOVED***
  }, [appStateContext?.state.isLoading])

  useEffect(() => {
***REMOVED***setIsLoading(appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Loading)
  }, [appStateContext?.state.chatHistoryLoadingState])

  const getUserInfoList = async () => {
***REMOVED***if (!AUTH_ENABLED) {
***REMOVED***  setShowAuthMessage(false)
***REMOVED***  return
***REMOVED***
***REMOVED***const userInfoList = await getUserInfo()
***REMOVED***if (userInfoList.length === 0 && window.location.hostname !== '127.0.0.1') {
***REMOVED***  setShowAuthMessage(true)
***REMOVED***
***REMOVED***  setShowAuthMessage(false)
***REMOVED***
  }

  let assistantMessage = {} as ChatMessage
  let toolMessage = {} as ChatMessage
  let assistantContent = ''

  useEffect(() => parseExecResults(execResults), [execResults])

  const parseExecResults = (exec_results_: any): void => {
***REMOVED***if (exec_results_ == undefined) return
***REMOVED***const exec_results = exec_results_.length === 2 ? exec_results_ : exec_results_.splice(2)
***REMOVED***appStateContext?.dispatch({ type: 'SET_ANSWER_EXEC_RESULT', payload: { answerId: answerId, exec_result: exec_results } })
  }

  const processResultMessage = (resultMessage: ChatMessage, userMessage: ChatMessage, conversationId?: string) => {
***REMOVED***if (typeof resultMessage.content === "string" && resultMessage.content.includes('all_exec_results')) {
***REMOVED***  const parsedExecResults = JSON.parse(resultMessage.content) as AzureSqlServerExecResults
***REMOVED***  setExecResults(parsedExecResults.all_exec_results)
***REMOVED***  assistantMessage.context = JSON.stringify({
***REMOVED***all_exec_results: parsedExecResults.all_exec_results
  ***REMOVED***)
***REMOVED***

***REMOVED***if (resultMessage.role === ASSISTANT) {
***REMOVED***  setAnswerId(resultMessage.id)
***REMOVED***  assistantContent += resultMessage.content
***REMOVED***  assistantMessage = { ...assistantMessage, ...resultMessage }
***REMOVED***  assistantMessage.content = assistantContent

***REMOVED***  if (resultMessage.context) {
***REMOVED***toolMessage = {
***REMOVED***  id: uuid(),
***REMOVED***  role: TOOL,
***REMOVED***  content: resultMessage.context,
***REMOVED***  date: new Date().toISOString()
***REMOVED***
  ***REMOVED***
***REMOVED***

***REMOVED***if (resultMessage.role === TOOL) toolMessage = resultMessage

***REMOVED***if (!conversationId) {
***REMOVED***  isEmpty(toolMessage)
***REMOVED***? setMessages([...messages, userMessage, assistantMessage])
***REMOVED***: setMessages([...messages, userMessage, toolMessage, assistantMessage])
***REMOVED***
***REMOVED***  isEmpty(toolMessage)
***REMOVED***? setMessages([...messages, assistantMessage])
***REMOVED***: setMessages([...messages, toolMessage, assistantMessage])
***REMOVED***
  }

  const makeApiRequestWithoutCosmosDB = async (question: ChatMessage["content"], conversationId?: string) => {
***REMOVED***setIsLoading(true)
***REMOVED***setShowLoadingMessage(true)
***REMOVED***const abortController = new AbortController()
***REMOVED***abortFuncs.current.unshift(abortController)

***REMOVED***const questionContent = typeof question === 'string' ? question : [{ type: "text", text: question[0].text }, { type: "image_url", image_url: { url: question[1].image_url.url } }]
***REMOVED***question = typeof question !== 'string' && question[0]?.text?.length > 0 ? question[0].text : question

***REMOVED***const userMessage: ChatMessage = {
***REMOVED***  id: uuid(),
***REMOVED***  role: 'user',
***REMOVED***  content: questionContent as string,
***REMOVED***  date: new Date().toISOString()
***REMOVED***

***REMOVED***let conversation: Conversation | null | undefined
***REMOVED***if (!conversationId) {
***REMOVED***  conversation = {
***REMOVED***id: conversationId ?? uuid(),
***REMOVED***title: question as string,
***REMOVED***messages: [userMessage],
***REMOVED***date: new Date().toISOString()
  ***REMOVED***
***REMOVED***
***REMOVED***  conversation = appStateContext?.state?.currentChat
***REMOVED***  if (!conversation) {
***REMOVED***console.error('Conversation not found.')
***REMOVED***setIsLoading(false)
***REMOVED***setShowLoadingMessage(false)
***REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***return
  ***REMOVED***
***REMOVED***conversation.messages.push(userMessage)
  ***REMOVED***
***REMOVED***

***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: conversation })
***REMOVED***setMessages(conversation.messages)

***REMOVED***const request: ConversationRequest = {
***REMOVED***  messages: [...conversation.messages.filter(answer => answer.role !== ERROR)]
***REMOVED***

***REMOVED***let result = {} as ChatResponse
***REMOVED***try {
***REMOVED***  const response = await conversationApi(request, abortController.signal)
***REMOVED***  if (response?.body) {
***REMOVED***const reader = response.body.getReader()

***REMOVED***let runningText = ''
***REMOVED***while (true) {
***REMOVED***  setProcessMessages(messageStatus.Processing)
***REMOVED***  const { done, value } = await reader.read()
***REMOVED***  if (done) break

***REMOVED***  var text = new TextDecoder('utf-8').decode(value)
***REMOVED***  const objects = text.split('\n')
***REMOVED***  objects.forEach(obj => {
***REMOVED******REMOVED***try {
***REMOVED******REMOVED***  if (obj !== '' && obj !== '{}') {
***REMOVED******REMOVED***runningText += obj
***REMOVED******REMOVED***result = JSON.parse(runningText)
***REMOVED******REMOVED***if (result.choices?.length > 0) {
***REMOVED******REMOVED***  result.choices[0].messages.forEach(msg => {
***REMOVED******REMOVED******REMOVED***msg.id = result.id
***REMOVED******REMOVED******REMOVED***msg.date = new Date().toISOString()
***REMOVED***  ***REMOVED***)
***REMOVED******REMOVED***  if (result.choices[0].messages?.some(m => m.role === ASSISTANT)) {
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false)
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***  result.choices[0].messages.forEach(resultObj => {
***REMOVED******REMOVED******REMOVED***processResultMessage(resultObj, userMessage, conversationId)
***REMOVED***  ***REMOVED***)
***REMOVED******REMOVED*** else if (result.error) {
***REMOVED******REMOVED***  throw Error(result.error)
***REMOVED******REMOVED***
***REMOVED******REMOVED***runningText = ''
  ***REMOVED***
***REMOVED*** catch (e) {
***REMOVED******REMOVED***  if (!(e instanceof SyntaxError)) {
***REMOVED******REMOVED***console.error(e)
***REMOVED******REMOVED***throw e
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***console.log('Incomplete message. Continuing...')
  ***REMOVED***
***REMOVED***
  ***REMOVED***)
***REMOVED***
***REMOVED***conversation.messages.push(toolMessage, assistantMessage)
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: conversation })
***REMOVED***setMessages([...messages, toolMessage, assistantMessage])
  ***REMOVED***
***REMOVED*** catch (e) {
***REMOVED***  if (!abortController.signal.aborted) {
***REMOVED***let errorMessage =
***REMOVED***  'An error occurred. Please try again. If the problem persists, please contact the site administrator.'
***REMOVED***if (result.error?.message) {
***REMOVED***  errorMessage = result.error.message
***REMOVED*** else if (typeof result.error === 'string') {
***REMOVED***  errorMessage = result.error
***REMOVED***

***REMOVED***errorMessage = parseErrorMessage(errorMessage)

***REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED***  id: uuid(),
***REMOVED***  role: ERROR,
***REMOVED***  content: errorMessage,
***REMOVED***  date: new Date().toISOString()
***REMOVED***
***REMOVED***conversation.messages.push(errorChatMsg)
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: conversation })
***REMOVED***setMessages([...messages, errorChatMsg])
  ***REMOVED***
***REMOVED***setMessages([...messages, userMessage])
  ***REMOVED***
***REMOVED*** finally {
***REMOVED***  setIsLoading(false)
***REMOVED***  setShowLoadingMessage(false)
***REMOVED***  abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***  setProcessMessages(messageStatus.Done)
***REMOVED***

***REMOVED***return abortController.abort()
  }

  const makeApiRequestWithCosmosDB = async (question: ChatMessage["content"], conversationId?: string) => {
***REMOVED***setIsLoading(true)
***REMOVED***setShowLoadingMessage(true)
***REMOVED***const abortController = new AbortController()
***REMOVED***abortFuncs.current.unshift(abortController)
***REMOVED***const questionContent = typeof question === 'string' ? question : [{ type: "text", text: question[0].text }, { type: "image_url", image_url: { url: question[1].image_url.url } }]
***REMOVED***question = typeof question !== 'string' && question[0]?.text?.length > 0 ? question[0].text : question

***REMOVED***const userMessage: ChatMessage = {
***REMOVED***  id: uuid(),
***REMOVED***  role: 'user',
***REMOVED***  content: questionContent as string,
***REMOVED***  date: new Date().toISOString()
***REMOVED***

***REMOVED***let request: ConversationRequest
***REMOVED***let conversation
***REMOVED***if (conversationId) {
***REMOVED***  conversation = appStateContext?.state?.chatHistory?.find(conv => conv.id === conversationId)
***REMOVED***  if (!conversation) {
***REMOVED***console.error('Conversation not found.')
***REMOVED***setIsLoading(false)
***REMOVED***setShowLoadingMessage(false)
***REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***return
  ***REMOVED***
***REMOVED***conversation.messages.push(userMessage)
***REMOVED***request = {
***REMOVED***  messages: [...conversation.messages.filter(answer => answer.role !== ERROR)]
***REMOVED***
  ***REMOVED***
***REMOVED***
***REMOVED***  request = {
***REMOVED***messages: [userMessage].filter(answer => answer.role !== ERROR)
  ***REMOVED***
***REMOVED***  setMessages(request.messages)
***REMOVED***
***REMOVED***let result = {} as ChatResponse
***REMOVED***var errorResponseMessage = 'Please try again. If the problem persists, please contact the site administrator.'
***REMOVED***try {
***REMOVED***  const response = conversationId
***REMOVED***? await historyGenerate(request, abortController.signal, conversationId)
***REMOVED***: await historyGenerate(request, abortController.signal)
***REMOVED***  if (!response?.ok) {
***REMOVED***const responseJson = await response.json()
***REMOVED***errorResponseMessage =
***REMOVED***  responseJson.error === undefined ? errorResponseMessage : parseErrorMessage(responseJson.error)
***REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED***  id: uuid(),
***REMOVED***  role: ERROR,
***REMOVED***  content: `There was an error generating a response. Chat history can't be saved at this time. ${errorResponseMessage}`,
***REMOVED***  date: new Date().toISOString()
***REMOVED***
***REMOVED***let resultConversation
***REMOVED***if (conversationId) {
***REMOVED***  resultConversation = appStateContext?.state?.chatHistory?.find(conv => conv.id === conversationId)
***REMOVED***  if (!resultConversation) {
***REMOVED******REMOVED***console.error('Conversation not found.')
***REMOVED******REMOVED***setIsLoading(false)
***REMOVED******REMOVED***setShowLoadingMessage(false)
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED******REMOVED***return
  ***REMOVED***
***REMOVED***  resultConversation.messages.push(errorChatMsg)
***REMOVED***
***REMOVED***  setMessages([...messages, userMessage, errorChatMsg])
***REMOVED***  setIsLoading(false)
***REMOVED***  setShowLoadingMessage(false)
***REMOVED***  abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***  return
***REMOVED***
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: resultConversation })
***REMOVED***setMessages([...resultConversation.messages])
***REMOVED***return
  ***REMOVED***
***REMOVED***  if (response?.body) {
***REMOVED***const reader = response.body.getReader()

***REMOVED***let runningText = ''
***REMOVED***while (true) {
***REMOVED***  setProcessMessages(messageStatus.Processing)
***REMOVED***  const { done, value } = await reader.read()
***REMOVED***  if (done) break

***REMOVED***  var text = new TextDecoder('utf-8').decode(value)
***REMOVED***  const objects = text.split('\n')
***REMOVED***  objects.forEach(obj => {
***REMOVED******REMOVED***try {
***REMOVED******REMOVED***  if (obj !== '' && obj !== '{}') {
***REMOVED******REMOVED***runningText += obj
***REMOVED******REMOVED***result = JSON.parse(runningText)
***REMOVED******REMOVED***if (!result.choices?.[0]?.messages?.[0].content) {
***REMOVED******REMOVED***  errorResponseMessage = NO_CONTENT_ERROR
***REMOVED******REMOVED***  throw Error()
***REMOVED******REMOVED***
***REMOVED******REMOVED***if (result.choices?.length > 0) {
***REMOVED******REMOVED***  result.choices[0].messages.forEach(msg => {
***REMOVED******REMOVED******REMOVED***msg.id = result.id
***REMOVED******REMOVED******REMOVED***msg.date = new Date().toISOString()
***REMOVED***  ***REMOVED***)
***REMOVED******REMOVED***  if (result.choices[0].messages?.some(m => m.role === ASSISTANT)) {
***REMOVED******REMOVED******REMOVED***setShowLoadingMessage(false)
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***  result.choices[0].messages.forEach(resultObj => {
***REMOVED******REMOVED******REMOVED***processResultMessage(resultObj, userMessage, conversationId)
***REMOVED***  ***REMOVED***)
***REMOVED******REMOVED***
***REMOVED******REMOVED***runningText = ''
  ***REMOVED*** else if (result.error) {
***REMOVED******REMOVED***throw Error(result.error)
  ***REMOVED***
***REMOVED*** catch (e) {
***REMOVED******REMOVED***  if (!(e instanceof SyntaxError)) {
***REMOVED******REMOVED***console.error(e)
***REMOVED******REMOVED***throw e
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***console.log('Incomplete message. Continuing...')
  ***REMOVED***
***REMOVED***
  ***REMOVED***)
***REMOVED***

***REMOVED***let resultConversation
***REMOVED***if (conversationId) {
***REMOVED***  resultConversation = appStateContext?.state?.chatHistory?.find(conv => conv.id === conversationId)
***REMOVED***  if (!resultConversation) {
***REMOVED******REMOVED***console.error('Conversation not found.')
***REMOVED******REMOVED***setIsLoading(false)
***REMOVED******REMOVED***setShowLoadingMessage(false)
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED******REMOVED***return
  ***REMOVED***
***REMOVED***  isEmpty(toolMessage)
***REMOVED******REMOVED***? resultConversation.messages.push(assistantMessage)
***REMOVED******REMOVED***: resultConversation.messages.push(toolMessage, assistantMessage)
***REMOVED***
***REMOVED***  resultConversation = {
***REMOVED******REMOVED***id: result.history_metadata.conversation_id,
***REMOVED******REMOVED***title: result.history_metadata.title,
***REMOVED******REMOVED***messages: [userMessage],
***REMOVED******REMOVED***date: result.history_metadata.date
  ***REMOVED***
***REMOVED***  isEmpty(toolMessage)
***REMOVED******REMOVED***? resultConversation.messages.push(assistantMessage)
***REMOVED******REMOVED***: resultConversation.messages.push(toolMessage, assistantMessage)
***REMOVED***
***REMOVED***if (!resultConversation) {
***REMOVED***  setIsLoading(false)
***REMOVED***  setShowLoadingMessage(false)
***REMOVED***  abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***  return
***REMOVED***
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: resultConversation })
***REMOVED***isEmpty(toolMessage)
***REMOVED***  ? setMessages([...messages, assistantMessage])
***REMOVED***  : setMessages([...messages, toolMessage, assistantMessage])
  ***REMOVED***
***REMOVED*** catch (e) {
***REMOVED***  if (!abortController.signal.aborted) {
***REMOVED***let errorMessage = `An error occurred. ${errorResponseMessage}`
***REMOVED***if (result.error?.message) {
***REMOVED***  errorMessage = result.error.message
***REMOVED*** else if (typeof result.error === 'string') {
***REMOVED***  errorMessage = result.error
***REMOVED***

***REMOVED***errorMessage = parseErrorMessage(errorMessage)

***REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED***  id: uuid(),
***REMOVED***  role: ERROR,
***REMOVED***  content: errorMessage,
***REMOVED***  date: new Date().toISOString()
***REMOVED***
***REMOVED***let resultConversation
***REMOVED***if (conversationId) {
***REMOVED***  resultConversation = appStateContext?.state?.chatHistory?.find(conv => conv.id === conversationId)
***REMOVED***  if (!resultConversation) {
***REMOVED******REMOVED***console.error('Conversation not found.')
***REMOVED******REMOVED***setIsLoading(false)
***REMOVED******REMOVED***setShowLoadingMessage(false)
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED******REMOVED***return
  ***REMOVED***
***REMOVED***  resultConversation.messages.push(errorChatMsg)
***REMOVED***
***REMOVED***  if (!result.history_metadata) {
***REMOVED******REMOVED***console.error('Error retrieving data.', result)
***REMOVED******REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED******REMOVED***  id: uuid(),
***REMOVED******REMOVED***  role: ERROR,
***REMOVED******REMOVED***  content: errorMessage,
***REMOVED******REMOVED***  date: new Date().toISOString()
***REMOVED***
***REMOVED******REMOVED***setMessages([...messages, userMessage, errorChatMsg])
***REMOVED******REMOVED***setIsLoading(false)
***REMOVED******REMOVED***setShowLoadingMessage(false)
***REMOVED******REMOVED***abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED******REMOVED***return
  ***REMOVED***
***REMOVED***  resultConversation = {
***REMOVED******REMOVED***id: result.history_metadata.conversation_id,
***REMOVED******REMOVED***title: result.history_metadata.title,
***REMOVED******REMOVED***messages: [userMessage],
***REMOVED******REMOVED***date: result.history_metadata.date
  ***REMOVED***
***REMOVED***  resultConversation.messages.push(errorChatMsg)
***REMOVED***
***REMOVED***if (!resultConversation) {
***REMOVED***  setIsLoading(false)
***REMOVED***  setShowLoadingMessage(false)
***REMOVED***  abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***  return
***REMOVED***
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: resultConversation })
***REMOVED***setMessages([...messages, errorChatMsg])
  ***REMOVED***
***REMOVED***setMessages([...messages, userMessage])
  ***REMOVED***
***REMOVED*** finally {
***REMOVED***  setIsLoading(false)
***REMOVED***  setShowLoadingMessage(false)
***REMOVED***  abortFuncs.current = abortFuncs.current.filter(a => a !== abortController)
***REMOVED***  setProcessMessages(messageStatus.Done)
***REMOVED***
***REMOVED***return abortController.abort()
  }

  const clearChat = async () => {
***REMOVED***setClearingChat(true)
***REMOVED***if (appStateContext?.state.currentChat?.id && appStateContext?.state.isCosmosDBAvailable.cosmosDB) {
***REMOVED***  let response = await historyClear(appStateContext?.state.currentChat.id)
***REMOVED***  if (!response.ok) {
***REMOVED***setErrorMsg({
***REMOVED***  title: 'Error clearing current chat',
***REMOVED***  subtitle: 'Please try again. If the problem persists, please contact the site administrator.'
***REMOVED***)
***REMOVED***toggleErrorDialog()
  ***REMOVED***
***REMOVED***appStateContext?.dispatch({
***REMOVED***  type: 'DELETE_CURRENT_CHAT_MESSAGES',
***REMOVED***  payload: appStateContext?.state.currentChat.id
***REMOVED***)
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CHAT_HISTORY', payload: appStateContext?.state.currentChat })
***REMOVED***setActiveCitation(undefined)
***REMOVED***setIsCitationPanelOpen(false)
***REMOVED***setIsIntentsPanelOpen(false)
***REMOVED***setMessages([])
  ***REMOVED***
***REMOVED***
***REMOVED***setClearingChat(false)
  }

  const tryGetRaiPrettyError = (errorMessage: string) => {
***REMOVED***try {
***REMOVED***  // Using a regex to extract the JSON part that contains "innererror"
***REMOVED***  const match = errorMessage.match(/'innererror': ({.*})\}\}/)
***REMOVED***  if (match) {
***REMOVED***// Replacing single quotes with double quotes and converting Python-like booleans to JSON booleans
***REMOVED***const fixedJson = match[1]
***REMOVED***  .replace(/'/g, '"')
***REMOVED***  .replace(/\bTrue\b/g, 'true')
***REMOVED***  .replace(/\bFalse\b/g, 'false')
***REMOVED***const innerErrorJson = JSON.parse(fixedJson)
***REMOVED***let reason = ''
***REMOVED***// Check if jailbreak content filter is the reason of the error
***REMOVED***const jailbreak = innerErrorJson.content_filter_result.jailbreak
***REMOVED***if (jailbreak.filtered === true) {
***REMOVED***  reason = 'Jailbreak'
***REMOVED***

***REMOVED***// Returning the prettified error message
***REMOVED***if (reason !== '') {
***REMOVED***  return (
***REMOVED******REMOVED***'The prompt was filtered due to triggering Azure OpenAI’s content filtering system.\n' +
***REMOVED******REMOVED***'Reason: This prompt contains content flagged as ' +
***REMOVED******REMOVED***reason +
***REMOVED******REMOVED***'\n\n' +
***REMOVED******REMOVED***'Please modify your prompt and retry. Learn more: https://go.microsoft.com/fwlink/?linkid=2198766'
***REMOVED***  )
***REMOVED***
  ***REMOVED***
***REMOVED*** catch (e) {
***REMOVED***  console.error('Failed to parse the error:', e)
***REMOVED***
***REMOVED***return errorMessage
  }

  const parseErrorMessage = (errorMessage: string) => {
***REMOVED***let errorCodeMessage = errorMessage.substring(0, errorMessage.indexOf('-') + 1)
***REMOVED***const innerErrorCue = "{\\'error\\': {\\'message\\': "
***REMOVED***if (errorMessage.includes(innerErrorCue)) {
***REMOVED***  try {
***REMOVED***let innerErrorString = errorMessage.substring(errorMessage.indexOf(innerErrorCue))
***REMOVED***if (innerErrorString.endsWith("'}}")) {
***REMOVED***  innerErrorString = innerErrorString.substring(0, innerErrorString.length - 3)
***REMOVED***
***REMOVED***innerErrorString = innerErrorString.replaceAll("\\'", "'")
***REMOVED***let newErrorMessage = errorCodeMessage + ' ' + innerErrorString
***REMOVED***errorMessage = newErrorMessage
  ***REMOVED*** catch (e) {
***REMOVED***console.error('Error parsing inner error message: ', e)
  ***REMOVED***
***REMOVED***

***REMOVED***return tryGetRaiPrettyError(errorMessage)
  }

  const newChat = () => {
***REMOVED***setProcessMessages(messageStatus.Processing)
***REMOVED***setMessages([])
***REMOVED***setIsCitationPanelOpen(false)
***REMOVED***setIsIntentsPanelOpen(false)
***REMOVED***setActiveCitation(undefined)
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: null })
***REMOVED***setProcessMessages(messageStatus.Done)
  }






  


  const exportChat = () => {
***REMOVED***setExportChatDialogOpen(true)
  }

  const resetFeedbackDialog = () => {
***REMOVED***setExportChatDialogOpen(false)
  }

  const onExportChatHistory = () => {
***REMOVED***const invalidEmailMessage = document.getElementById("invalidEmail");
***REMOVED***const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

***REMOVED***if (emailRegex.test(exportEmail)) {
***REMOVED***  console.log(exportEmail);
***REMOVED***  setExportEmail('');
***REMOVED***  setExportChatDialogOpen(false)

***REMOVED***  if (invalidEmailMessage) {
***REMOVED***invalidEmailMessage.style.display = 'none';
  ***REMOVED***
***REMOVED***
***REMOVED***  if (invalidEmailMessage) {
***REMOVED***invalidEmailMessage.style.display = 'initial';
  ***REMOVED***
***REMOVED***
  }

  const updateEmail = (ev?: FormEvent<HTMLElement | HTMLInputElement>) => {
***REMOVED***setExportEmail((ev?.target as HTMLInputElement)?.value)
  }











  const stopGenerating = () => {
***REMOVED***abortFuncs.current.forEach(a => a.abort())
***REMOVED***setShowLoadingMessage(false)
***REMOVED***setIsLoading(false)
  }

  useEffect(() => {
***REMOVED***if (appStateContext?.state.currentChat) {
***REMOVED***  setMessages(appStateContext.state.currentChat.messages)
***REMOVED***
***REMOVED***  setMessages([])
***REMOVED***
  }, [appStateContext?.state.currentChat])

  useLayoutEffect(() => {
***REMOVED***const saveToDB = async (messages: ChatMessage[], id: string) => {
***REMOVED***  const response = await historyUpdate(messages, id)
***REMOVED***  return response
***REMOVED***

***REMOVED***if (appStateContext && appStateContext.state.currentChat && processMessages === messageStatus.Done) {
***REMOVED***  if (appStateContext.state.isCosmosDBAvailable.cosmosDB) {
***REMOVED***if (!appStateContext?.state.currentChat?.messages) {
***REMOVED***  console.error('Failure fetching current chat state.')
***REMOVED***  return
***REMOVED***
***REMOVED***const noContentError = appStateContext.state.currentChat.messages.find(m => m.role === ERROR)

***REMOVED***if (!noContentError) {
***REMOVED***  saveToDB(appStateContext.state.currentChat.messages, appStateContext.state.currentChat.id)
***REMOVED******REMOVED***.then(res => {
***REMOVED******REMOVED***  if (!res.ok) {
***REMOVED******REMOVED***let errorMessage =
***REMOVED******REMOVED***  "An error occurred. Answers can't be saved at this time. If the problem persists, please contact the site administrator."
***REMOVED******REMOVED***let errorChatMsg: ChatMessage = {
***REMOVED******REMOVED***  id: uuid(),
***REMOVED******REMOVED***  role: ERROR,
***REMOVED******REMOVED***  content: errorMessage,
***REMOVED******REMOVED***  date: new Date().toISOString()
***REMOVED******REMOVED***
***REMOVED******REMOVED***if (!appStateContext?.state.currentChat?.messages) {
***REMOVED******REMOVED***  let err: Error = {
***REMOVED******REMOVED******REMOVED***...new Error(),
***REMOVED******REMOVED******REMOVED***message: 'Failure fetching current chat state.'
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***  throw err
***REMOVED******REMOVED***
***REMOVED******REMOVED***setMessages([...appStateContext?.state.currentChat?.messages, errorChatMsg])
  ***REMOVED***
***REMOVED******REMOVED***  return res as Response
***REMOVED***)
***REMOVED******REMOVED***.catch(err => {
***REMOVED******REMOVED***  console.error('Error: ', err)
***REMOVED******REMOVED***  let errRes: Response = {
***REMOVED******REMOVED***...new Response(),
***REMOVED******REMOVED***ok: false,
***REMOVED******REMOVED***status: 500
  ***REMOVED***
***REMOVED******REMOVED***  return errRes
***REMOVED***)
***REMOVED***
  ***REMOVED***
  ***REMOVED***
***REMOVED***  appStateContext?.dispatch({ type: 'UPDATE_CHAT_HISTORY', payload: appStateContext.state.currentChat })
***REMOVED***  setMessages(appStateContext.state.currentChat.messages)
***REMOVED***  setProcessMessages(messageStatus.NotRunning)
***REMOVED***
  }, [processMessages])

  useEffect(() => {
***REMOVED***if (AUTH_ENABLED !== undefined) getUserInfoList()
  }, [AUTH_ENABLED])

  useLayoutEffect(() => {
***REMOVED***chatMessageStreamEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }, [showLoadingMessage, processMessages])

  const onShowCitation = (citation: Citation) => {
***REMOVED***setActiveCitation(citation)
***REMOVED***setIsCitationPanelOpen(true)
  }

  const onShowExecResult = (answerId: string) => {
***REMOVED***setIsIntentsPanelOpen(true)
  }

  const onViewSource = (citation: Citation) => {
***REMOVED***if (citation.url && !citation.url.includes('blob.core')) {
***REMOVED***  window.open(citation.url, '_blank')
***REMOVED***
  }

  const parseCitationFromMessage = (message: ChatMessage) => {
***REMOVED***if (message?.role && message?.role === 'tool' && typeof message?.content === "string") {
***REMOVED***  try {
***REMOVED***const toolMessage = JSON.parse(message.content) as ToolMessageContent
***REMOVED***return toolMessage.citations
  ***REMOVED*** catch {
***REMOVED***return []
  ***REMOVED***
***REMOVED***
***REMOVED***return []
  }

  const parsePlotFromMessage = (message: ChatMessage) => {
***REMOVED***if (message?.role && message?.role === "tool" && typeof message?.content === "string") {
***REMOVED***  try {
***REMOVED***const execResults = JSON.parse(message.content) as AzureSqlServerExecResults;
***REMOVED***const codeExecResult = execResults.all_exec_results.at(-1)?.code_exec_result;

***REMOVED***if (codeExecResult === undefined) {
***REMOVED***  return null;
***REMOVED***
***REMOVED***return codeExecResult.toString();
  ***REMOVED***
***REMOVED***  catch {
***REMOVED***return null;
  ***REMOVED***
***REMOVED***  // const execResults = JSON.parse(message.content) as AzureSqlServerExecResults;
***REMOVED***  // return execResults.all_exec_results.at(-1)?.code_exec_result;
***REMOVED***
***REMOVED***return null;
  }

  const disabledButton = () => {
***REMOVED***return (
***REMOVED***  isLoading ||
***REMOVED***  (messages && messages.length === 0) ||
***REMOVED***  clearingChat ||
***REMOVED***  appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Loading
***REMOVED***)
  }


  return (
***REMOVED***<div className={styles.container} role="main">
***REMOVED***  {showAuthMessage ? (
***REMOVED***<Stack className={styles.chatEmptyState}>
***REMOVED***  <ShieldLockRegular
***REMOVED******REMOVED***className={styles.chatIcon}
***REMOVED******REMOVED***style={{ color: 'darkorange', height: '200px', width: '200px' }}
***REMOVED***  />
***REMOVED***  <h1 className={styles.chatEmptyStateTitle}>Authentication Not Configured</h1>
***REMOVED***  <h2 className={styles.chatEmptyStateSubtitle}>
***REMOVED******REMOVED***This app does not have authentication configured. Please add an identity provider by finding your app in the{' '}
***REMOVED******REMOVED***<a href="https://portal.azure.com/" target="_blank">
***REMOVED******REMOVED***  Azure Portal
***REMOVED******REMOVED***</a>
***REMOVED******REMOVED***and following{' '}
***REMOVED******REMOVED***<a
***REMOVED******REMOVED***  href="https://learn.microsoft.com/en-us/azure/app-service/scenario-secure-app-authentication-app-service#3-configure-authentication-and-authorization"
***REMOVED******REMOVED***  target="_blank">
***REMOVED******REMOVED***  these instructions
***REMOVED******REMOVED***</a>
***REMOVED******REMOVED***.
***REMOVED***  </h2>
***REMOVED***  <h2 className={styles.chatEmptyStateSubtitle} style={{ fontSize: '20px' }}>
***REMOVED******REMOVED***<strong>Authentication configuration takes a few minutes to apply. </strong>
***REMOVED***  </h2>
***REMOVED***  <h2 className={styles.chatEmptyStateSubtitle} style={{ fontSize: '20px' }}>
***REMOVED******REMOVED***<strong>If you deployed in the last 10 minutes, please wait and reload the page after 10 minutes.</strong>
***REMOVED***  </h2>
***REMOVED***</Stack>
***REMOVED***  ) : (
***REMOVED***<Stack horizontal className={styles.chatRoot}>
***REMOVED***  <div className={styles.chatContainer}>
***REMOVED******REMOVED***{!messages || messages.length < 1 ? (
***REMOVED******REMOVED***  <Stack className={styles.chatEmptyState}>
***REMOVED******REMOVED***<img src={logo} className={styles.chatIcon} aria-hidden="true" />
***REMOVED******REMOVED***<h1 className={styles.chatEmptyStateTitle}>{ui?.chat_title}</h1>
***REMOVED******REMOVED***<h2 className={styles.chatEmptyStateSubtitle}>{ui?.chat_description}</h2>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***) : (
***REMOVED******REMOVED***  <div className={styles.chatMessageStream} style={{ marginBottom: isLoading ? '40px' : '0px' }} role="log">
***REMOVED******REMOVED***{messages.map((answer, index) => (
***REMOVED******REMOVED***  <>
***REMOVED******REMOVED******REMOVED***{answer.role === 'user' ? (
***REMOVED******REMOVED******REMOVED***  <div className={styles.chatMessageUser} tabIndex={0}>
***REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageUserMessage}>
***REMOVED******REMOVED******REMOVED***  {typeof answer.content === "string" && answer.content ? answer.content : Array.isArray(answer.content) ? <>{answer.content[0].text} <img className={styles.uploadedImageChat} src={answer.content[1].image_url.url} alt="Uploaded Preview" /></> : null}
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***  </div>
***REMOVED******REMOVED******REMOVED***) : answer.role === 'assistant' ? (
***REMOVED******REMOVED******REMOVED***  <div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED***{typeof answer.content === "string" && <Answer
***REMOVED******REMOVED******REMOVED***  answer={{
***REMOVED******REMOVED******REMOVED******REMOVED***answer: answer.content,
***REMOVED******REMOVED******REMOVED******REMOVED***citations: parseCitationFromMessage(messages[index - 1]),
***REMOVED******REMOVED******REMOVED******REMOVED***generated_chart: parsePlotFromMessage(messages[index - 1]),
***REMOVED******REMOVED******REMOVED******REMOVED***message_id: answer.id,
***REMOVED******REMOVED******REMOVED******REMOVED***feedback: answer.feedback,
***REMOVED******REMOVED******REMOVED******REMOVED***exec_results: execResults
***REMOVED******REMOVED***  ***REMOVED***}
***REMOVED******REMOVED******REMOVED***  onCitationClicked={c => onShowCitation(c)}
***REMOVED******REMOVED******REMOVED***  onExectResultClicked={() => onShowExecResult(answerId)}
***REMOVED******REMOVED******REMOVED***/>}
***REMOVED******REMOVED******REMOVED***  </div>
***REMOVED******REMOVED******REMOVED***) : answer.role === ERROR ? (
***REMOVED******REMOVED******REMOVED***  <div className={styles.chatMessageError}>
***REMOVED******REMOVED******REMOVED***<Stack horizontal className={styles.chatMessageErrorContent}>
***REMOVED******REMOVED******REMOVED***  <ErrorCircleRegular className={styles.errorIcon} style={{ color: 'rgba(182, 52, 67, 1)' }} />
***REMOVED******REMOVED******REMOVED***  <span>Error</span>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***<span className={styles.chatMessageErrorContent}>{typeof answer.content === "string" && answer.content}</span>
***REMOVED******REMOVED******REMOVED***  </div>
***REMOVED******REMOVED******REMOVED***) : null}
***REMOVED******REMOVED***  </>
***REMOVED******REMOVED***))}
***REMOVED******REMOVED***{showLoadingMessage && (
***REMOVED******REMOVED***  <>
***REMOVED******REMOVED******REMOVED***<div className={styles.chatMessageGpt}>
***REMOVED******REMOVED******REMOVED***  <Answer
***REMOVED******REMOVED******REMOVED***answer={{
***REMOVED******REMOVED******REMOVED***  answer: "Generating answer...",
***REMOVED******REMOVED******REMOVED***  citations: [],
***REMOVED******REMOVED******REMOVED***  generated_chart: null
***REMOVED******REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED***onCitationClicked={() => null}
***REMOVED******REMOVED******REMOVED***onExectResultClicked={() => null}
***REMOVED******REMOVED******REMOVED***  />
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***  </>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***<div ref={chatMessageStreamEnd} />
***REMOVED******REMOVED***  </div>
***REMOVED******REMOVED***)}

***REMOVED******REMOVED***<Stack horizontal className={styles.chatInput}>
***REMOVED******REMOVED***  {isLoading && messages.length > 0 && (
***REMOVED******REMOVED***<Stack
***REMOVED******REMOVED***  horizontal
***REMOVED******REMOVED***  className={styles.stopGeneratingContainer}
***REMOVED******REMOVED***  role="button"
***REMOVED******REMOVED***  aria-label="Stop generating"
***REMOVED******REMOVED***  tabIndex={0}
***REMOVED******REMOVED***  onClick={stopGenerating}
***REMOVED******REMOVED***  onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? stopGenerating() : null)}>
***REMOVED******REMOVED***  <SquareRegular className={styles.stopGeneratingIcon} aria-hidden="true" />
***REMOVED******REMOVED***  <span className={styles.stopGeneratingText} aria-hidden="true">
***REMOVED******REMOVED******REMOVED***Stop generating
***REMOVED******REMOVED***  </span>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  )}
***REMOVED******REMOVED***  <Stack>
***REMOVED******REMOVED***{appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured && (
***REMOVED******REMOVED***  <CommandBarButton
***REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED***styles={{
***REMOVED******REMOVED******REMOVED***  icon: {
***REMOVED******REMOVED******REMOVED***color: '#FFFFFF'
***REMOVED***  ***REMOVED***,
***REMOVED******REMOVED******REMOVED***  iconDisabled: {
***REMOVED******REMOVED******REMOVED***color: '#FFFFFF !important'
***REMOVED***  ***REMOVED***,
***REMOVED******REMOVED******REMOVED***  root: {
***REMOVED******REMOVED******REMOVED***color: '#FFFFFF',
***REMOVED******REMOVED******REMOVED***background:
***REMOVED******REMOVED******REMOVED***  'radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)'
***REMOVED***  ***REMOVED***,
***REMOVED******REMOVED******REMOVED***  rootDisabled: {
***REMOVED******REMOVED******REMOVED***background: '#606060'
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***}
***REMOVED******REMOVED******REMOVED***className={styles.newChatIcon}
***REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'Add' }}
***REMOVED******REMOVED******REMOVED***onClick={newChat}
***REMOVED******REMOVED******REMOVED***disabled={disabledButton()}
***REMOVED******REMOVED******REMOVED***aria-label="start a new chat button"
***REMOVED******REMOVED***  ><span className={styles.newChatText}>New Chat</span></CommandBarButton>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***{/* <CommandBarButton
***REMOVED******REMOVED***  role="button"
***REMOVED******REMOVED***  styles={{
***REMOVED******REMOVED******REMOVED***icon: {
***REMOVED******REMOVED******REMOVED***  color: '#FFFFFF'
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***iconDisabled: {
***REMOVED******REMOVED******REMOVED***  color: '#FFFFFF !important'
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***root: {
***REMOVED******REMOVED******REMOVED***  color: '#FFFFFF',
***REMOVED******REMOVED******REMOVED***  background:
***REMOVED******REMOVED******REMOVED***'radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)'
***REMOVED******REMOVED***,
***REMOVED******REMOVED******REMOVED***rootDisabled: {
***REMOVED******REMOVED******REMOVED***  background: '#606060'
***REMOVED******REMOVED***
***REMOVED***  ***REMOVED***}
***REMOVED******REMOVED***  className={styles.exportChatIcon}
***REMOVED******REMOVED***  iconProps={{ iconName: 'MailForward' }}
***REMOVED******REMOVED***  onClick={exportChat}
***REMOVED******REMOVED***  disabled={disabledButton()}
***REMOVED******REMOVED***  aria-label="export chat button"
***REMOVED******REMOVED***><span className={styles.exportChatText}>Email Chat</span></CommandBarButton> */}
***REMOVED******REMOVED***<Dialog
***REMOVED******REMOVED***  hidden={hideErrorDialog}
***REMOVED******REMOVED***  onDismiss={handleErrorDialogClose}
***REMOVED******REMOVED***  dialogContentProps={errorDialogContentProps}
***REMOVED******REMOVED***  modalProps={modalProps}></Dialog>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***  <QuestionInput
***REMOVED******REMOVED***clearOnSend
***REMOVED******REMOVED***placeholder="Type a new question..."
***REMOVED******REMOVED***disabled={isLoading}
***REMOVED******REMOVED***onSend={(question, id) => {
***REMOVED******REMOVED***  appStateContext?.state.isCosmosDBAvailable?.cosmosDB
***REMOVED******REMOVED******REMOVED***? makeApiRequestWithCosmosDB(question, id)
***REMOVED******REMOVED******REMOVED***: makeApiRequestWithoutCosmosDB(question, id)
***REMOVED******REMOVED***}
***REMOVED******REMOVED***conversationId={
***REMOVED******REMOVED***  appStateContext?.state.currentChat?.id ? appStateContext?.state.currentChat?.id : undefined
***REMOVED******REMOVED***
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***{/* <Dialog
***REMOVED******REMOVED***  onDismiss={() => {
***REMOVED******REMOVED***resetFeedbackDialog()
  ***REMOVED***}
***REMOVED******REMOVED***  hidden={!isExportChatDialogOpen}
***REMOVED******REMOVED***  styles={{
***REMOVED******REMOVED***main: [
***REMOVED******REMOVED***  {
***REMOVED******REMOVED******REMOVED***selectors: {
***REMOVED******REMOVED******REMOVED***  ['@media (min-width: 480px)']: {
***REMOVED******REMOVED******REMOVED***maxWidth: '600px',
***REMOVED******REMOVED******REMOVED***background: '#FFFFFF',
***REMOVED******REMOVED******REMOVED***boxShadow: '0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)',
***REMOVED******REMOVED******REMOVED***borderRadius: '8px',
***REMOVED******REMOVED******REMOVED***maxHeight: '600px',
***REMOVED******REMOVED******REMOVED***minHeight: '100px'
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***]
  ***REMOVED***}
***REMOVED******REMOVED***  dialogContentProps={{
***REMOVED******REMOVED***title: 'Email Chat History',
***REMOVED******REMOVED***showCloseButton: true
  ***REMOVED***}>
***REMOVED******REMOVED***  <Stack tokens={{ childrenGap: 4 }}>
***REMOVED******REMOVED***<div>Enter your email address below and click submit to receive an email with the chat history of this conversation.</div>
***REMOVED***  
***REMOVED******REMOVED***<label><strong>Email Address:</strong></label>
***REMOVED******REMOVED***<input
***REMOVED******REMOVED***  type="email"
***REMOVED******REMOVED***  onChange={updateEmail}></input>
***REMOVED******REMOVED***<label className={styles.invalidEmail} id='invalidEmail'>Invalid email format</label>

***REMOVED******REMOVED***<DefaultButton onClick={onExportChatHistory}>
***REMOVED******REMOVED***  Send Email
***REMOVED******REMOVED***</DefaultButton>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***</Dialog> */}
***REMOVED***  </div>
***REMOVED***  {/* Citation Panel */}
***REMOVED***  {messages && messages.length > 0 && isCitationPanelOpen && activeCitation && (
***REMOVED******REMOVED***<Stack.Item className={styles.citationPanel} tabIndex={0} role="tabpanel" aria-label="Citations Panel">
***REMOVED******REMOVED***  <Stack
***REMOVED******REMOVED***aria-label="Citations Panel Header Container"
***REMOVED******REMOVED***horizontal
***REMOVED******REMOVED***className={styles.citationPanelHeaderContainer}
***REMOVED******REMOVED***horizontalAlign="space-between"
***REMOVED******REMOVED***verticalAlign="center">
***REMOVED******REMOVED***<span aria-label="Citations" className={styles.citationPanelHeader}>
***REMOVED******REMOVED***  Citations
***REMOVED******REMOVED***</span>
***REMOVED******REMOVED***<IconButton
***REMOVED******REMOVED***  iconProps={{ iconName: 'Cancel' }}
***REMOVED******REMOVED***  aria-label="Close citations panel"
***REMOVED******REMOVED***  onClick={() => setIsCitationPanelOpen(false)}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***  <h5
***REMOVED******REMOVED***className={styles.citationPanelTitle}
***REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED***title={
***REMOVED******REMOVED***  activeCitation.url && !activeCitation.url.includes('blob.core')
***REMOVED******REMOVED******REMOVED***? activeCitation.url
***REMOVED******REMOVED******REMOVED***: activeCitation.title ?? ''
***REMOVED******REMOVED***
***REMOVED******REMOVED***onClick={() => onViewSource(activeCitation)}>
***REMOVED******REMOVED***{activeCitation.title}
***REMOVED******REMOVED***  </h5>
***REMOVED******REMOVED***  <div tabIndex={0}>
***REMOVED******REMOVED***<ReactMarkdown
***REMOVED******REMOVED***  linkTarget="_blank"
***REMOVED******REMOVED***  className={styles.citationPanelContent}
***REMOVED******REMOVED***  children={DOMPurify.sanitize(activeCitation.content, { ALLOWED_TAGS: XSSAllowTags })}
***REMOVED******REMOVED***  remarkPlugins={[remarkGfm]}
***REMOVED******REMOVED***  rehypePlugins={[rehypeRaw]}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***  </div>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED***  )}
***REMOVED***  {messages && messages.length > 0 && isIntentsPanelOpen && (
***REMOVED******REMOVED***<Stack.Item className={styles.citationPanel} tabIndex={0} role="tabpanel" aria-label="Intents Panel">
***REMOVED******REMOVED***  <Stack
***REMOVED******REMOVED***aria-label="Intents Panel Header Container"
***REMOVED******REMOVED***horizontal
***REMOVED******REMOVED***className={styles.citationPanelHeaderContainer}
***REMOVED******REMOVED***horizontalAlign="space-between"
***REMOVED******REMOVED***verticalAlign="center">
***REMOVED******REMOVED***<span aria-label="Intents" className={styles.citationPanelHeader}>
***REMOVED******REMOVED***  Intents
***REMOVED******REMOVED***</span>
***REMOVED******REMOVED***<IconButton
***REMOVED******REMOVED***  iconProps={{ iconName: 'Cancel' }}
***REMOVED******REMOVED***  aria-label="Close intents panel"
***REMOVED******REMOVED***  onClick={() => setIsIntentsPanelOpen(false)}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***  <Stack horizontalAlign="space-between">
***REMOVED******REMOVED***{appStateContext?.state?.answerExecResult[answerId]?.map((execResult: ExecResults, index) => (
***REMOVED******REMOVED***  <Stack className={styles.exectResultList} verticalAlign="space-between">
***REMOVED******REMOVED******REMOVED***<><span>Intent:</span> <p>{execResult.intent}</p></>
***REMOVED******REMOVED******REMOVED***{execResult.search_query && <><span>Search Query:</span>
***REMOVED******REMOVED******REMOVED***  <SyntaxHighlighter
***REMOVED******REMOVED******REMOVED***style={nord}
***REMOVED******REMOVED******REMOVED***wrapLines={true}
***REMOVED******REMOVED******REMOVED***lineProps={{ style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' } }}
***REMOVED******REMOVED******REMOVED***language="sql"
***REMOVED******REMOVED******REMOVED***PreTag="p">
***REMOVED******REMOVED******REMOVED***{execResult.search_query}
***REMOVED******REMOVED******REMOVED***  </SyntaxHighlighter></>}
***REMOVED******REMOVED******REMOVED***{execResult.search_result && <><span>Search Result:</span> <p>{execResult.search_result}</p></>}
***REMOVED******REMOVED******REMOVED***{execResult.code_generated && <><span>Code Generated:</span>
***REMOVED******REMOVED******REMOVED***  <SyntaxHighlighter
***REMOVED******REMOVED******REMOVED***style={nord}
***REMOVED******REMOVED******REMOVED***wrapLines={true}
***REMOVED******REMOVED******REMOVED***lineProps={{ style: { wordBreak: 'break-all', whiteSpace: 'pre-wrap' } }}
***REMOVED******REMOVED******REMOVED***language="python"
***REMOVED******REMOVED******REMOVED***PreTag="p">
***REMOVED******REMOVED******REMOVED***{execResult.code_generated}
***REMOVED******REMOVED******REMOVED***  </SyntaxHighlighter>
***REMOVED******REMOVED******REMOVED***</>}
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***))}
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED***  )}
***REMOVED***  {/* {appStateContext?.state.isChatHistoryOpen &&
***REMOVED******REMOVED***appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured && <ChatHistoryPanel />} */}
***REMOVED***</Stack>
***REMOVED***  )}

***REMOVED******REMOVED***{/* <div id={styles.top_content} className={styles.top_content}>
***REMOVED******REMOVED***  <div id={styles.header} className={styles.section_wrapper}></div>
***REMOVED******REMOVED***  <div id={styles.content} className={styles.section_wrapper}>
***REMOVED******REMOVED***  <div id={styles.content_main} className={styles.content_wrapper}>
***REMOVED******REMOVED******REMOVED***<div id={styles.intro} className={styles.info_box}>
***REMOVED******REMOVED******REMOVED***  <p><strong>Welcome to the HiQ Self-Service Kiosk</strong></p>
***REMOVED******REMOVED******REMOVED***  <p>No time to wait in line? Access quick support here. 😎✨</p>
***REMOVED******REMOVED******REMOVED***  <p>Find answers to your questions about assessments, fees, enrolment, library resources, wellbeing support, and more.</p>
***REMOVED******REMOVED******REMOVED***  <p>To get started, click the <strong>Ask a question</strong> button. Make sure your question is detailed, specific, and written in complete sentences. You can clear your chats anytime using the broom icon.</p>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***  </div>



***REMOVED******REMOVED***  <div id={styles.content_instructions} className={styles.content_wrapper}>
***REMOVED******REMOVED******REMOVED***  <div id={styles.instructions} className={styles.info_box}>
***REMOVED******REMOVED******REMOVED***  <p><strong>How to use the HiQ Self-Service Kiosk:</strong></p>
***REMOVED******REMOVED******REMOVED***  <ul>
***REMOVED******REMOVED******REMOVED******REMOVED***<li><i className={styles.material_icons}>chat</i> Click on the <strong>blue chat button</strong> at the bottom right to .</li>
***REMOVED******REMOVED******REMOVED******REMOVED***<li><i className={styles.material_icons}>question_answer</i> Type your question and press enter to receive an instant response.</li>***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED***<li><i className={styles.material_icons}>link</i> If there is a link in the response, click on it to learn more (opens in a new tab).</li>
***REMOVED******REMOVED******REMOVED******REMOVED***<li><i className={styles.material_icons}>add</i> Use the <strong>plus button</strong> to add new chat sessions.</li>
***REMOVED******REMOVED******REMOVED******REMOVED***<li><i className={styles.material_icons}>cleaning_services</i> Click the <strong>broom icon</strong> to clear the chat and start fresh.</li>***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***  <li><i className={styles.material_icons}>history</i> Click on <strong>Show chat history</strong> to view your recent chats with HiKA-AI.</li>***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***  <li><i className={styles.material_icons}>close</i> Click the "X" in the top right corner to close the chat and reset for the next user.</li>
***REMOVED******REMOVED******REMOVED***  </ul>
***REMOVED******REMOVED******REMOVED***  <p><strong>Note:</strong> Each new chat resets the conversation, so feel free to explore different questions!</p>
***REMOVED******REMOVED******REMOVED***  <br />
***REMOVED******REMOVED******REMOVED***  <p><strong>Tip for Better Questions:</strong> For the best responses, ask detailed, specific questions. Provide context (e.g., topic or department) and use complete sentences. This helps HiKA-AI give you accurate answers more quickly.</p>
***REMOVED******REMOVED******REMOVED***  </div> */}
***REMOVED******REMOVED******REMOVED***  {/* <button className={styles.floating}chat-btn" onClick={openChatInNewTab()}>Ask a question</button>
***REMOVED******REMOVED******REMOVED***  <button className={styles.feedback}btn" onClick={openFeedbackForm()}>Leave Feedback</button> */}
***REMOVED******REMOVED***  {/* </div>
***REMOVED******REMOVED***  </div>
***REMOVED******REMOVED***  <div id={styles.footer} className={styles.section_wrapper}></div>



***REMOVED******REMOVED***  <div id={styles.fixed_disclaimer} className={styles.section_wrapper}>
***REMOVED******REMOVED***  <div id={styles.content_fixed_disclaimer} className={styles.content_wrapper}>
***REMOVED******REMOVED******REMOVED***  <div id={styles.disclaimer} className={styles.info_box}>
***REMOVED******REMOVED******REMOVED***  <div id={styles.disclaimer_content}>
***REMOVED******REMOVED******REMOVED******REMOVED***  <strong><em>Disclaimer:</em></strong>
***REMOVED******REMOVED******REMOVED******REMOVED***  <br />
***REMOVED******REMOVED******REMOVED******REMOVED***  <em>The HiQ Self-Service Kiosk utilises artificial intelligence. While it aims to provide accurate and relevant information, the responses may not always be complete, current, or entirely accurate. 
***REMOVED******REMOVED******REMOVED******REMOVED***  <br />
***REMOVED******REMOVED******REMOVED******REMOVED***  Please independently verify information via the provided links, the HiQ website, or by contacting HiQ directly. Use of this kiosk is at your own risk.</em>
***REMOVED******REMOVED******REMOVED***  </div>
***REMOVED******REMOVED******REMOVED***  <i id={styles.disclaimer_close} className={styles.material_icons}>close</i>
***REMOVED******REMOVED******REMOVED***  </div>
***REMOVED******REMOVED***  </div>
***REMOVED******REMOVED***  </div>
***REMOVED***  </div> */}



***REMOVED***</div>
  )
}

export default FAQ
