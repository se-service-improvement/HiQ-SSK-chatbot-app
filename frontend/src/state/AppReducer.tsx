import { Conversation, Feedback, fetchChatHistoryInit, historyList } from '../api';
import { Action, AppState } from './AppProvider';

// Define the reducer function
export const appStateReducer = (state: AppState, action: Action): AppState => {
***REMOVED***switch (action.type) {
***REMOVED***case 'TOGGLE_CHAT_HISTORY':
***REMOVED******REMOVED***return { ...state, isChatHistoryOpen: !state.isChatHistoryOpen };
***REMOVED***case 'UPDATE_CURRENT_CHAT':
***REMOVED******REMOVED***return { ...state, currentChat: action.payload };
***REMOVED***case 'UPDATE_CHAT_HISTORY_LOADING_STATE':
***REMOVED******REMOVED***return { ...state, chatHistoryLoadingState: action.payload };
***REMOVED***case 'UPDATE_CHAT_HISTORY':
***REMOVED******REMOVED***if(!state.chatHistory || !state.currentChat){
***REMOVED******REMOVED***return state;
***REMOVED***
***REMOVED******REMOVED***let conversationIndex = state.chatHistory.findIndex(conv => conv.id === action.payload.id);
***REMOVED******REMOVED***if (conversationIndex !== -1) {
***REMOVED******REMOVED***let updatedChatHistory = [...state.chatHistory];
***REMOVED******REMOVED***updatedChatHistory[conversationIndex] = state.currentChat
***REMOVED******REMOVED***return {...state, chatHistory: updatedChatHistory}
***REMOVED******REMOVED***
***REMOVED******REMOVED***return { ...state, chatHistory: [...state.chatHistory, action.payload] };
***REMOVED***
***REMOVED***case 'UPDATE_CHAT_TITLE':
***REMOVED******REMOVED***if(!state.chatHistory){
***REMOVED******REMOVED***return { ...state, chatHistory: [] };
***REMOVED***
***REMOVED******REMOVED***let updatedChats = state.chatHistory.map(chat => {
***REMOVED******REMOVED***if (chat.id === action.payload.id) {
***REMOVED******REMOVED******REMOVED***if(state.currentChat?.id === action.payload.id){
***REMOVED******REMOVED******REMOVED***state.currentChat.title = action.payload.title;
***REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***//TODO: make api call to save new title to DB
***REMOVED******REMOVED******REMOVED***return { ...chat, title: action.payload.title };
***REMOVED******REMOVED***
***REMOVED******REMOVED***return chat;
***REMOVED***);
***REMOVED******REMOVED***return { ...state, chatHistory: updatedChats };
***REMOVED***case 'DELETE_CHAT_ENTRY':
***REMOVED******REMOVED***if(!state.chatHistory){
***REMOVED******REMOVED***return { ...state, chatHistory: [] };
***REMOVED***
***REMOVED******REMOVED***let filteredChat = state.chatHistory.filter(chat => chat.id !== action.payload);
***REMOVED******REMOVED***state.currentChat = null;
***REMOVED******REMOVED***//TODO: make api call to delete conversation from DB
***REMOVED******REMOVED***return { ...state, chatHistory: filteredChat };
***REMOVED***case 'DELETE_CHAT_HISTORY':
***REMOVED******REMOVED***//TODO: make api call to delete all conversations from DB
***REMOVED******REMOVED***return { ...state, chatHistory: [], filteredChatHistory: [], currentChat: null };
***REMOVED***case 'DELETE_CURRENT_CHAT_MESSAGES':
***REMOVED******REMOVED***//TODO: make api call to delete current conversation messages from DB
***REMOVED******REMOVED***if(!state.currentChat || !state.chatHistory){
***REMOVED******REMOVED***return state;
***REMOVED***
***REMOVED******REMOVED***const updatedCurrentChat = {
***REMOVED******REMOVED***...state.currentChat,
***REMOVED******REMOVED***messages: []
***REMOVED***;
***REMOVED******REMOVED***return {
***REMOVED******REMOVED***...state,
***REMOVED******REMOVED***currentChat: updatedCurrentChat
***REMOVED***;
***REMOVED***case 'FETCH_CHAT_HISTORY':
***REMOVED******REMOVED***return { ...state, chatHistory: action.payload };
***REMOVED***case 'SET_COSMOSDB_STATUS':
***REMOVED******REMOVED***return { ...state, isCosmosDBAvailable: action.payload };
***REMOVED***case 'FETCH_FRONTEND_SETTINGS':
***REMOVED******REMOVED***return { ...state, frontendSettings: action.payload };***REMOVED***
***REMOVED***case 'SET_FEEDBACK_STATE':
***REMOVED******REMOVED***return {
***REMOVED******REMOVED***...state,
***REMOVED******REMOVED***feedbackState: {
***REMOVED******REMOVED******REMOVED***...state.feedbackState,
***REMOVED******REMOVED******REMOVED***[action.payload.answerId]: action.payload.feedback,
***REMOVED******REMOVED***,
***REMOVED***;***REMOVED***
***REMOVED***default:
***REMOVED******REMOVED***return state;
  ***REMOVED***
};