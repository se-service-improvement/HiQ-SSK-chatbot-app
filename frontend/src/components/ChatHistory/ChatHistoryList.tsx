import React, { useContext } from 'react'
import { Stack, StackItem, Text } from '@fluentui/react'

import { Conversation } from '../../api/models'
import { AppStateContext } from '../../state/AppProvider'

import { ChatHistoryListItemGroups } from './ChatHistoryListItem'

interface ChatHistoryListProps {}

export interface GroupedChatHistory {
  month: string
  entries: Conversation[]
}

const groupByMonth = (entries: Conversation[]) => {
  const groups: GroupedChatHistory[] = [{ month: 'Recent', entries: [] }]
  const currentDate = new Date()

  entries.forEach(entry => {
***REMOVED***const date = new Date(entry.date)
***REMOVED***const daysDifference = (currentDate.getTime() - date.getTime()) / (1000 * 60 * 60 * 24)
***REMOVED***const monthYear = date.toLocaleString('default', { month: 'long', year: 'numeric' })
***REMOVED***const existingGroup = groups.find(group => group.month === monthYear)

***REMOVED***if (daysDifference <= 7) {
***REMOVED***  groups[0].entries.push(entry)
***REMOVED***
***REMOVED***  if (existingGroup) {
***REMOVED***existingGroup.entries.push(entry)
  ***REMOVED***
***REMOVED***groups.push({ month: monthYear, entries: [entry] })
  ***REMOVED***
***REMOVED***
  })

  groups.sort((a, b) => {
***REMOVED***// Check if either group has no entries and handle it
***REMOVED***if (a.entries.length === 0 && b.entries.length === 0) {
***REMOVED***  return 0 // No change in order
***REMOVED*** else if (a.entries.length === 0) {
***REMOVED***  return 1 // Move 'a' to a higher index (bottom)
***REMOVED*** else if (b.entries.length === 0) {
***REMOVED***  return -1 // Move 'b' to a higher index (bottom)
***REMOVED***
***REMOVED***const dateA = new Date(a.entries[0].date)
***REMOVED***const dateB = new Date(b.entries[0].date)
***REMOVED***return dateB.getTime() - dateA.getTime()
  })

  groups.forEach(group => {
***REMOVED***group.entries.sort((a, b) => {
***REMOVED***  const dateA = new Date(a.date)
***REMOVED***  const dateB = new Date(b.date)
***REMOVED***  return dateB.getTime() - dateA.getTime()
***REMOVED***)
  })

  return groups
}

const ChatHistoryList: React.FC<ChatHistoryListProps> = () => {
  const appStateContext = useContext(AppStateContext)
  const chatHistory = appStateContext?.state.chatHistory

  React.useEffect(() => {}, [appStateContext?.state.chatHistory])

  let groupedChatHistory
  if (chatHistory && chatHistory.length > 0) {
***REMOVED***groupedChatHistory = groupByMonth(chatHistory)
  } else {
***REMOVED***return (
***REMOVED***  <Stack horizontal horizontalAlign="center" verticalAlign="center" style={{ width: '100%', marginTop: 10 }}>
***REMOVED***<StackItem>
***REMOVED***  <Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 14 }}>
***REMOVED******REMOVED***<span>No chat history.</span>
***REMOVED***  </Text>
***REMOVED***</StackItem>
***REMOVED***  </Stack>
***REMOVED***)
  }

  return <ChatHistoryListItemGroups groupedChatHistory={groupedChatHistory} />
}

export default ChatHistoryList
