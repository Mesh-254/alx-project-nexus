import { useState } from "react";
import "./App.css";
import { JobBoard } from "./components/JobBoard"


function App() {
  const [count, setCount] = useState(0);

  return (
    <>
     <JobBoard />
    </>
  );
}

export default App;
