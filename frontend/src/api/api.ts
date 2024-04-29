import { chatHistorySampleData } from '../constants/chatHistory'

import { ChatMessage, Conversation, ConversationRequest, CosmosDBHealth, CosmosDBStatus, UserInfo } from './models'

export async function conversationApi(options: ConversationRequest, abortSignal: AbortSignal): Promise<Response> {
  const response = await fetch('/conversation', {
***REMOVED***method: 'POST',
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***,
***REMOVED***body: JSON.stringify({
***REMOVED***  messages: options.messages
***REMOVED***),
***REMOVED***signal: abortSignal
  })

  return response
}

export async function getUserInfo(): Promise<UserInfo[]> {
  const response = await fetch('/.auth/me')
  if (!response.ok) {
***REMOVED***console.log('No identity provider found. Access to chat will be blocked.')
***REMOVED***return []
  }

  const payload = await response.json()
  return payload
}

// export const fetchChatHistoryInit = async (): Promise<Conversation[] | null> => {
export const fetchChatHistoryInit = (): Conversation[] | null => {
  // Make initial API call here

  return chatHistorySampleData
}

export const historyList = async (offset = 0): Promise<Conversation[] | null> => {
  const response = await fetch(`/history/list?offset=${offset}`, {
***REMOVED***method: 'GET'
  })
***REMOVED***.then(async res => {
***REMOVED***  const payload = await res.json()
***REMOVED***  if (!Array.isArray(payload)) {
***REMOVED***console.error('There was an issue fetching your data.')
***REMOVED***return null
  ***REMOVED***
***REMOVED***  const conversations: Conversation[] = await Promise.all(
***REMOVED***payload.map(async (conv: any) => {
***REMOVED***  let convMessages: ChatMessage[] = []
***REMOVED***  convMessages = await historyRead(conv.id)
***REMOVED******REMOVED***.then(res => {
***REMOVED******REMOVED***  return res
***REMOVED***)
***REMOVED******REMOVED***.catch(err => {
***REMOVED******REMOVED***  console.error('error fetching messages: ', err)
***REMOVED******REMOVED***  return []
***REMOVED***)
***REMOVED***  const conversation: Conversation = {
***REMOVED******REMOVED***id: conv.id,
***REMOVED******REMOVED***title: conv.title,
***REMOVED******REMOVED***date: conv.createdAt,
***REMOVED******REMOVED***messages: convMessages
  ***REMOVED***
***REMOVED***  return conversation
***REMOVED***)
***REMOVED***  )
***REMOVED***  return conversations
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  return null
***REMOVED***)

  return response
}

export const historyRead = async (convId: string): Promise<ChatMessage[]> => {
  const response = await fetch('/history/read', {
***REMOVED***method: 'POST',
***REMOVED***body: JSON.stringify({
***REMOVED***  conversation_id: convId
***REMOVED***),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(async res => {
***REMOVED***  if (!res) {
***REMOVED***return []
  ***REMOVED***
***REMOVED***  const payload = await res.json()
***REMOVED***  const messages: ChatMessage[] = []
***REMOVED***  if (payload?.messages) {
***REMOVED***payload.messages.forEach((msg: any) => {
***REMOVED***  const message: ChatMessage = {
***REMOVED******REMOVED***id: msg.id,
***REMOVED******REMOVED***role: msg.role,
***REMOVED******REMOVED***date: msg.createdAt,
***REMOVED******REMOVED***content: msg.content,
***REMOVED******REMOVED***feedback: msg.feedback ?? undefined
  ***REMOVED***
***REMOVED***  messages.push(message)
***REMOVED***)
  ***REMOVED***
***REMOVED***  return messages
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  return []
***REMOVED***)
  return response
}

export const historyGenerate = async (
  options: ConversationRequest,
  abortSignal: AbortSignal,
  convId?: string
): Promise<Response> => {
  let body
  if (convId) {
***REMOVED***body = JSON.stringify({
***REMOVED***  conversation_id: convId,
***REMOVED***  messages: options.messages
***REMOVED***)
  } else {
***REMOVED***body = JSON.stringify({
***REMOVED***  messages: options.messages
***REMOVED***)
  }
  const response = await fetch('/history/generate', {
***REMOVED***method: 'POST',
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***,
***REMOVED***body: body,
***REMOVED***signal: abortSignal
  })
***REMOVED***.then(res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  return new Response()
***REMOVED***)
  return response
}

export const historyUpdate = async (messages: ChatMessage[], convId: string): Promise<Response> => {
  const response = await fetch('/history/update', {
***REMOVED***method: 'POST',
***REMOVED***body: JSON.stringify({
***REMOVED***  conversation_id: convId,
***REMOVED***  messages: messages
***REMOVED***),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(async res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  const errRes: Response = {
***REMOVED***...new Response(),
***REMOVED***ok: false,
***REMOVED***status: 500
  ***REMOVED***
***REMOVED***  return errRes
***REMOVED***)
  return response
}

export const historyDelete = async (convId: string): Promise<Response> => {
  const response = await fetch('/history/delete', {
***REMOVED***method: 'DELETE',
***REMOVED***body: JSON.stringify({
***REMOVED***  conversation_id: convId
***REMOVED***),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  const errRes: Response = {
***REMOVED***...new Response(),
***REMOVED***ok: false,
***REMOVED***status: 500
  ***REMOVED***
***REMOVED***  return errRes
***REMOVED***)
  return response
}

export const historyDeleteAll = async (): Promise<Response> => {
  const response = await fetch('/history/delete_all', {
***REMOVED***method: 'DELETE',
***REMOVED***body: JSON.stringify({}),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  const errRes: Response = {
***REMOVED***...new Response(),
***REMOVED***ok: false,
***REMOVED***status: 500
  ***REMOVED***
***REMOVED***  return errRes
***REMOVED***)
  return response
}

export const historyClear = async (convId: string): Promise<Response> => {
  const response = await fetch('/history/clear', {
***REMOVED***method: 'POST',
***REMOVED***body: JSON.stringify({
***REMOVED***  conversation_id: convId
***REMOVED***),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  const errRes: Response = {
***REMOVED***...new Response(),
***REMOVED***ok: false,
***REMOVED***status: 500
  ***REMOVED***
***REMOVED***  return errRes
***REMOVED***)
  return response
}

export const historyRename = async (convId: string, title: string): Promise<Response> => {
  const response = await fetch('/history/rename', {
***REMOVED***method: 'POST',
***REMOVED***body: JSON.stringify({
***REMOVED***  conversation_id: convId,
***REMOVED***  title: title
***REMOVED***),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  const errRes: Response = {
***REMOVED***...new Response(),
***REMOVED***ok: false,
***REMOVED***status: 500
  ***REMOVED***
***REMOVED***  return errRes
***REMOVED***)
  return response
}

export const historyEnsure = async (): Promise<CosmosDBHealth> => {
  const response = await fetch('/history/ensure', {
***REMOVED***method: 'GET'
  })
***REMOVED***.then(async res => {
***REMOVED***  const respJson = await res.json()
***REMOVED***  let formattedResponse
***REMOVED***  if (respJson.message) {
***REMOVED***formattedResponse = CosmosDBStatus.Working
  ***REMOVED***
***REMOVED***if (res.status === 500) {
***REMOVED***  formattedResponse = CosmosDBStatus.NotWorking
***REMOVED*** else if (res.status === 401) {
***REMOVED***  formattedResponse = CosmosDBStatus.InvalidCredentials
***REMOVED*** else if (res.status === 422) {
***REMOVED***  formattedResponse = respJson.error
***REMOVED***
***REMOVED***  formattedResponse = CosmosDBStatus.NotConfigured
***REMOVED***
  ***REMOVED***
***REMOVED***  if (!res.ok) {
***REMOVED***return {
***REMOVED***  cosmosDB: false,
***REMOVED***  status: formattedResponse
***REMOVED***
  ***REMOVED***
***REMOVED***return {
***REMOVED***  cosmosDB: true,
***REMOVED***  status: formattedResponse
***REMOVED***
  ***REMOVED***
***REMOVED***)
***REMOVED***.catch(err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  return {
***REMOVED***cosmosDB: false,
***REMOVED***status: err
  ***REMOVED***
***REMOVED***)
  return response
}

export const frontendSettings = async (): Promise<Response | null> => {
  const response = await fetch('/frontend_settings', {
***REMOVED***method: 'GET'
  })
***REMOVED***.then(res => {
***REMOVED***  return res.json()
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  return null
***REMOVED***)

  return response
}
export const historyMessageFeedback = async (messageId: string, feedback: string): Promise<Response> => {
  const response = await fetch('/history/message_feedback', {
***REMOVED***method: 'POST',
***REMOVED***body: JSON.stringify({
***REMOVED***  message_id: messageId,
***REMOVED***  message_feedback: feedback
***REMOVED***),
***REMOVED***headers: {
***REMOVED***  'Content-Type': 'application/json'
***REMOVED***
  })
***REMOVED***.then(res => {
***REMOVED***  return res
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue logging feedback.')
***REMOVED***  const errRes: Response = {
***REMOVED***...new Response(),
***REMOVED***ok: false,
***REMOVED***status: 500
  ***REMOVED***
***REMOVED***  return errRes
***REMOVED***)
  return response
}
