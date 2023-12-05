import * as React from 'react';
import { DefaultButton, Dialog, DialogFooter, DialogType, Text, IconButton, List, PrimaryButton, Separator, Stack, TextField, ITextField, Spinner, SpinnerSize } from '@fluentui/react';

import { AppStateContext } from '../../state/AppProvider';
import { GroupedChatHistory } from './ChatHistoryList';

import styles from "./ChatHistoryPanel.module.css"
import { useBoolean } from '@fluentui/react-hooks';
import { Conversation } from '../../api/models';
import { historyDelete, historyRename, historyList } from '../../api';
import { useEffect, useRef, useState, useContext } from 'react';

interface ChatHistoryListItemCellProps {
  item?: Conversation;
  onSelect: (item: Conversation | null) => void;
}

interface ChatHistoryListItemGroupsProps {
  groupedChatHistory: GroupedChatHistory[];
}

const formatMonth = (month: string) => {
***REMOVED***const currentDate = new Date();
***REMOVED***const currentYear = currentDate.getFullYear();
***REMOVED***
***REMOVED***const [monthName, yearString] = month.split(' ');
***REMOVED***const year = parseInt(yearString);

***REMOVED***if (year === currentYear) {
***REMOVED***return monthName;
***REMOVED***
***REMOVED***return month;
***REMOVED***
};

export const ChatHistoryListItemCell: React.FC<ChatHistoryListItemCellProps> = ({
  item,
  onSelect,
}) => {
***REMOVED***const [isHovered, setIsHovered] = React.useState(false);
***REMOVED***const [edit, setEdit] = useState(false);
***REMOVED***const [editTitle, setEditTitle] = useState("");
***REMOVED***const [hideDeleteDialog, { toggle: toggleDeleteDialog }] = useBoolean(true);
***REMOVED***const [errorDelete, setErrorDelete] = useState(false);
***REMOVED***const [renameLoading, setRenameLoading] = useState(false);
***REMOVED***const [errorRename, setErrorRename] = useState<string | undefined>(undefined);
***REMOVED***const [textFieldFocused, setTextFieldFocused] = useState(false);
***REMOVED***const textFieldRef = useRef<ITextField | null>(null);
***REMOVED***
***REMOVED***const appStateContext = React.useContext(AppStateContext)
***REMOVED***const isSelected = item?.id === appStateContext?.state.currentChat?.id;
***REMOVED***const dialogContentProps = {
***REMOVED***type: DialogType.close,
***REMOVED***title: 'Are you sure you want to delete this item?',
***REMOVED***closeButtonAriaLabel: 'Close',
***REMOVED***subText: 'The history of this chat session will permanently removed.',
***REMOVED***;

***REMOVED***const modalProps = {
***REMOVED***titleAriaId: 'labelId',
***REMOVED***subtitleAriaId: 'subTextId',
***REMOVED***isBlocking: true,
***REMOVED***styles: { main: { maxWidth: 450 } },
***REMOVED***

***REMOVED***if (!item) {
***REMOVED***return null;
***REMOVED***

***REMOVED***useEffect(() => {
***REMOVED***if (textFieldFocused && textFieldRef.current) {
***REMOVED******REMOVED***textFieldRef.current.focus();
***REMOVED******REMOVED***setTextFieldFocused(false);
***REMOVED***
***REMOVED***, [textFieldFocused]);

***REMOVED***useEffect(() => {
***REMOVED***if (appStateContext?.state.currentChat?.id !== item?.id) {
***REMOVED******REMOVED***setEdit(false);
***REMOVED******REMOVED***setEditTitle('')
***REMOVED***
***REMOVED***, [appStateContext?.state.currentChat?.id, item?.id]);

***REMOVED***const onDelete = async () => {
***REMOVED***let response = await historyDelete(item.id)
***REMOVED***if(!response.ok){
***REMOVED******REMOVED***setErrorDelete(true)
***REMOVED******REMOVED***setTimeout(() => {
***REMOVED******REMOVED***setErrorDelete(false);
***REMOVED***, 5000);
***REMOVED***else{
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'DELETE_CHAT_ENTRY', payload: item.id })
***REMOVED***
***REMOVED***toggleDeleteDialog();
***REMOVED***;

***REMOVED***const onEdit = () => {
***REMOVED***setEdit(true)
***REMOVED***setTextFieldFocused(true)
***REMOVED***setEditTitle(item?.title)
***REMOVED***;

***REMOVED***const handleSelectItem = () => {
***REMOVED***onSelect(item)
***REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CURRENT_CHAT', payload: item } )
***REMOVED***

***REMOVED***const truncatedTitle = (item?.title?.length > 28) ? `${item.title.substring(0, 28)} ...` : item.title;

***REMOVED***const handleSaveEdit = async (e: any) => {
***REMOVED***e.preventDefault();
***REMOVED***if(errorRename || renameLoading){
***REMOVED******REMOVED***return;
***REMOVED***
***REMOVED***if(editTitle == item.title){
***REMOVED******REMOVED***setErrorRename("Error: Enter a new title to proceed.")
***REMOVED******REMOVED***setTimeout(() => {
***REMOVED******REMOVED***setErrorRename(undefined);
***REMOVED******REMOVED***setTextFieldFocused(true);
***REMOVED******REMOVED***if (textFieldRef.current) {
***REMOVED******REMOVED******REMOVED***textFieldRef.current.focus();
***REMOVED******REMOVED***
***REMOVED***, 5000);
***REMOVED******REMOVED***return
***REMOVED***
***REMOVED***setRenameLoading(true)
***REMOVED***let response = await historyRename(item.id, editTitle);
***REMOVED***if(!response.ok){
***REMOVED******REMOVED***setErrorRename("Error: could not rename item")
***REMOVED******REMOVED***setTimeout(() => {
***REMOVED******REMOVED***setTextFieldFocused(true);
***REMOVED******REMOVED***setErrorRename(undefined);
***REMOVED******REMOVED***if (textFieldRef.current) {
***REMOVED******REMOVED******REMOVED***textFieldRef.current.focus();
***REMOVED******REMOVED***
***REMOVED***, 5000);
***REMOVED***else{
***REMOVED******REMOVED***setRenameLoading(false)
***REMOVED******REMOVED***setEdit(false)
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'UPDATE_CHAT_TITLE', payload: { ...item, title: editTitle } as Conversation })
***REMOVED******REMOVED***setEditTitle("");
***REMOVED***
***REMOVED***

***REMOVED***const chatHistoryTitleOnChange = (e: any) => {
***REMOVED***setEditTitle(e.target.value);
***REMOVED***;

***REMOVED***const cancelEditTitle = () => {
***REMOVED***setEdit(false)
***REMOVED***setEditTitle("");
***REMOVED***

***REMOVED***const handleKeyPressEdit = (e: any) => {
***REMOVED***if(e.key === "Enter"){
***REMOVED******REMOVED***return handleSaveEdit(e)
***REMOVED***
***REMOVED***if(e.key === "Escape"){
***REMOVED******REMOVED***cancelEditTitle();
***REMOVED******REMOVED***return
***REMOVED***
***REMOVED***

***REMOVED***return (
***REMOVED***<Stack
***REMOVED******REMOVED***key={item.id}
***REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED***aria-label='chat history item'
***REMOVED******REMOVED***className={styles.itemCell}
***REMOVED******REMOVED***onClick={() => handleSelectItem()}
***REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? handleSelectItem() : null}
***REMOVED******REMOVED***verticalAlign='center'
***REMOVED******REMOVED***// horizontal
***REMOVED******REMOVED***onMouseEnter={() => setIsHovered(true)}
***REMOVED******REMOVED***onMouseLeave={() => setIsHovered(false)}
***REMOVED******REMOVED***styles={{
***REMOVED******REMOVED***root: {
***REMOVED******REMOVED******REMOVED***backgroundColor: isSelected ? '#e6e6e6' : 'transparent',
***REMOVED******REMOVED***
***REMOVED***}
***REMOVED***>
***REMOVED******REMOVED***{edit ? <>
***REMOVED******REMOVED***<Stack.Item 
***REMOVED******REMOVED******REMOVED***style={{ width: '100%' }}
***REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED***<form aria-label='edit title form' onSubmit={(e) => handleSaveEdit(e)} style={{padding: '5px 0px'}}>
***REMOVED******REMOVED******REMOVED***<Stack horizontal verticalAlign={'start'}>
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack.Item>
***REMOVED******REMOVED******REMOVED******REMOVED***<TextField
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***componentRef={textFieldRef}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***autoFocus={textFieldFocused}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***value={editTitle}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***placeholder={item.title}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onChange={chatHistoryTitleOnChange}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***onKeyDown={handleKeyPressEdit}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***// errorMessage={errorRename}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***disabled={errorRename ? true : false}
***REMOVED******REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED******REMOVED******REMOVED***{editTitle && (<Stack.Item>
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack aria-label='action button group' horizontal verticalAlign={'center'}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<IconButton role='button' disabled={errorRename !== undefined} onKeyDown={e => e.key === " " || e.key === 'Enter' ? handleSaveEdit(e) : null} onClick={(e) => handleSaveEdit(e)} aria-label='confirm new title' iconProps={{iconName: 'CheckMark'}} styles={{ root: { color: 'green', marginLeft: '5px' } }} />
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<IconButton role='button' disabled={errorRename !== undefined} onKeyDown={e => e.key === " " || e.key === 'Enter' ? cancelEditTitle() : null} onClick={() => cancelEditTitle()} aria-label='cancel edit title' iconProps={{iconName: 'Cancel'}} styles={{ root: { color: 'red', marginLeft: '5px' } }} />
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack.Item>)}
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***{errorRename && (
***REMOVED******REMOVED******REMOVED******REMOVED***<Text role='alert' aria-label={errorRename} style={{fontSize: 12, fontWeight: 400, color: 'rgb(164,38,44)'}}>{errorRename}</Text>
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***</form>
***REMOVED******REMOVED***</Stack.Item>
***REMOVED******REMOVED***</> : <>
***REMOVED******REMOVED***<Stack horizontal verticalAlign={'center'} style={{ width: '100%' }}>
***REMOVED******REMOVED******REMOVED***<div className={styles.chatTitle}>{truncatedTitle}</div>
***REMOVED******REMOVED******REMOVED***{(isSelected || isHovered) && <Stack horizontal horizontalAlign='end'>
***REMOVED******REMOVED******REMOVED***<IconButton className={styles.itemButton} iconProps={{ iconName: 'Delete' }} title="Delete" onClick={toggleDeleteDialog} onKeyDown={e => e.key === " " ? toggleDeleteDialog() : null}/>
***REMOVED******REMOVED******REMOVED***<IconButton className={styles.itemButton} iconProps={{ iconName: 'Edit' }} title="Edit" onClick={onEdit} onKeyDown={e => e.key === " " ? onEdit() : null}/>
***REMOVED******REMOVED******REMOVED***</Stack>}
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</>
***REMOVED***
***REMOVED******REMOVED***{errorDelete && (
***REMOVED******REMOVED***<Text
***REMOVED******REMOVED******REMOVED***styles={{
***REMOVED******REMOVED******REMOVED***root: { color: 'red', marginTop: 5, fontSize: 14 }
***REMOVED******REMOVED***}
***REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED***Error: could not delete item
***REMOVED******REMOVED***</Text>
***REMOVED******REMOVED***)}
***REMOVED******REMOVED***<Dialog
***REMOVED******REMOVED***hidden={hideDeleteDialog}
***REMOVED******REMOVED***onDismiss={toggleDeleteDialog}
***REMOVED******REMOVED***dialogContentProps={dialogContentProps}
***REMOVED******REMOVED***modalProps={modalProps}
***REMOVED******REMOVED***>
***REMOVED******REMOVED***<DialogFooter>
***REMOVED******REMOVED***<PrimaryButton onClick={onDelete} text="Delete" />
***REMOVED******REMOVED***<DefaultButton onClick={toggleDeleteDialog} text="Cancel" />
***REMOVED******REMOVED***</DialogFooter>
***REMOVED******REMOVED***</Dialog>
***REMOVED***</Stack>
***REMOVED***);
};

export const ChatHistoryListItemGroups: React.FC<ChatHistoryListItemGroupsProps> = ({ groupedChatHistory }) => {
***REMOVED***const appStateContext = useContext(AppStateContext);
***REMOVED***const observerTarget = useRef(null);
***REMOVED***const [ , setSelectedItem] = React.useState<Conversation | null>(null);
***REMOVED***const [offset, setOffset] = useState<number>(25);
***REMOVED***const [observerCounter, setObserverCounter] = useState(0);
***REMOVED***const [showSpinner, setShowSpinner] = useState(false);
***REMOVED***const firstRender = useRef(true);

  const handleSelectHistory = (item?: Conversation) => {
***REMOVED***if(item){
***REMOVED***setSelectedItem(item)
***REMOVED***
  }

  const onRenderCell = (item?: Conversation) => {
***REMOVED***return (
***REMOVED***  <ChatHistoryListItemCell item={item} onSelect={() => handleSelectHistory(item)} />
***REMOVED***);
  };

***REMOVED***useEffect(() => {
***REMOVED***if (firstRender.current) {
***REMOVED******REMOVED***firstRender.current = false;
***REMOVED******REMOVED***return;
***REMOVED***
***REMOVED***handleFetchHistory();
***REMOVED***setOffset((offset) => offset += 25);
***REMOVED***, [observerCounter]);

***REMOVED***const handleFetchHistory = async () => {
***REMOVED***const currentChatHistory = appStateContext?.state.chatHistory;
***REMOVED***setShowSpinner(true);

***REMOVED***await historyList(offset).then((response) => {
***REMOVED******REMOVED***const concatenatedChatHistory = currentChatHistory && response && currentChatHistory.concat(...response)
***REMOVED******REMOVED***if (response) {
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'FETCH_CHAT_HISTORY', payload: concatenatedChatHistory || response });
***REMOVED******REMOVED***
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'FETCH_CHAT_HISTORY', payload: null });
***REMOVED***
***REMOVED******REMOVED***setShowSpinner(false);
***REMOVED******REMOVED***return response
***REMOVED***)
***REMOVED***

***REMOVED***useEffect(() => {
***REMOVED***const observer = new IntersectionObserver(
***REMOVED******REMOVED***entries => {
***REMOVED******REMOVED***if (entries[0].isIntersecting) 
***REMOVED******REMOVED******REMOVED***setObserverCounter((observerCounter) => observerCounter += 1);
***REMOVED***,
***REMOVED******REMOVED***{ threshold: 1 }
***REMOVED***);

***REMOVED***if (observerTarget.current) observer.observe(observerTarget.current);

***REMOVED***return () => {
***REMOVED******REMOVED***if (observerTarget.current) observer.unobserve(observerTarget.current);
***REMOVED***;
***REMOVED***, [observerTarget]);

  return (
***REMOVED***<div className={styles.listContainer} data-is-scrollable>
***REMOVED***  {groupedChatHistory.map((group) => (
***REMOVED***group.entries.length > 0 && <Stack horizontalAlign="start" verticalAlign="center" key={group.month} className={styles.chatGroup} aria-label={`chat history group: ${group.month}`}>
***REMOVED***  <Stack aria-label={group.month} className={styles.chatMonth}>{formatMonth(group.month)}</Stack>
***REMOVED***  <List aria-label={`chat history list`} items={group.entries} onRenderCell={onRenderCell} className={styles.chatList}/>
***REMOVED***  <div ref={observerTarget} />
***REMOVED***  <Separator styles={{
***REMOVED******REMOVED***root: {
***REMOVED******REMOVED***width: '100%',
***REMOVED******REMOVED***position: 'relative',
***REMOVED******REMOVED***'::before': {
***REMOVED******REMOVED***  backgroundColor: '#d6d6d6',
***REMOVED******REMOVED***,
  ***REMOVED***,
  ***REMOVED***}/>
***REMOVED***</Stack>
***REMOVED***  ))}
***REMOVED***  {showSpinner && <div className={styles.spinnerContainer}><Spinner size={SpinnerSize.small} aria-label="loading more chat history" className={styles.spinner}/></div>}
***REMOVED***</div>
  );
};
