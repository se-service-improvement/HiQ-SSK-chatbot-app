import React, {
  createContext,
  ReactNode,
  useEffect,
  useReducer
} from 'react'

import {
  ChatHistoryLoadingState,
  Conversation,
  CosmosDBHealth,
  CosmosDBStatus,
  Feedback,
  FrontendSettings,
  frontendSettings,
  historyEnsure,
  historyList
} from '../api'

import { appStateReducer } from './AppReducer'

export interface AppState {
  isChatHistoryOpen: boolean
  chatHistoryLoadingState: ChatHistoryLoadingState
  isCosmosDBAvailable: CosmosDBHealth
  chatHistory: Conversation[] | null
  filteredChatHistory: Conversation[] | null
  currentChat: Conversation | null
  frontendSettings: FrontendSettings | null
  feedbackState: { [answerId: string]: Feedback.Neutral | Feedback.Positive | Feedback.Negative }
  isLoading: boolean;
}

export type Action =
  | { type: 'TOGGLE_CHAT_HISTORY' }
  | { type: 'SET_COSMOSDB_STATUS'; payload: CosmosDBHealth }
  | { type: 'UPDATE_CHAT_HISTORY_LOADING_STATE'; payload: ChatHistoryLoadingState }
  | { type: 'UPDATE_CURRENT_CHAT'; payload: Conversation | null }
  | { type: 'UPDATE_FILTERED_CHAT_HISTORY'; payload: Conversation[] | null }
  | { type: 'UPDATE_CHAT_HISTORY'; payload: Conversation }
  | { type: 'UPDATE_CHAT_TITLE'; payload: Conversation }
  | { type: 'DELETE_CHAT_ENTRY'; payload: string }
  | { type: 'DELETE_CHAT_HISTORY' }
  | { type: 'DELETE_CURRENT_CHAT_MESSAGES'; payload: string }
  | { type: 'FETCH_CHAT_HISTORY'; payload: Conversation[] | null }
  | { type: 'FETCH_FRONTEND_SETTINGS'; payload: FrontendSettings | null }
  | {
***REMOVED***type: 'SET_FEEDBACK_STATE'
***REMOVED***payload: { answerId: string; feedback: Feedback.Positive | Feedback.Negative | Feedback.Neutral }
  }
  | { type: 'GET_FEEDBACK_STATE'; payload: string }

const initialState: AppState = {
  isChatHistoryOpen: false,
  chatHistoryLoadingState: ChatHistoryLoadingState.Loading,
  chatHistory: null,
  filteredChatHistory: null,
  currentChat: null,
  isCosmosDBAvailable: {
***REMOVED***cosmosDB: false,
***REMOVED***status: CosmosDBStatus.NotConfigured
  },
  frontendSettings: null,
  feedbackState: {},
  isLoading: true
}

export const AppStateContext = createContext<
  | {
***REMOVED***state: AppState
***REMOVED***dispatch: React.Dispatch<Action>
  }
  | undefined
>(undefined)

type AppStateProviderProps = {
  children: ReactNode
}

export const AppStateProvider: React.FC<AppStateProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(appStateReducer, initialState)

  useEffect(() => {
***REMOVED***// Check for cosmosdb config and fetch initial data here
***REMOVED***const fetchChatHistory = async (offset = 0): Promise<Conversation[] | null> => {
***REMOVED***  const result = await historyList(offset)
***REMOVED***.then(response => {
***REMOVED***  if (response) {
***REMOVED******REMOVED***dispatch({ type: 'FETCH_CHAT_HISTORY', payload: response })
  ***REMOVED***
***REMOVED******REMOVED***dispatch({ type: 'FETCH_CHAT_HISTORY', payload: null })
  ***REMOVED***
***REMOVED***  return response
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail })
***REMOVED***  dispatch({ type: 'FETCH_CHAT_HISTORY', payload: null })
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***  return null
***REMOVED***)
***REMOVED***  return result
***REMOVED***

***REMOVED***const getHistoryEnsure = async () => {
***REMOVED***  dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Loading })
***REMOVED***  historyEnsure()
***REMOVED***.then(response => {
***REMOVED***  if (response?.cosmosDB) {
***REMOVED******REMOVED***fetchChatHistory()
***REMOVED******REMOVED***  .then(res => {
***REMOVED******REMOVED***if (res) {
***REMOVED******REMOVED***  dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Success })
***REMOVED******REMOVED***  dispatch({ type: 'SET_COSMOSDB_STATUS', payload: response })
***REMOVED******REMOVED***
***REMOVED******REMOVED***  dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail })
***REMOVED******REMOVED***  dispatch({
***REMOVED******REMOVED******REMOVED***type: 'SET_COSMOSDB_STATUS',
***REMOVED******REMOVED******REMOVED***payload: { cosmosDB: false, status: CosmosDBStatus.NotWorking }
***REMOVED***  ***REMOVED***)
***REMOVED******REMOVED***
  ***REMOVED***)
***REMOVED******REMOVED***  .catch(_err => {
***REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail })
***REMOVED******REMOVED***dispatch({
***REMOVED******REMOVED***  type: 'SET_COSMOSDB_STATUS',
***REMOVED******REMOVED***  payload: { cosmosDB: false, status: CosmosDBStatus.NotWorking }
***REMOVED******REMOVED***)
  ***REMOVED***)
  ***REMOVED***
***REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail })
***REMOVED******REMOVED***dispatch({ type: 'SET_COSMOSDB_STATUS', payload: response })
  ***REMOVED***
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail })
***REMOVED***  dispatch({ type: 'SET_COSMOSDB_STATUS', payload: { cosmosDB: false, status: CosmosDBStatus.NotConfigured } })
***REMOVED***)
***REMOVED***
***REMOVED***getHistoryEnsure()
  }, [])

  useEffect(() => {
***REMOVED***const getFrontendSettings = async () => {
***REMOVED***  frontendSettings()
***REMOVED***.then(response => {
***REMOVED***  dispatch({ type: 'FETCH_FRONTEND_SETTINGS', payload: response as FrontendSettings })
***REMOVED***)
***REMOVED***.catch(_err => {
***REMOVED***  console.error('There was an issue fetching your data.')
***REMOVED***)
***REMOVED***
***REMOVED***getFrontendSettings()
  }, [])

  return <AppStateContext.Provider value={{ state, dispatch }}>{children}</AppStateContext.Provider>
}
