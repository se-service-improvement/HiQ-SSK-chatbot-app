import React from 'react'
import ReactDOM from 'react-dom/client'
import { HashRouter, Route, Routes } from 'react-router-dom'
import { initializeIcons } from '@fluentui/react'

import Chat from './pages/chat/Chat'
import FAQ from './pages/faq/FAQ'
import Review from './pages/review/Review'
import Layout from './pages/layout/Layout'
import NoPage from './pages/NoPage'
import { AppStateProvider } from './state/AppProvider'

import './index.css'

initializeIcons("https://res.cdn.office.net/files/fabric-cdn-prod_20241209.001/assets/icons/")

export default function App() {
  return (
***REMOVED***<AppStateProvider>
***REMOVED***  <HashRouter>
***REMOVED***<Routes>
***REMOVED***  <Route path="/" element={<Layout />}>
***REMOVED******REMOVED***<Route index element={<Chat />} />
***REMOVED******REMOVED***<Route path="faq/:faq_id" element={<FAQ />} />
***REMOVED******REMOVED***{/* <Route path=":conversation_id" element={<Review />} /> */}
***REMOVED******REMOVED***<Route path="*" element={<NoPage />} />
***REMOVED***  </Route>
***REMOVED***</Routes>
***REMOVED***  </HashRouter>
***REMOVED***</AppStateProvider>
  )
}

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
***REMOVED***<App />
  </React.StrictMode>
)

const stylesheetLink: HTMLLinkElement = document.createElement('link');
stylesheetLink.rel = 'stylesheet';
stylesheetLink.href = 'https://fonts.googleapis.com/icon?family=Material+Icons';
document.head.append(stylesheetLink);