import { GroupedList, IGroup, IGroupHeaderProps, IRenderFunction, List, Stack, StackItem, Text } from '@fluentui/react';
import React, { useContext } from 'react';
import { AppStateContext } from '../../state/AppProvider';
import { ChatHistoryListItemGroups } from './ChatHistoryListItem';
import { Conversation } from '../../api/models';

interface ChatHistoryListProps {}

export interface GroupedChatHistory {
***REMOVED***month: string;
***REMOVED***entries: Conversation[]
}

const groupByMonth = (entries: Conversation[]) => {
***REMOVED***const groups: GroupedChatHistory[] = [{ month: "Recent", entries: [] }];
***REMOVED***const currentDate = new Date();
  
***REMOVED***entries.forEach((entry) => {
***REMOVED***const date = new Date(entry.date);
***REMOVED***const daysDifference = (currentDate.getTime() - date.getTime()) / (1000 * 60 * 60 * 24);
***REMOVED***const monthYear = date.toLocaleString('default', { month: 'long', year: 'numeric' })
***REMOVED***const existingGroup = groups.find((group) => group.month === monthYear);
***REMOVED***
***REMOVED***if(daysDifference <= 7){
***REMOVED******REMOVED***groups[0].entries.push(entry);
***REMOVED***else{
***REMOVED******REMOVED***if (existingGroup) {
***REMOVED******REMOVED***existingGroup.entries.push(entry);
***REMOVED******REMOVED***
***REMOVED******REMOVED***groups.push({ month: monthYear, entries: [entry] });
***REMOVED***
***REMOVED***
***REMOVED***);

***REMOVED***groups.sort((a, b) => {
***REMOVED***// Check if either group has no entries and handle it
***REMOVED***if (a.entries.length === 0 && b.entries.length === 0) {
***REMOVED******REMOVED***return 0; // No change in order
***REMOVED*** else if (a.entries.length === 0) {
***REMOVED******REMOVED***return 1; // Move 'a' to a higher index (bottom)
***REMOVED*** else if (b.entries.length === 0) {
***REMOVED******REMOVED***return -1; // Move 'b' to a higher index (bottom)
***REMOVED***
***REMOVED***const dateA = new Date(a.entries[0].date);
***REMOVED***const dateB = new Date(b.entries[0].date);
***REMOVED***return dateB.getTime() - dateA.getTime();
***REMOVED***);

***REMOVED***groups.forEach((group) => {
***REMOVED***group.entries.sort((a, b) => {
***REMOVED******REMOVED***const dateA = new Date(a.date);
***REMOVED******REMOVED***const dateB = new Date(b.date);
***REMOVED******REMOVED***return dateB.getTime() - dateA.getTime();
***REMOVED***);
***REMOVED***);
  
***REMOVED***return groups;
};

const ChatHistoryList: React.FC<ChatHistoryListProps> = () => {
***REMOVED***const appStateContext = useContext(AppStateContext);
***REMOVED***const chatHistory = appStateContext?.state.chatHistory;

***REMOVED***React.useEffect(() => {}, [appStateContext?.state.chatHistory]);
***REMOVED***
***REMOVED***let groupedChatHistory;
***REMOVED***if(chatHistory && chatHistory.length > 0){
***REMOVED***groupedChatHistory = groupByMonth(chatHistory);
***REMOVED***else{
***REMOVED***return <Stack horizontal horizontalAlign='center' verticalAlign='center' style={{ width: "100%", marginTop: 10 }}>
***REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED***<Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 14 }}>
***REMOVED******REMOVED******REMOVED***<span>No chat history.</span>
***REMOVED******REMOVED***</Text>
***REMOVED******REMOVED***</StackItem>
***REMOVED***</Stack>
***REMOVED***
***REMOVED***
***REMOVED***return (
***REMOVED***<ChatHistoryListItemGroups groupedChatHistory={groupedChatHistory}/>
***REMOVED***);
};

export default ChatHistoryList;
