import React from "react";
import ReactDOM from "react-dom/client";
import { HashRouter, Routes, Route } from "react-router-dom";
import { initializeIcons } from "@fluentui/react";

import "./index.css";

import Layout from "./pages/layout/Layout";
import NoPage from "./pages/NoPage";
import OneShot from "./pages/oneshot/OneShot";
import Chat from "./pages/chat/Chat";

initializeIcons();

export default function App() {
***REMOVED***return (
***REMOVED***<HashRouter>
***REMOVED******REMOVED***<Routes>
***REMOVED******REMOVED***<Route path="/" element={<Layout />}>
***REMOVED******REMOVED******REMOVED***<Route index element={<Chat />} />
***REMOVED******REMOVED******REMOVED***<Route path="qa" element={<OneShot />} />
***REMOVED******REMOVED******REMOVED***<Route path="*" element={<NoPage />} />
***REMOVED******REMOVED***</Route>
***REMOVED******REMOVED***</Routes>
***REMOVED***</HashRouter>
***REMOVED***);
}

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
***REMOVED***<React.StrictMode>
***REMOVED***<App />
***REMOVED***</React.StrictMode>
);
