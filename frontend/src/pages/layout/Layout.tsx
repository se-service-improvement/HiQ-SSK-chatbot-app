import { useContext, useEffect, useState } from 'react'
import { Link, Outlet } from 'react-router-dom'
import { Dialog, Stack, TextField } from '@fluentui/react'
import { CopyRegular } from '@fluentui/react-icons'

import { CosmosDBStatus } from '../../api'
import Contoso from '../../assets/Contoso.svg'
import { HistoryButton, ShareButton } from '../../components/common/Button'
import { AppStateContext } from '../../state/AppProvider'

import styles from './Layout.module.css'

const Layout = () => {
  const [isSharePanelOpen, setIsSharePanelOpen] = useState<boolean>(false)
  const [copyClicked, setCopyClicked] = useState<boolean>(false)
  const [copyText, setCopyText] = useState<string>('Copy URL')
  const [shareLabel, setShareLabel] = useState<string | undefined>('Share')
  const [hideHistoryLabel, setHideHistoryLabel] = useState<string>('Hide chat history')
  const [showHistoryLabel, setShowHistoryLabel] = useState<string>('Show chat history')
  const [logo, setLogo] = useState('')
  const appStateContext = useContext(AppStateContext)
  const ui = appStateContext?.state.frontendSettings?.ui

  const handleShareClick = () => {
***REMOVED***setIsSharePanelOpen(true)
  }

  const handleSharePanelDismiss = () => {
***REMOVED***setIsSharePanelOpen(false)
***REMOVED***setCopyClicked(false)
***REMOVED***setCopyText('Copy URL')
  }

  const handleCopyClick = () => {
***REMOVED***navigator.clipboard.writeText(window.location.href)
***REMOVED***setCopyClicked(true)
  }

  const handleHistoryClick = () => {
***REMOVED***appStateContext?.dispatch({ type: 'TOGGLE_CHAT_HISTORY' })
  }

  useEffect(() => {
***REMOVED***if (!appStateContext?.state.isLoading) {
***REMOVED***  setLogo(ui?.logo || Contoso)
***REMOVED***
  }, [appStateContext?.state.isLoading])

  useEffect(() => {
***REMOVED***if (copyClicked) {
***REMOVED***  setCopyText('Copied URL')
***REMOVED***
  }, [copyClicked])

  useEffect(() => { }, [appStateContext?.state.isCosmosDBAvailable.status])

  useEffect(() => {
***REMOVED***const handleResize = () => {
***REMOVED***  if (window.innerWidth < 480) {
***REMOVED***setShareLabel(undefined)
***REMOVED***setHideHistoryLabel('Hide history')
***REMOVED***setShowHistoryLabel('Show history')
  ***REMOVED***
***REMOVED***setShareLabel('Share')
***REMOVED***setHideHistoryLabel('Hide chat history')
***REMOVED***setShowHistoryLabel('Show chat history')
  ***REMOVED***
***REMOVED***

***REMOVED***window.addEventListener('resize', handleResize)
***REMOVED***handleResize()

***REMOVED***return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
***REMOVED***<div className={styles.layout}>
***REMOVED***  <header className={styles.header} role={'banner'}>
***REMOVED***<Stack horizontal verticalAlign="center" horizontalAlign="space-between">
***REMOVED***  <Stack horizontal verticalAlign="center">
***REMOVED******REMOVED***<img src={logo} className={styles.headerIcon} aria-hidden="true" alt="" />
***REMOVED******REMOVED***<Link to="/" className={styles.headerTitleContainer}>
***REMOVED******REMOVED***  <h1 className={styles.headerTitle}>{ui?.title}</h1>
***REMOVED******REMOVED***</Link>
***REMOVED***  </Stack>
***REMOVED***  <Stack horizontal tokens={{ childrenGap: 4 }} className={styles.shareButtonContainer}>
***REMOVED******REMOVED***  {/* {(appStateContext?.state.isCosmosDBAvailable?.status !== CosmosDBStatus.NotConfigured) &&
***REMOVED******REMOVED***  <HistoryButton onClick={handleHistoryClick} text={appStateContext?.state?.isChatHistoryOpen ? hideHistoryLabel : showHistoryLabel} />
  ***REMOVED*** */}
***REMOVED******REMOVED***  {/* {ui?.show_share_button &&<ShareButton onClick={handleShareClick} text={shareLabel} />} */}
***REMOVED***  </Stack>
***REMOVED***</Stack>
***REMOVED***  </header>
***REMOVED***  <Outlet />
***REMOVED***  <Dialog
***REMOVED***onDismiss={handleSharePanelDismiss}
***REMOVED***hidden={!isSharePanelOpen}
***REMOVED***styles={{
***REMOVED***  main: [
***REMOVED******REMOVED***{
***REMOVED******REMOVED***  selectors: {
***REMOVED******REMOVED***['@media (min-width: 480px)']: {
***REMOVED******REMOVED***  maxWidth: '600px',
***REMOVED******REMOVED***  background: '#FFFFFF',
***REMOVED******REMOVED***  boxShadow: '0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)',
***REMOVED******REMOVED***  borderRadius: '8px',
***REMOVED******REMOVED***  maxHeight: '200px',
***REMOVED******REMOVED***  minHeight: '100px'
***REMOVED******REMOVED***
  ***REMOVED***
***REMOVED***
***REMOVED***  ]
***REMOVED***}
***REMOVED***dialogContentProps={{
***REMOVED***  title: 'Share the web app',
***REMOVED***  showCloseButton: true
***REMOVED***}>
***REMOVED***<Stack horizontal verticalAlign="center" style={{ gap: '8px' }}>
***REMOVED***  <TextField className={styles.urlTextBox} defaultValue={window.location.href} readOnly />
***REMOVED***  <div
***REMOVED******REMOVED***className={styles.copyButtonContainer}
***REMOVED******REMOVED***role="button"
***REMOVED******REMOVED***tabIndex={0}
***REMOVED******REMOVED***aria-label="Copy"
***REMOVED******REMOVED***onClick={handleCopyClick}
***REMOVED******REMOVED***onKeyDown={e => (e.key === 'Enter' || e.key === ' ' ? handleCopyClick() : null)}>
***REMOVED******REMOVED***<CopyRegular className={styles.copyButton} />
***REMOVED******REMOVED***<span className={styles.copyButtonText}>{copyText}</span>
***REMOVED***  </div>
***REMOVED***</Stack>
***REMOVED***  </Dialog>
***REMOVED***</div>
  )
}

export default Layout
