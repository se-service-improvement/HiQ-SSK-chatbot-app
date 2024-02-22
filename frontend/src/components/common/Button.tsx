import { CommandBarButton, DefaultButton, IButtonProps } from "@fluentui/react";

import styles from './Button.module.css';

interface ButtonProps extends IButtonProps {
  onClick: () => void;
  text: string | undefined;
}

export const ShareButton: React.FC<ButtonProps> = ({ onClick, text }) => {

  return (
***REMOVED***<CommandBarButton
***REMOVED***  className={styles.shareButtonRoot}
***REMOVED***  iconProps={{ iconName: 'Share' }}
***REMOVED***  onClick={onClick}
***REMOVED***  text={text}
***REMOVED***/>
  )
}

export const HistoryButton: React.FC<ButtonProps> = ({ onClick, text }) => {
  return (
***REMOVED***<DefaultButton
***REMOVED***  className={styles.historyButtonRoot}
***REMOVED***  text={text}
***REMOVED***  iconProps={{ iconName: 'History' }}
***REMOVED***  onClick={onClick}
***REMOVED***/>
  )
}