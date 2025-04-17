import "./App.css";
import { AppProvider } from "./AppContext";
import ResizableLayout from "./components/ResizableLayout";

import "normalize.css";
import Toolbar from "./components/Toolbar";

function App() {
  return (
    <>
      <AppProvider>
        <div
          style={{ display: "flex", flexDirection: "column", height: "100vh" }}
        >
          <Toolbar />
          <ResizableLayout />
        </div>
      </AppProvider>
    </>
  );
}

export default App;
