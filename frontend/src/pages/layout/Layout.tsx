import { Outlet, NavLink, Link } from "react-router-dom";

import github from "../../assets/github.svg";

import styles from "./Layout.module.css";

const Layout = () => {
***REMOVED***return (
***REMOVED***<div className={styles.layout}>
***REMOVED******REMOVED***<header className={styles.header} role={"banner"}>
***REMOVED******REMOVED***<div className={styles.headerContainer}>
***REMOVED******REMOVED******REMOVED***<Link to="/" className={styles.headerTitleContainer}>
***REMOVED******REMOVED******REMOVED***<h3 className={styles.headerTitle}>Azure OpenAI</h3>
***REMOVED******REMOVED******REMOVED***</Link>
***REMOVED******REMOVED***</div>
***REMOVED******REMOVED***</header>

***REMOVED******REMOVED***<Outlet />
***REMOVED***</div>
***REMOVED***);
};

export default Layout;
