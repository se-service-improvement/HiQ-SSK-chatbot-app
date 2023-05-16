import { Outlet, Link } from "react-router-dom";
import styles from "./Layout.module.css";
import AzureOpenAILogo from "../../assets/AzureOpenAILogo.svg";
import { CopyRegular, ShareRegular } from "@fluentui/react-icons";
import { Dialog, Stack, TextField } from "@fluentui/react";
import { useEffect, useState } from "react";

const Layout = () => {
***REMOVED***const [isSharePanelOpen, setIsSharePanelOpen] = useState<boolean>(false);
***REMOVED***const [copyClicked, setCopyClicked] = useState<boolean>(false);
***REMOVED***const [copyText, setCopyText] = useState<string>("Copy URL");

***REMOVED***const handleShareClick = () => {
***REMOVED***setIsSharePanelOpen(true);
***REMOVED***;

***REMOVED***const handleSharePanelDismiss = () => {
***REMOVED***setIsSharePanelOpen(false);
***REMOVED***setCopyClicked(false);
***REMOVED***setCopyText("Copy URL");
***REMOVED***;

***REMOVED***const handleCopyClick = () => {
***REMOVED***navigator.clipboard.writeText(window.location.href);
***REMOVED***setCopyClicked(true);
***REMOVED***;

***REMOVED***useEffect(() => {
***REMOVED***if (copyClicked) {
***REMOVED******REMOVED***setCopyText("Copied URL");
***REMOVED***
***REMOVED***, [copyClicked]);

***REMOVED***return (
***REMOVED***<div className={styles.layout}>
***REMOVED******REMOVED***<header className={styles.header} role={"banner"}>
***REMOVED******REMOVED***<div className={styles.headerContainer}>
***REMOVED******REMOVED******REMOVED***<Stack horizontal verticalAlign="center">
***REMOVED******REMOVED******REMOVED***<img
***REMOVED******REMOVED******REMOVED******REMOVED***src={AzureOpenAILogo}
***REMOVED******REMOVED******REMOVED******REMOVED***className={styles.headerIcon}
***REMOVED******REMOVED******REMOVED******REMOVED***aria-hidden="true"
***REMOVED******REMOVED******REMOVED***/>
***REMOVED******REMOVED******REMOVED***<Link to="/" className={styles.headerTitleContainer}>
***REMOVED******REMOVED******REMOVED******REMOVED***<h3 className={styles.headerTitle}>Azure OpenAI</h3>
***REMOVED******REMOVED******REMOVED***</Link>
***REMOVED******REMOVED******REMOVED***<div className={styles.shareButtonContainer} role="button" tabIndex={0} aria-label="Share" onClick={handleShareClick} onKeyDown={e => e.key === "Enter" || e.key === " " ? handleShareClick() : null}>
***REMOVED******REMOVED******REMOVED******REMOVED***<ShareRegular className={styles.shareButton} />
***REMOVED******REMOVED******REMOVED******REMOVED***<span className={styles.shareButtonText}>Share</span>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***</header>
***REMOVED******REMOVED***<Outlet />
***REMOVED******REMOVED***<Dialog 
***REMOVED******REMOVED***onDismiss={handleSharePanelDismiss}
***REMOVED******REMOVED***hidden={!isSharePanelOpen}
***REMOVED******REMOVED***styles={{
***REMOVED******REMOVED******REMOVED***
***REMOVED******REMOVED******REMOVED***main: [{
***REMOVED******REMOVED******REMOVED***selectors: {
***REMOVED******REMOVED******REMOVED***  ['@media (min-width: 480px)']: {
***REMOVED******REMOVED******REMOVED******REMOVED***maxWidth: '600px',
***REMOVED******REMOVED******REMOVED******REMOVED***background: "#FFFFFF",
***REMOVED******REMOVED******REMOVED******REMOVED***boxShadow: "0px 14px 28.8px rgba(0, 0, 0, 0.24), 0px 0px 8px rgba(0, 0, 0, 0.2)",
***REMOVED******REMOVED******REMOVED******REMOVED***borderRadius: "8px",
***REMOVED******REMOVED******REMOVED******REMOVED***maxHeight: '200px',
***REMOVED******REMOVED******REMOVED******REMOVED***minHeight: '100px',
***REMOVED******REMOVED***  ***REMOVED***
***REMOVED******REMOVED******REMOVED***
***REMOVED***  ***REMOVED***]
***REMOVED******REMOVED***}
***REMOVED******REMOVED***dialogContentProps={{
***REMOVED******REMOVED******REMOVED***title: "Share the web app",
***REMOVED******REMOVED******REMOVED***showCloseButton: true
***REMOVED******REMOVED***}
***REMOVED******REMOVED***>
***REMOVED******REMOVED***<Stack horizontal verticalAlign="center" style={{gap: "8px"}}>
***REMOVED******REMOVED******REMOVED***<TextField className={styles.urlTextBox} defaultValue={window.location.href} readOnly/>
***REMOVED******REMOVED******REMOVED***<div 
***REMOVED******REMOVED******REMOVED***className={styles.copyButtonContainer} 
***REMOVED******REMOVED******REMOVED***role="button" 
***REMOVED******REMOVED******REMOVED***tabIndex={0} 
***REMOVED******REMOVED******REMOVED***aria-label="Copy" 
***REMOVED******REMOVED******REMOVED***onClick={handleCopyClick}
***REMOVED******REMOVED******REMOVED***onKeyDown={e => e.key === "Enter" || e.key === " " ? handleCopyClick() : null}
***REMOVED******REMOVED******REMOVED***>
***REMOVED******REMOVED******REMOVED***<CopyRegular className={styles.copyButton} />
***REMOVED******REMOVED******REMOVED***<span className={styles.copyButtonText}>{copyText}</span>
***REMOVED******REMOVED******REMOVED***</div>
***REMOVED******REMOVED***</Stack>
***REMOVED******REMOVED***</Dialog>
***REMOVED***</div>
***REMOVED***);
};

export default Layout;
