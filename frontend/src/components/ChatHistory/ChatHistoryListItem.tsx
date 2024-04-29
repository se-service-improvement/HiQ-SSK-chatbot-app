import * as React from 'react'
import { useContext, useEffect, useRef, useState } from 'react'
import {
  DefaultButton,
  Dialog,
  DialogFooter,
  DialogType,
  IconButton,
  ITextField,
  List,
  PrimaryButton,
  Separator,
  Spinner,
  SpinnerSize,
  Stack,
  Text,
  TextField
} from '@fluentui/react'
import { useBoolean } from '@fluentui/react-hooks'

import { historyDelete, historyList, historyRename } from '../../api'
import { Conversation } from '../../api/models'
import { AppStateContext } from '../../state/AppProvider'

import { GroupedChatHistory } from './ChatHistoryList'

import styles from './ChatHistoryPanel.module.css'

interface ChatHistoryListItemCellProps {
  item?: Conversation
  onSelect: (item: Conversation | null) => void
}

interface ChatHistoryListItemGroupsProps {
  groupedChatHistory: GroupedChatHistory[]
}

const formatMonth = (month: string) => {
  const currentDate = new Date()
  const currentYear = currentDate.getFullYear()

  const [monthName, yearString] = month.split(' ')
  const year = parseInt(yearString)

  if (year === currentYear) {
***REMOVED***return monthName
  } else {
***REMOVED***return month
  }
}

export const ChatHistoryListItemCell: React.FC<ChatHistoryListItemCellProps> = ({ item, onSelect }) => {
  const [isHovered, setIsHovered] = React.useState(false)
  const [edit, setEdit] = useState(false)
  const [editTitle, setEditTitle] = useState('')
  const [hideDeleteDialog, { toggle: toggleDeleteDialog }] = useBoolean(true)
  const [errorDelete, setErrorDelete] = useState(false)
  const [renameLoading, setRenameLoading] = useState(false)
  const [errorRename, setErrorRename] = useState<string | undefined>(undefined)
  const [textFieldFocused, setTextFieldFocused] = useState(false)
  const textFieldRef = useRef<ITextField | null>(null)

  const appStateContext = React.useContext(AppStateContext)
  const isSelected = item?.id === appStateContext?.state.currentChat?.id
  const dialogContentProps = {
***REMOVED***type: DialogType.close,
***REMOVED***title: 'Are you sure you want to delete this item?',
***REMOVED***closeButtonAriaLabel: 'Close',
***REMOVED***subText: 'The history of this chat session will permanently removed.'
  }

  const modalProps = {
***REMOVED***titleAriaId: 'labelId',
***REMOVED***subtitleAriaId: 'subTextId',
***REMOVED***isBlocking: true,
***REMOVED***styles: { main: { maxWidth: 450 } }
  }

  if (!item) {
***REMOVED***return null
  }

  useEffect(() => {
***REMOVED***if (textFieldFocused && textFieldRef.current) {
***REMOVED***  textFieldRef.current.focus()
***REMOVED***  setTextFieldFocused(false)
***REMOVED***
  }, [textFieldFocused])

  useEffect(() => {
***REMOVED***if (appStateContext?.state.currentChat?.id !== item?.id) {
***REMOVED***  setEdit(false)
***REMOVED***  setEditTitle('')
***REMOVED***
  }, [appStateContext?.state.currentChat?.id, item?.id])

  const onDelete = async () => {
***REMOVED***const response = await historyDelete(item.id)
***REMOVED***if (!response.ok) {
***REMOVED***  setErrorDelete(true)
***REMOVED***  setTimeout(() => {
***REMOVED***setErrorDelete(false)
  ***REMOVED***, 5000)
***REMOVED***
***REMOVED***  appStateContext?.dispatch({ type: 'DELETE_CHAT_ENTRY', payload: item.id })
***REMOVED***
***REMOVED***toggleDeleteDialog()
  }

  const onEdit = () => {
***REMOVED***setEdit(true)
***REMOVED***setTextFieldFocused(true)
***REMOVED***setEditTitle(item?.title)
  }

  const handleSelectItem = () => {
***REMOVED***onSelect(item)
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: item })
  }

  const truncatedTitle = item?.title?.length > 28 ? `${item.title.substring(0, 28)} ...` : item.title

  const handleSaveEdit = async (e: any) => {
***REMOVED***e.preventDefault()
***REMOVED***if (errorRename || renameLoading) {
***REMOVED***  return
***REMOVED***
***REMOVED***if (editTitle == item.title) {
***REMOVED***  setErrorRename('Error: Enter a new title to proceed.')
***REMOVED***  setTimeout(() => {
***REMOVED***setErrorRename(undefined)
***REMOVED***setTextFieldFocused(true)
***REMOVED***if (textFieldRef.current) {
***REMOVED***  textFieldRef.current.focus()
***REMOVED***
  ***REMOVED***, 5000)
***REMOVED***  return
***REMOVED***
***REMOVED***setRenameLoading(true)
***REMOVED***const response = await historyRename(item.id, editTitle)
***REMOVED***if (!response.ok) {
***REMOVED***  setErrorRename('Error: could not rename item')
***REMOVED***  setTimeout(() => {
***REMOVED***setTextFieldFocused(true)
***REMOVED***setErrorRename(undefined)
***REMOVED***if (textFieldRef.current) {
***REMOVED***  textFieldRef.current.focus()
***REMOVED***
  ***REMOVED***, 5000)
***REMOVED***
***REMOVED***  setRenameLoading(false)
***REMOVED***  setEdit(false)
***REMOVED***  appStateContext?.dispatch({ type: 'UPDATE_CHAT_TITLE', payload: { ...item, title: editTitle } as Conversation })
***REMOVED***  setEditTitle('')
***REMOVED***
  }

  const chatHistoryTitleOnChange = (e: any) => {
***REMOVED***setEditTitle(e.target.value)
  }

  const cancelEditTitle = () => {
***REMOVED***setEdit(false)
***REMOVED***setEditTitle('')
  }

  const handleKeyPressEdit = (e: any) => {
***REMOVED***if (e.key === 'Enter') {
***REMOVED***  return handleSaveEdit(e)
***REMOVED***
***REMOVED***if (e.key === 'Escape') {
***REMOVED***  cancelEditTitle()
***REMOVED***  return
***REMOVED***
  }

  return (
***REMOVED***<Stack
***REMOVED***  key={item.id}
***REMOVED***  tabIndex={0}
***REMOVED***  aria-label="chat history item"
***REMOVED***  className={styles.itemCell}
***REMOVED***  onClick={() => handleSelectItem()}
***REMOVED***  onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? handleSelectItem() : null)}
***REMOVED***  verticalAlign="center"
***REMOVED***  // horizontal
***REMOVED***  onMouseEnter={() => setIsHovered(true)}
***REMOVED***  onMouseLeave={() => setIsHovered(false)}
***REMOVED***  styles={{
***REMOVED***root: {
***REMOVED***  backgroundColor: isSelected ? '#e6e6e6' : 'transparent'
***REMOVED***
  ***REMOVED***}>
***REMOVED***  {edit ? (
***REMOVED***<>
***REMOVED***  <Stack.Item style={{ width: '100%' }}>
***REMOVED******REMOVED***<form aria-label="edit title form" onSubmit={e => handleSaveEdit(e)} style={{ padding: '5px 0px' }}>
***REMOVED******REMOVED***  <Stack horizontal verticalAlign={'start'}>
***REMOVED******REMOVED***<Stack.Item>
***REMOVED******REMOVED***  <TextField
***REMOVED******REMOVED******REMOVED***componentRef={textFieldRef}
***REMOVED******REMOVED******REMOVED***autoFocus={textFieldFocused}
***REMOVED******REMOVED******REMOVED***value={editTitle}
***REMOVED******REMOVED******REMOVED***placeholder={item.title}
***REMOVED******REMOVED******REMOVED***onChange={chatHistoryTitleOnChange}
***REMOVED******REMOVED******REMOVED***onKeyDown={handleKeyPressEdit}
***REMOVED******REMOVED******REMOVED***// errorMessage={errorRename}
***REMOVED******REMOVED******REMOVED***disabled={errorRename ? true : false}
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***{editTitle && (
***REMOVED******REMOVED***  <Stack.Item>
***REMOVED******REMOVED******REMOVED***<Stack aria-label="action button group" horizontal verticalAlign={'center'}>
***REMOVED******REMOVED******REMOVED***  <IconButton
***REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED***disabled={errorRename !== undefined}
***REMOVED******REMOVED******REMOVED***onKeyDown={e => (e.key === ' ' || e.key === 'Enter' ? handleSaveEdit(e) : null)}
***REMOVED******REMOVED******REMOVED***onClick={e => handleSaveEdit(e)}
***REMOVED******REMOVED******REMOVED***aria-label="confirm new title"
***REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'CheckMark' }}
***REMOVED******REMOVED******REMOVED***styles={{ root: { color: 'green', marginLeft: '5px' } }}
***REMOVED******REMOVED******REMOVED***  />
***REMOVED******REMOVED******REMOVED***  <IconButton
***REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED***disabled={errorRename !== undefined}
***REMOVED******REMOVED******REMOVED***onKeyDown={e => (e.key === ' ' || e.key === 'Enter' ? cancelEditTitle() : null)}
***REMOVED******REMOVED******REMOVED***onClick={() => cancelEditTitle()}
***REMOVED******REMOVED******REMOVED***aria-label="cancel edit title"
***REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'Cancel' }}
***REMOVED******REMOVED******REMOVED***styles={{ root: { color: 'red', marginLeft: '5px' } }}
***REMOVED******REMOVED******REMOVED***  />
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  </Stack.Item>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***  {errorRename && (
***REMOVED******REMOVED***<Text
***REMOVED******REMOVED***  role="alert"
***REMOVED******REMOVED***  aria-label={errorRename}
***REMOVED******REMOVED***  style={{ fontSize: 12, fontWeight: 400, color: 'rgb(164,38,44)' }}>
***REMOVED******REMOVED***  {errorRename}
***REMOVED******REMOVED***</Text>
***REMOVED******REMOVED***  )}
***REMOVED******REMOVED***</form>
***REMOVED***  </Stack.Item>
***REMOVED***</>
***REMOVED***  ) : (
***REMOVED***<>
***REMOVED***  <Stack horizontal verticalAlign={'center'} style={{ width: '100%' }}>
***REMOVED******REMOVED***<div className={styles.chatTitle}>{truncatedTitle}</div>
***REMOVED******REMOVED***{(isSelected || isHovered) && (
***REMOVED******REMOVED***  <Stack horizontal horizontalAlign="end">
***REMOVED******REMOVED***<IconButton
***REMOVED******REMOVED***  className={styles.itemButton}
***REMOVED******REMOVED***  iconProps={{ iconName: 'Delete' }}
***REMOVED******REMOVED***  title="Delete"
***REMOVED******REMOVED***  onClick={toggleDeleteDialog}
***REMOVED******REMOVED***  onKeyDown={e => (e.key === ' ' ? toggleDeleteDialog() : null)}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***<IconButton
***REMOVED******REMOVED***  className={styles.itemButton}
***REMOVED******REMOVED***  iconProps={{ iconName: 'Edit' }}
***REMOVED******REMOVED***  title="Edit"
***REMOVED******REMOVED***  onClick={onEdit}
***REMOVED******REMOVED***  onKeyDown={e => (e.key === ' ' ? onEdit() : null)}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***)}
***REMOVED***  </Stack>
***REMOVED***</>
***REMOVED***  )}
***REMOVED***  {errorDelete && (
***REMOVED***<Text
***REMOVED***  styles={{
***REMOVED******REMOVED***root: { color: 'red', marginTop: 5, fontSize: 14 }
  ***REMOVED***}>
***REMOVED***  Error: could not delete item
***REMOVED***</Text>
***REMOVED***  )}
***REMOVED***  <Dialog
***REMOVED***hidden={hideDeleteDialog}
***REMOVED***onDismiss={toggleDeleteDialog}
***REMOVED***dialogContentProps={dialogContentProps}
***REMOVED***modalProps={modalProps}>
***REMOVED***<DialogFooter>
***REMOVED***  <PrimaryButton onClick={onDelete} text="Delete" />
***REMOVED***  <DefaultButton onClick={toggleDeleteDialog} text="Cancel" />
***REMOVED***</DialogFooter>
***REMOVED***  </Dialog>
***REMOVED***</Stack>
  )
}

export const ChatHistoryListItemGroups: React.FC<ChatHistoryListItemGroupsProps> = ({ groupedChatHistory }) => {
  const appStateContext = useContext(AppStateContext)
  const observerTarget = useRef(null)
  const [, setSelectedItem] = React.useState<Conversation | null>(null)
  const [offset, setOffset] = useState<number>(25)
  const [observerCounter, setObserverCounter] = useState(0)
  const [showSpinner, setShowSpinner] = useState(false)
  const firstRender = useRef(true)

  const handleSelectHistory = (item?: Conversation) => {
***REMOVED***if (item) {
***REMOVED***  setSelectedItem(item)
***REMOVED***
  }

  const onRenderCell = (item?: Conversation) => {
***REMOVED***return <ChatHistoryListItemCell item={item} onSelect={() => handleSelectHistory(item)} />
  }

  useEffect(() => {
***REMOVED***if (firstRender.current) {
***REMOVED***  firstRender.current = false
***REMOVED***  return
***REMOVED***
***REMOVED***handleFetchHistory()
***REMOVED***setOffset(offset => (offset += 25))
  }, [observerCounter])

  const handleFetchHistory = async () => {
***REMOVED***const currentChatHistory = appStateContext?.state.chatHistory
***REMOVED***setShowSpinner(true)

***REMOVED***await historyList(offset).then(response => {
***REMOVED***  const concatenatedChatHistory = currentChatHistory && response && currentChatHistory.concat(...response)
***REMOVED***  if (response) {
***REMOVED***appStateContext?.dispatch({ type: 'FETCH_CHAT_HISTORY', payload: concatenatedChatHistory || response })
  ***REMOVED***
***REMOVED***appStateContext?.dispatch({ type: 'FETCH_CHAT_HISTORY', payload: null })
  ***REMOVED***
***REMOVED***  setShowSpinner(false)
***REMOVED***  return response
***REMOVED***)
  }

  useEffect(() => {
***REMOVED***const observer = new IntersectionObserver(
***REMOVED***  entries => {
***REMOVED***if (entries[0].isIntersecting) setObserverCounter(observerCounter => (observerCounter += 1))
  ***REMOVED***,
***REMOVED***  { threshold: 1 }
***REMOVED***)

***REMOVED***if (observerTarget.current) observer.observe(observerTarget.current)

***REMOVED***return () => {
***REMOVED***  if (observerTarget.current) observer.unobserve(observerTarget.current)
***REMOVED***
  }, [observerTarget])

  return (
***REMOVED***<div className={styles.listContainer} data-is-scrollable>
***REMOVED***  {groupedChatHistory.map(
***REMOVED***group =>
***REMOVED***  group.entries.length > 0 && (
***REMOVED******REMOVED***<Stack
***REMOVED******REMOVED***  horizontalAlign="start"
***REMOVED******REMOVED***  verticalAlign="center"
***REMOVED******REMOVED***  key={group.month}
***REMOVED******REMOVED***  className={styles.chatGroup}
***REMOVED******REMOVED***  aria-label={`chat history group: ${group.month}`}>
***REMOVED******REMOVED***  <Stack aria-label={group.month} className={styles.chatMonth}>
***REMOVED******REMOVED***{formatMonth(group.month)}
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***  <List
***REMOVED******REMOVED***aria-label={`chat history list`}
***REMOVED******REMOVED***items={group.entries}
***REMOVED******REMOVED***onRenderCell={onRenderCell}
***REMOVED******REMOVED***className={styles.chatList}
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***  <div ref={observerTarget} />
***REMOVED******REMOVED***  <Separator
***REMOVED******REMOVED***styles={{
***REMOVED******REMOVED***  root: {
***REMOVED******REMOVED******REMOVED***width: '100%',
***REMOVED******REMOVED******REMOVED***position: 'relative',
***REMOVED******REMOVED******REMOVED***'::before': {
***REMOVED******REMOVED******REMOVED***  backgroundColor: '#d6d6d6'
***REMOVED******REMOVED***
***REMOVED***  ***REMOVED***
***REMOVED******REMOVED***}
***REMOVED******REMOVED***  />
***REMOVED******REMOVED***</Stack>
***REMOVED***  )
***REMOVED***  )}
***REMOVED***  {showSpinner && (
***REMOVED***<div className={styles.spinnerContainer}>
***REMOVED***  <Spinner size={SpinnerSize.small} aria-label="loading more chat history" className={styles.spinner} />
***REMOVED***</div>
***REMOVED***  )}
***REMOVED***</div>
  )
}
