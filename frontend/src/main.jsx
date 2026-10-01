import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./AgriSenseApp";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);