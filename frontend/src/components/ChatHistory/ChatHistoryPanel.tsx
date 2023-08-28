import { CommandBarButton, ContextualMenu, DefaultButton, Dialog, DialogFooter, DialogType, ICommandBarStyles, IContextualMenuItem, IStackStyles, PrimaryButton, Spinner, SpinnerSize, Stack, StackItem, Text } from "@fluentui/react";
import { useBoolean } from '@fluentui/react-hooks';

import styles from "./ChatHistoryPanel.module.css"
import { useContext } from "react";
import { AppStateContext } from "../../state/AppProvider";
import React from "react";
import ChatHistoryList from "./ChatHistoryList";
import { ChatHistoryLoadingState, historyDeleteAll } from "../../api";

interface ChatHistoryPanelProps {

}

export enum ChatHistoryPanelTabs {
***REMOVED***History = "History"
}

const commandBarStyle: ICommandBarStyles = {
***REMOVED***root: {
***REMOVED***padding: '0',
***REMOVED***display: 'flex',
***REMOVED***justifyContent: 'center',
***REMOVED***backgroundColor: 'transparent'
***REMOVED***,
};

const commandBarButtonStyle: Partial<IStackStyles> = { root: { height: '50px' } };

export function ChatHistoryPanel(props: ChatHistoryPanelProps) {
***REMOVED***const appStateContext = useContext(AppStateContext)
***REMOVED***const [showContextualMenu, setShowContextualMenu] = React.useState(false);
***REMOVED***const [hideClearAllDialog, { toggle: toggleClearAllDialog }] = useBoolean(true);
***REMOVED***const [clearing, setClearing] = React.useState(false)
***REMOVED***const [clearingError, setClearingError] = React.useState(false)

***REMOVED***const clearAllDialogContentProps = {
***REMOVED***type: DialogType.close,
***REMOVED***title: !clearingError? 'Are you sure you want to clear all chat history?' : 'Error deleting all of chat history',
***REMOVED***closeButtonAriaLabel: 'Close',
***REMOVED***subText: !clearingError ? 'All chat history will be permanently removed.' : 'Please try again. If the problem persists, please contact the site administrator.',
***REMOVED***;
***REMOVED***
***REMOVED***const modalProps = {
***REMOVED***titleAriaId: 'labelId',
***REMOVED***subtitleAriaId: 'subTextId',
***REMOVED***isBlocking: true,
***REMOVED***styles: { main: { maxWidth: 450 } },
***REMOVED***

***REMOVED***const menuItems: IContextualMenuItem[] = [
***REMOVED***{ key: 'clearAll', text: 'Clear all chat history', iconProps: { iconName: 'Delete' }},
***REMOVED***];

***REMOVED***const handleHistoryClick = () => {
***REMOVED***appStateContext?.dispatch({ type: 'TOGGLE_CHAT_HISTORY' })
***REMOVED***;
***REMOVED***
***REMOVED***const onShowContextualMenu = React.useCallback((ev: React.MouseEvent<HTMLElement>) => {
***REMOVED***ev.preventDefault(); // don't navigate
***REMOVED***setShowContextualMenu(true);
***REMOVED***, []);

***REMOVED***const onHideContextualMenu = React.useCallback(() => setShowContextualMenu(false), []);

***REMOVED***const onClearAllChatHistory = async () => {
***REMOVED***setClearing(true)
***REMOVED***let response = await historyDeleteAll()
***REMOVED***if(!response.ok){
***REMOVED******REMOVED***setClearingError(true)
***REMOVED***else{
***REMOVED******REMOVED***appStateContext?.dispatch({ type: 'DELETE_CHAT_HISTORY' })
***REMOVED******REMOVED***toggleClearAllDialog();
***REMOVED***
***REMOVED***setClearing(false);
***REMOVED***

***REMOVED***const onHideClearAllDialog = () => {
***REMOVED***toggleClearAllDialog()
***REMOVED***setTimeout(() => {
***REMOVED******REMOVED***setClearingError(false)
***REMOVED***, 2000);
***REMOVED***

***REMOVED***React.useEffect(() => {}, [appStateContext?.state.chatHistory, clearingError]);

***REMOVED***return (
***REMOVED***<section className={styles.container} data-is-scrollable aria-label={"chat history panel"}>
***REMOVED******REMOVED***<Stack horizontal horizontalAlign='space-between' verticalAlign='center' wrap aria-label="chat history header">
***REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED******REMOVED***<Text role="heading" aria-level={2} style={{ alignSelf: "center", fontWeight: "600", fontSize: "18px", marginRight: "auto", paddingLeft: "20px" }}>Chat history</Text>
***REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED***<Stack verticalAlign="start">
***REMOVED******REMOVED******REMOVED***<Stack horizontal styles={commandBarButtonStyle}>
***REMOVED******REMOVED******REMOVED***<CommandBarButton
***REMOVED******REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'More' }}
***REMOVED******REMOVED******REMOVED******REMOVED***title={"Clear all chat history"}
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={onShowContextualMenu}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label={"clear all chat history"}
***REMOVED******REMOVED******REMOVED******REMOVED***styles={commandBarStyle}
***REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED******REMOVED***id="moreButton"
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***<ContextualMenu
***REMOVED******REMOVED******REMOVED******REMOVED***items={menuItems}
***REMOVED******REMOVED******REMOVED******REMOVED***hidden={!showContextualMenu}
***REMOVED******REMOVED******REMOVED******REMOVED***target={"#moreButton"}
***REMOVED******REMOVED******REMOVED******REMOVED***onItemClick={toggleClearAllDialog}
***REMOVED******REMOVED******REMOVED******REMOVED***onDismiss={onHideContextualMenu}
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***<CommandBarButton
***REMOVED******REMOVED******REMOVED******REMOVED***iconProps={{ iconName: 'Cancel' }}
***REMOVED******REMOVED******REMOVED******REMOVED***title={"Hide"}
***REMOVED******REMOVED******REMOVED******REMOVED***onClick={handleHistoryClick}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-label={"hide button"}
***REMOVED******REMOVED******REMOVED******REMOVED***styles={commandBarStyle}
***REMOVED******REMOVED******REMOVED******REMOVED***role="button"
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***<Stack aria-label="chat history panel content"
***REMOVED******REMOVED***styles={{
***REMOVED******REMOVED******REMOVED***root: {
***REMOVED******REMOVED******REMOVED***display: "flex",
***REMOVED******REMOVED******REMOVED***flexGrow: 1,
***REMOVED******REMOVED******REMOVED***flexDirection: "column",
***REMOVED******REMOVED******REMOVED***paddingTop: '2.5px',
***REMOVED******REMOVED******REMOVED***maxWidth: "100%"
***REMOVED******REMOVED***,
***REMOVED******REMOVED***}
***REMOVED******REMOVED***style={{
***REMOVED******REMOVED******REMOVED***display: "flex",
***REMOVED******REMOVED******REMOVED***flexGrow: 1,
***REMOVED******REMOVED******REMOVED***flexDirection: "column",
***REMOVED******REMOVED******REMOVED***flexWrap: "wrap",
***REMOVED******REMOVED******REMOVED***padding: "1px"
***REMOVED******REMOVED***}>
***REMOVED******REMOVED***<Stack className={styles.chatHistoryListContainer}>
***REMOVED******REMOVED******REMOVED***{(appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Success && appStateContext?.state.isCosmosDBAvailable.cosmosDB) && <ChatHistoryList/>}
***REMOVED******REMOVED******REMOVED***{(appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Fail && appStateContext?.state.isCosmosDBAvailable) && <>
***REMOVED******REMOVED******REMOVED***<Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack horizontalAlign='center' verticalAlign='center' style={{ width: "100%", marginTop: 10 }}>
***REMOVED******REMOVED******REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 16 }}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{appStateContext?.state.isCosmosDBAvailable?.status && <span>{appStateContext?.state.isCosmosDBAvailable?.status}</span>}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***{!appStateContext?.state.isCosmosDBAvailable?.status && <span>Error loading chat history</span>}
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</Text>
***REMOVED******REMOVED******REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 14 }}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span>Chat history can't be saved at this time</span>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</Text>
***REMOVED******REMOVED******REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</>}
***REMOVED******REMOVED******REMOVED***{appStateContext?.state.chatHistoryLoadingState === ChatHistoryLoadingState.Loading && <>
***REMOVED******REMOVED******REMOVED***<Stack>
***REMOVED******REMOVED******REMOVED******REMOVED***<Stack horizontal horizontalAlign='center' verticalAlign='center' style={{ width: "100%", marginTop: 10 }}>
***REMOVED******REMOVED******REMOVED******REMOVED***<StackItem style={{ justifyContent: 'center', alignItems: 'center' }}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Spinner style={{ alignSelf: "flex-start", height: "100%", marginRight: "5px" }} size={SpinnerSize.medium} />
***REMOVED******REMOVED******REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED***<StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<Text style={{ alignSelf: 'center', fontWeight: '400', fontSize: 14 }}>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***<span style={{ whiteSpace: 'pre-wrap' }}>Loading chat history</span>
***REMOVED******REMOVED******REMOVED******REMOVED******REMOVED***</Text>
***REMOVED******REMOVED******REMOVED******REMOVED***</StackItem>
***REMOVED******REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED******REMOVED***</>}
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***<Dialog
***REMOVED******REMOVED***hidden={hideClearAllDialog}
***REMOVED******REMOVED***onDismiss={clearing ? ()=>{} : onHideClearAllDialog}
***REMOVED******REMOVED***dialogContentProps={clearAllDialogContentProps}
***REMOVED******REMOVED***modalProps={modalProps}
***REMOVED******REMOVED***>
***REMOVED******REMOVED***<DialogFooter>
***REMOVED******REMOVED***{!clearingError && <PrimaryButton onClick={onClearAllChatHistory} disabled={clearing} text="Clear All" />}
***REMOVED******REMOVED***<DefaultButton onClick={onHideClearAllDialog} disabled={clearing} text={!clearingError ? "Cancel" : "Close"} />
***REMOVED******REMOVED***</DialogFooter>
***REMOVED******REMOVED***</Dialog>
***REMOVED***</section>
***REMOVED***);
}