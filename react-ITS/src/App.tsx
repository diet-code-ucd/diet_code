import { useState } from "react";
import Display from "./TestDisplayData";
import Login from "./Login";
import SignUp from "./SignUp";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
  };

  return (
    <Router>
      <Routes>
        <Route path="/Display" element={<Display />} />
        <Route path="/SignUp" element={<SignUp />} />
        <Route path="/Login" element={<Login onLogin={handleLogin} />} />
      </Routes>
      <div>{isLoggedIn ? <Login onLogin={handleLogin} /> : <Display />}</div>
    </Router>
  );
}

export default App;
