import { useState } from "react";
import "./App.css";
import { JobBoard } from "./components/JobBoard";
import JobPostForm from "./components/jobpost/JobPostForm";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import PaymentSuccess from "./components/jobpost/PaymentSuccess";


function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route
            path="/"
            element={
              <>
                <JobBoard />
              </>
            }
          />
          <Route
            path="/post-job"
            element={
              <div className="w-full">
                <JobPostForm />
              </div>
            }
          />
          <Route path="/payment-success" element={<PaymentSuccess />} /> 
        </Routes>
      </BrowserRouter>
    </>
  );
}

export default App;
