import { Text } from "@fluentui/react";
import { Delete24Regular } from "@fluentui/react-icons";

import styles from "./ClearChatButton.module.css";

interface Props {
***REMOVED***className?: string;
***REMOVED***onClick: () => void;
***REMOVED***disabled?: boolean;
}

export const ClearChatButton = ({ className, disabled, onClick }: Props) => {
***REMOVED***return (
***REMOVED***<div className={`${styles.container} ${className ?? ""} ${disabled && styles.disabled}`} onClick={onClick}>
***REMOVED******REMOVED***<Delete24Regular />
***REMOVED******REMOVED***<Text>{"Clear chat"}</Text>
***REMOVED***</div>
***REMOVED***);
};
