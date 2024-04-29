import { useContext } from 'react'
import React from 'react'
import {
  CommandBarButton,
  ContextualMenu,
  DefaultButton,
  Dialog,
  DialogFooter,
  DialogType,
  ICommandBarStyles,
  IContextualMenuItem,
  IStackStyles,
  PrimaryButton,
  Spinner,
  SpinnerSize,
  Stack,
  StackItem,
  Text
} from '@fluentui/react'
import { useBoolean } from '@fluentui/react-hooks'

import { ChatHistoryLoadingState, historyDeleteAll } from '../../api'
import { AppStateContext } from '../../state/AppProvider'

import ChatHistoryList from './ChatHistoryList'

import styles from './ChatHistoryPanel.module.css'

interface ChatHistoryPanelProps {}

export enum ChatHistoryPanelTabs {
  History = 'History'
}

const commandBarStyle: ICommandBarStyles = {
  root: {
***REMOVED***padding: '0',
***REMOVED***display: 'flex',
***REMOVED***justifyContent: 'center',
***REMOVED***backgroundColor: 'transparent'
  }
}

const commandBarButtonStyle: Partial<IStackStyles> = { root: { height: '50px' } }

export function ChatHistoryPanel(_props: ChatHistoryPanelProps) {
  const appStateContext = useContext(AppStateContext)
  const [showContextualMenu, setShowContextualMenu] = React.useState(false)
  const [hideClearAllDialog, { toggle: toggleClearAllDialog }] = useBoolean(true)
  const [clearing, setClearing] = React.useState(false)
  const [clearingError, setClearingError] = React.useState(false)

  const clearAllDialogContentProps = {
***REMOVED***type: DialogType.close,
***REMOVED***title: !clearingError ? 'Are you sure you want to clear all chat history?' : 'Error deleting all of chat history',
***REMOVED***closeButtonAriaLabel: 'Close',
***REMOVED***subText: !clearingError
***REMOVED***  ? 'All chat history will be permanently removed.'
***REMOVED***  : 'Please try again. If the problem persists, please contact the site administrator.'
  }

  const modalProps = {
***REMOVED***titleAriaId: 'labelId',
***REMOVED***subtitleAriaId: 'subTextId',
***REMOVED***isBlocking: true,
***REMOVED***styles: { main: { maxWidth: 450 } }
  }

  const menuItems: IContextualMenuItem[] = [
***REMOVED***{ key: 'clearAll', text: 'Clear all chat history', iconProps: { iconName: 'Delete' } }
  ]

  const handleHistoryClick = () => {
***REMOVED***appStateContext?.dispatch({ type: 'TOGGLE_CHAT_HISTORY' })
  }

  const onShowContextualMenu = React.useCallback((ev: React.MouseEvent<HTMLElement>) => {
***REMOVED***ev.preventDefault() // don't navigate
***REMOVED***setShowContextualMenu(true)
  }, [])

  const onHideContextualMenu = React.useCallback(() => setShowContextualMenu(false), [])

  const onClearAllChatHistory = async () => {
***REMOVED***setClearing(true)
***REMOVED***const response = await historyDeleteAll()
***REMOVED***if (!response.ok) {
***REMOVED***  setClearingError(true)
***REMOVED***
***REMOVED***  appStateContext?.dispatch({ type: 'DELETE_CHAT_HISTORY' })
***REMOVED***  toggleClearAllDialog()
***REMOVED***
***REMOVED***setClearing(false)
  }

  const onHideClearAllDialog = () => {
***REMOVED***toggleClearAllDialog()
***REMOVED***setTimeout(() => {
***REMOVED***  setClearingError(false)
***REMOVED***, 2000)
  }

  React.useEffect(() => {}, [appStateContext?.state.chatHistory, clearingError])

  return (
***REMOVED***<section className={styles.container} data-is-scrollable aria-label={'chat history panel'}>
***REMOVED***  <Stack horizontal horizontalAlign="space-between" verticalAlign="center" wrap aria-label="chat history header">
***REMOVED***<StackItem>
***REMOVED***  <Text
***REMOVED******REMOVED***role="heading"
***REMOVED******REMOVED***aria-level={2}
***REMOVED******REMOVED***style={{
***REMOVED******REMOVED***  alignSelf: 'center',
***REMOVED******REMOVED***  fontWeight: '600',
***REMOVED******REMOVED***  fontSize: '18px',
***REMOVED******REMOVED***  marginRight: 'auto',
***REMOVED******REMOVED***  paddingLeft: '20px'
***REMOVED***}>
***REMOVED******REMOVED***Chat history
***REMOVED***  </Text>
***REMOVED***</StackItem>
***REMOVED***<Stack verticalAlign="start">
***REMOVED***  <Stack horizontal styles={commandBarButtonStyle}>
***REMOVED******REMOVED***<CommandBarButton
***REMOVED******REMOVED***  iconProps={{ iconName: 'More' }}
***REMOVED******REMOVED***  title={'Clear all chat history'}
***REMOVED******REMOVED***  onClick={onShowContextualMenu}
***REMOVED******REMOVED***  aria-label={'clear all chat history'}
***REMOVED******REMOVED***  styles={commandBarStyle}
***REMOVED******REMOVED***  role="button"
***REMOVED******REMOVED***  id="moreButton"
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***<ContextualMenu
***REMOVED******REMOVED***  items={menuItems}
***REMOVED******REMOVED***  hidden={!showContextualMenu}
***REMOVED******REMOVED***  target={'#moreButton'}
***REMOVED******REMOVED***  onItemClick={toggleClearAllDialog}
***REMOVED******REMOVED***  onDismiss={onHideContextualMenu}
***REMOVED******REMOVED***/>
***REMOVED******REMOVED***<CommandBarButton
***REMOVED******REMOVED***  iconProps={{ iconName: 'Cancel' }}
***REMOVED******REMOVED***  title={'Hide'}
***REMOVED******REMOVED***  onClick={handleHistoryClick}
***REMOVED******REMOVED***  aria-label={'hide button'}
***REMOVED******REMOVED***  styles={commandBarStyle}
***REMOVED******REMOVED***  role="button"
***REMOVED******REMOVED***/>
***REMOVED***  </Stack>
***REMOVED***</Stack>
***REMOVED***  </Stack>
***REMOVED***  <Stack
***REMOVED***aria-label="chat history panel content"
***REMOVED***styles={{
***REMOVED***  root: {
***REMOVED******REMOVED***display: 'flex',
***REMOVED******REMOVED***flexGrow: 1,
***REMOVED******REMOVED***flexDirection: 'column',
***REMOVED******REMOVED***paddingTop: '2.5px',
***REMOVED******REMOVED***maxWidth: '100%'
  ***REMOVED***
***REMOVED***}
***REMOVED***style={{
***REMOVED***  display: 'flex',
***REMOVED***  flexGrow: 1,
***REMOVED***  flexDirection: 'column',
***REMOVED***  flexWrap: 'wrap',
***REMOVED***  padding: '1px'
***REMOVED***}>
***REMOVED***<Stack className={styles.chatHistoryListContainer}>
***REMOVED***  {appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Success &&
***REMOVED******REMOVED***appStateContext?.state.isCosmosDBAvailable.cosmosDB && <ChatHistoryList />}
***REMOVED***  {appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Fail &&
***REMOVED******REMOVED***appStateContext?.state.isCosmosDBAvailable && (
***REMOVED******REMOVED***  <>
***REMOVED******REMOVED***<Stack>
***REMOVED******REMOVED***  <Stack horizontalAlign="center" verticalAlign="center" style={{ width: '100%', marginTop: 10 }}>
***REMOVED******REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED******REMOVED***  <Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 16 }}>
***REMOVED******REMOVED******REMOVED***{appStateContext?.state.isCosmosDBAvailable?.status && (
***REMOVED******REMOVED******REMOVED***  <span>{appStateContext?.state.isCosmosDBAvailable?.status}</span>
***REMOVED******REMOVED******REMOVED***)}
***REMOVED******REMOVED******REMOVED***{!appStateContext?.state.isCosmosDBAvailable?.status && <span>Error loading chat history</span>}
***REMOVED******REMOVED******REMOVED***  </Text>
***REMOVED******REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED******REMOVED***  <Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 14 }}>
***REMOVED******REMOVED******REMOVED***<span>Chat history can't be saved at this time</span>
***REMOVED******REMOVED******REMOVED***  </Text>
***REMOVED******REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  </>
***REMOVED******REMOVED***)}
***REMOVED***  {appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Loading && (
***REMOVED******REMOVED***<>
***REMOVED******REMOVED***  <Stack>
***REMOVED******REMOVED***<Stack
***REMOVED******REMOVED***  horizontal
***REMOVED******REMOVED***  horizontalAlign="center"
***REMOVED******REMOVED***  verticalAlign="center"
***REMOVED******REMOVED***  style={{ width: '100%', marginTop: 10 }}>
***REMOVED******REMOVED***  <StackItem style={{ justifyContent: 'center', alignItems: 'center' }}>
***REMOVED******REMOVED******REMOVED***<Spinner
***REMOVED******REMOVED******REMOVED***  style={{ alignSelf: 'flex-start', height: '100%', marginRight: '5px' }}
***REMOVED******REMOVED******REMOVED***  size={SpinnerSize.medium}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED***  </StackItem>
***REMOVED******REMOVED***  <StackItem>
***REMOVED******REMOVED******REMOVED***<Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 14 }}>
***REMOVED******REMOVED******REMOVED***  <span style={{ whiteSpace: 'pre-wrap' }}>Loading chat history</span>
***REMOVED******REMOVED******REMOVED***</Text>
***REMOVED******REMOVED***  </StackItem>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***  </Stack>
***REMOVED******REMOVED***</>
***REMOVED***  )}
***REMOVED***</Stack>
***REMOVED***  </Stack>
***REMOVED***  <Dialog
***REMOVED***hidden={hideClearAllDialog}
***REMOVED***onDismiss={clearing ? () => {} : onHideClearAllDialog}
***REMOVED***dialogContentProps={clearAllDialogContentProps}
***REMOVED***modalProps={modalProps}>
***REMOVED***<DialogFooter>
***REMOVED***  {!clearingError && <PrimaryButton onClick={onClearAllChatHistory} disabled={clearing} text="Clear All" />}
***REMOVED***  <DefaultButton
***REMOVED******REMOVED***onClick={onHideClearAllDialog}
***REMOVED******REMOVED***disabled={clearing}
***REMOVED******REMOVED***text={!clearingError ? 'Cancel' : 'Close'}
***REMOVED***  />
***REMOVED***</DialogFooter>
***REMOVED***  </Dialog>
***REMOVED***</section>
  )
}
