import { useState } from "react";
//import HelloWorld from "./HelloWorld";
import Login from "./Login";
import SignUp from "./SignUp";

function App() {
  const [currentPage, setCurrentPage] = useState("Login");

  const handlePageSwitch = (pageName: string) => {
    setCurrentPage(pageName);
  };

  return (
    <div>
      {currentPage === "Login" ? (
        <Login togglePage={() => handlePageSwitch("SignUp")} />
      ) : (
        <SignUp togglePage={() => handlePageSwitch("Login")} />
      )}
    </div>
  );
}

export default App;
