import { Action, AppState } from './AppProvider'

// Define the reducer function
export const appStateReducer = (state: AppState, action: Action): AppState => {
  switch (action.type) {
***REMOVED***case 'TOGGLE_CHAT_HISTORY':
***REMOVED***  return { ...state, isChatHistoryOpen: !state.isChatHistoryOpen }
***REMOVED***case 'UPDATE_CURRENT_CHAT':
***REMOVED***  return { ...state, currentChat: action.payload }
***REMOVED***case 'UPDATE_CHAT_HISTORY_LOADING_STATE':
***REMOVED***  return { ...state, chatHistoryLoadingState: action.payload }
***REMOVED***case 'UPDATE_CHAT_HISTORY':
***REMOVED***  if (!state.chatHistory || !state.currentChat) {
***REMOVED***return state
  ***REMOVED***
***REMOVED***  const conversationIndex = state.chatHistory.findIndex(conv => conv.id === action.payload.id)
***REMOVED***  if (conversationIndex !== -1) {
***REMOVED***const updatedChatHistory = [...state.chatHistory]
***REMOVED***updatedChatHistory[conversationIndex] = state.currentChat
***REMOVED***return { ...state, chatHistory: updatedChatHistory }
  ***REMOVED***
***REMOVED***return { ...state, chatHistory: [...state.chatHistory, action.payload] }
  ***REMOVED***
***REMOVED***case 'UPDATE_CHAT_TITLE':
***REMOVED***  if (!state.chatHistory) {
***REMOVED***return { ...state, chatHistory: [] }
  ***REMOVED***
***REMOVED***  const updatedChats = state.chatHistory.map(chat => {
***REMOVED***if (chat.id === action.payload.id) {
***REMOVED***  if (state.currentChat?.id === action.payload.id) {
***REMOVED******REMOVED***state.currentChat.title = action.payload.title
  ***REMOVED***
***REMOVED***  //TODO: make api call to save new title to DB
***REMOVED***  return { ...chat, title: action.payload.title }
***REMOVED***
***REMOVED***return chat
  ***REMOVED***)
***REMOVED***  return { ...state, chatHistory: updatedChats }
***REMOVED***case 'DELETE_CHAT_ENTRY':
***REMOVED***  if (!state.chatHistory) {
***REMOVED***return { ...state, chatHistory: [] }
  ***REMOVED***
***REMOVED***  const filteredChat = state.chatHistory.filter(chat => chat.id !== action.payload)
***REMOVED***  state.currentChat = null
***REMOVED***  //TODO: make api call to delete conversation from DB
***REMOVED***  return { ...state, chatHistory: filteredChat }
***REMOVED***case 'DELETE_CHAT_HISTORY':
***REMOVED***  //TODO: make api call to delete all conversations from DB
***REMOVED***  return { ...state, chatHistory: [], filteredChatHistory: [], currentChat: null }
***REMOVED***case 'DELETE_CURRENT_CHAT_MESSAGES':
***REMOVED***  //TODO: make api call to delete current conversation messages from DB
***REMOVED***  if (!state.currentChat || !state.chatHistory) {
***REMOVED***return state
  ***REMOVED***
***REMOVED***  const updatedCurrentChat = {
***REMOVED***...state.currentChat,
***REMOVED***messages: []
  ***REMOVED***
***REMOVED***  return {
***REMOVED***...state,
***REMOVED***currentChat: updatedCurrentChat
  ***REMOVED***
***REMOVED***case 'FETCH_CHAT_HISTORY':
***REMOVED***  return { ...state, chatHistory: action.payload }
***REMOVED***case 'SET_COSMOSDB_STATUS':
***REMOVED***  return { ...state, isCosmosDBAvailable: action.payload }
***REMOVED***case 'FETCH_FRONTEND_SETTINGS':
***REMOVED***  return { ...state, isLoading: false, frontendSettings: action.payload }
***REMOVED***case 'SET_FEEDBACK_STATE':
***REMOVED***  return {
***REMOVED***...state,
***REMOVED***feedbackState: {
***REMOVED***  ...state.feedbackState,
***REMOVED***  [action.payload.answerId]: action.payload.feedback
***REMOVED***
  ***REMOVED***
***REMOVED***case 'SET_ANSWER_EXEC_RESULT':
***REMOVED***  return {
***REMOVED***...state,
***REMOVED***answerExecResult: {
***REMOVED***  ...state.answerExecResult,
***REMOVED***  [action.payload.answerId]: action.payload.exec_result
***REMOVED***
  ***REMOVED***
***REMOVED***default:
***REMOVED***  return state
  }
}
