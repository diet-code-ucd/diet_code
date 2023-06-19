import { useState } from "react";
import Display from "./TestDisplayData";
import Login from "./Login";
import SignUp from "./SignUp";
import { BrowserRouter as Router } from "react-router-dom";
import { Routes, Route } from "react-router-dom";

function App() {
  const [currentPage, setCurrentPage] = useState("Login");

  const handlePageSwitch = (pageName: string) => {
    setCurrentPage(pageName);
  };

  return (
    <Router>
      <Routes>
        <Route path="/Display" element={<Display />} />
      </Routes>
      <div>
        {currentPage === "Login" ? (
          <Login togglePage={() => handlePageSwitch("SignUp")} />
        ) : (
          <SignUp togglePage={() => handlePageSwitch("Login")} />
        )}
      </div>
    </Router>
  );
}

export default App;
