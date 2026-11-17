import { createRoot } from "react-dom/client";
import App from "./App";
import "./App.css";

const root = document.querySelector( '#root' );
const create = createRoot( root );
create.render( <App /> );
