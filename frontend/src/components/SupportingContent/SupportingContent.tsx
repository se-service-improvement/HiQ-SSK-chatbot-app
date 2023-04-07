import { DocumentResult } from "../../api";
import styles from "./SupportingContent.module.css";

interface Props {
***REMOVED***supportingContent: DocumentResult;
}

export const SupportingContent = ({ supportingContent }: Props) => {
***REMOVED***return (
***REMOVED***<ul className={styles.supportingContentNavList}>
***REMOVED******REMOVED***<li className={styles.supportingContentItem}>
***REMOVED******REMOVED***<h4 className={styles.supportingContentItemHeader}>{supportingContent.title}</h4>
***REMOVED******REMOVED***<p className={styles.supportingContentItemText}>{supportingContent.content}</p>
***REMOVED******REMOVED***</li>
***REMOVED***</ul>
***REMOVED***);
};
