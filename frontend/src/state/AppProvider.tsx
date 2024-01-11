import React, { createContext, useReducer, ReactNode, useEffect } from 'react';
import { appStateReducer } from './AppReducer';
import { Conversation, ChatHistoryLoadingState, CosmosDBHealth, historyList, historyEnsure, CosmosDBStatus, frontendSettings, FrontendSettings, Feedback } from '../api';
  
export interface AppState {
***REMOVED***isChatHistoryOpen: boolean;
***REMOVED***chatHistoryLoadingState: ChatHistoryLoadingState;
***REMOVED***isCosmosDBAvailable: CosmosDBHealth;
***REMOVED***chatHistory: Conversation[] | null;
***REMOVED***filteredChatHistory: Conversation[] | null;
***REMOVED***currentChat: Conversation | null;
***REMOVED***frontendSettings: FrontendSettings | null;
***REMOVED***feedbackState: { [answerId: string]: Feedback.Neutral | Feedback.Positive | Feedback.Negative; };
}

export type Action =
***REMOVED***| { type: 'TOGGLE_CHAT_HISTORY' }
***REMOVED***| { type: 'SET_COSMOSDB_STATUS', payload: CosmosDBHealth }
***REMOVED***| { type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState }
***REMOVED***| { type: 'UPDATE_CURRENT_CHAT', payload: Conversation | null }
***REMOVED***| { type: 'UPDATE_FILTERED_CHAT_HISTORY', payload: Conversation[] | null }
***REMOVED***| { type: 'UPDATE_CHAT_HISTORY', payload: Conversation } // API Call
***REMOVED***| { type: 'UPDATE_CHAT_TITLE', payload: Conversation } // API Call
***REMOVED***| { type: 'DELETE_CHAT_ENTRY', payload: string } // API Call
***REMOVED***| { type: 'DELETE_CHAT_HISTORY'}  // API Call
***REMOVED***| { type: 'DELETE_CURRENT_CHAT_MESSAGES', payload: string }  // API Call
***REMOVED***| { type: 'FETCH_CHAT_HISTORY', payload: Conversation[] | null }  // API Call
***REMOVED***| { type: 'FETCH_FRONTEND_SETTINGS', payload: FrontendSettings | null }  // API Call
***REMOVED***| { type: 'SET_FEEDBACK_STATE'; payload: { answerId: string; feedback: Feedback.Positive | Feedback.Negative | Feedback.Neutral } }
***REMOVED***| { type: 'GET_FEEDBACK_STATE'; payload: string };

const initialState: AppState = {
***REMOVED***isChatHistoryOpen: false,
***REMOVED***chatHistoryLoadingState: ChatHistoryLoadingState.Loading,
***REMOVED***chatHistory: null,
***REMOVED***filteredChatHistory: null,
***REMOVED***currentChat: null,
***REMOVED***isCosmosDBAvailable: {
***REMOVED***cosmosDB: false,
***REMOVED***status: CosmosDBStatus.NotConfigured,
***REMOVED***,
***REMOVED***frontendSettings: null,
***REMOVED***feedbackState: {}
};

export const AppStateContext = createContext<{
***REMOVED***state: AppState;
***REMOVED***dispatch: React.Dispatch<Action>;
  } | undefined>(undefined);

type AppStateProviderProps = {
***REMOVED***children: ReactNode;
  };
  
  export const AppStateProvider: React.FC<AppStateProviderProps> = ({ children }) => {
***REMOVED***const [state, dispatch] = useReducer(appStateReducer, initialState);

***REMOVED***useEffect(() => {
***REMOVED***// Check for cosmosdb config and fetch initial data here
***REMOVED***const fetchChatHistory = async (offset=0): Promise<Conversation[] | null> => {
***REMOVED******REMOVED***const result = await historyList(offset).then((response) => {
***REMOVED******REMOVED***if(response){
***REMOVED******REMOVED******REMOVED***dispatch({ type: 'FETCH_CHAT_HISTORY', payload: response});
***REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED***dispatch({ type: 'FETCH_CHAT_HISTORY', payload: null });
***REMOVED******REMOVED***
***REMOVED******REMOVED***return response
***REMOVED***)
***REMOVED******REMOVED***.catch((err) => {
***REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail });
***REMOVED******REMOVED***dispatch({ type: 'FETCH_CHAT_HISTORY', payload: null });
***REMOVED******REMOVED***console.error("There was an issue fetching your data.");
***REMOVED******REMOVED***return null
***REMOVED***)
***REMOVED******REMOVED***return result
***REMOVED***;

***REMOVED***const getHistoryEnsure = async () => {
***REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Loading });
***REMOVED******REMOVED***historyEnsure().then((response) => {
***REMOVED******REMOVED***if(response?.cosmosDB){
***REMOVED******REMOVED******REMOVED***fetchChatHistory()
***REMOVED******REMOVED******REMOVED***.then((res) => {
***REMOVED******REMOVED******REMOVED***if(res){
***REMOVED******REMOVED******REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Success });
***REMOVED******REMOVED******REMOVED******REMOVED***dispatch({ type: 'SET_COSMOSDB_STATUS', payload: response });
***REMOVED******REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail });
***REMOVED******REMOVED******REMOVED******REMOVED***dispatch({ type: 'SET_COSMOSDB_STATUS', payload: {cosmosDB: false, status: CosmosDBStatus.NotWorking} });
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED***)
***REMOVED******REMOVED******REMOVED***.catch((err) => {
***REMOVED******REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail });
***REMOVED******REMOVED******REMOVED***dispatch({ type: 'SET_COSMOSDB_STATUS', payload: {cosmosDB: false, status: CosmosDBStatus.NotWorking} });
***REMOVED******REMOVED***)
***REMOVED******REMOVED***else{
***REMOVED******REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail });
***REMOVED******REMOVED******REMOVED***dispatch({ type: 'SET_COSMOSDB_STATUS', payload: response });
***REMOVED******REMOVED***
***REMOVED***)
***REMOVED******REMOVED***.catch((err) => {
***REMOVED******REMOVED***dispatch({ type: 'UPDATE_CHAT_HISTORY_LOADING_STATE', payload: ChatHistoryLoadingState.Fail });
***REMOVED******REMOVED***dispatch({ type: 'SET_COSMOSDB_STATUS', payload: {cosmosDB: false, status: CosmosDBStatus.NotConfigured} });
***REMOVED***)
***REMOVED***
***REMOVED***getHistoryEnsure();
***REMOVED***, []);

***REMOVED***useEffect(() => {
***REMOVED***const getFrontendSettings = async () => {
***REMOVED******REMOVED***frontendSettings().then((response) => {
***REMOVED******REMOVED***dispatch({ type: 'FETCH_FRONTEND_SETTINGS', payload: response as FrontendSettings });
***REMOVED***)
***REMOVED******REMOVED***.catch((err) => {
***REMOVED******REMOVED***console.error("There was an issue fetching your data.");
***REMOVED***)
***REMOVED***
***REMOVED***getFrontendSettings();
***REMOVED***, []);
  
***REMOVED***return (
***REMOVED***  <AppStateContext.Provider value={{ state, dispatch }}>
***REMOVED***{children}
***REMOVED***  </AppStateContext.Provider>
***REMOVED***);
  };


