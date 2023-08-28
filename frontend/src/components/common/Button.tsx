import { CommandBarButton, DefaultButton, IButtonProps, IButtonStyles, ICommandBarStyles } from "@fluentui/react";

interface ShareButtonProps extends IButtonProps {
***REMOVED***onClick: () => void;
  }

export const ShareButton: React.FC<ShareButtonProps> = ({onClick}) => {
***REMOVED***const shareButtonStyles: ICommandBarStyles & IButtonStyles = {
***REMOVED***root: {
***REMOVED***  width: 86,
***REMOVED***  height: 32,
***REMOVED***  borderRadius: 4,
***REMOVED***  background: 'radial-gradient(109.81% 107.82% at 100.1% 90.19%, #0F6CBD 33.63%, #2D87C3 70.31%, #8DDDD8 100%)',
***REMOVED***//   position: 'absolute',
***REMOVED***//   right: 20,
***REMOVED***  padding: '5px 12px',
***REMOVED***  marginRight: '20px'
***REMOVED***,
***REMOVED***icon: {
***REMOVED***  color: '#FFFFFF',
***REMOVED***,
***REMOVED***rootHovered: {
***REMOVED***  background: 'linear-gradient(135deg, #0F6CBD 0%, #2D87C3 51.04%, #8DDDD8 100%)',
***REMOVED***,
***REMOVED***label: {
***REMOVED***  fontWeight: 600,
***REMOVED***  fontSize: 14,
***REMOVED***  lineHeight: '20px',
***REMOVED***  color: '#FFFFFF',
***REMOVED***,
  ***REMOVED***;

***REMOVED***  return (
***REMOVED***<CommandBarButton
***REMOVED******REMOVED***styles={shareButtonStyles}
***REMOVED******REMOVED***iconProps={{ iconName: 'Share' }}
***REMOVED******REMOVED***onClick={onClick}
***REMOVED******REMOVED***text="Share"
***REMOVED***/>
***REMOVED***  )
}

interface HistoryButtonProps extends IButtonProps {
***REMOVED***onClick: () => void;
***REMOVED***text: string;
  }

export const HistoryButton: React.FC<HistoryButtonProps> = ({onClick, text}) => {
***REMOVED***const historyButtonStyles: ICommandBarStyles & IButtonStyles = {
***REMOVED***root: {
***REMOVED******REMOVED***width: '180px',
***REMOVED******REMOVED***border: `1px solid #D1D1D1`,
  ***REMOVED***,
***REMOVED***  rootHovered: {
***REMOVED******REMOVED***border: `1px solid #D1D1D1`,
  ***REMOVED***,
***REMOVED***  rootPressed: {
***REMOVED******REMOVED***border: `1px solid #D1D1D1`,
  ***REMOVED***,
  ***REMOVED***;

***REMOVED***  return (
***REMOVED***<DefaultButton
***REMOVED******REMOVED***text={text}
***REMOVED******REMOVED***iconProps={{ iconName: 'History' }}
***REMOVED******REMOVED***onClick={onClick}
***REMOVED******REMOVED***styles={historyButtonStyles}
***REMOVED***/>
***REMOVED***  )
}