import { useState } from "react";
import { useNavigate } from "react-router-dom";

interface LoginProps {
  togglePage: () => void;
}

function Login(props: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(email);

    navigate("/Display", { replace: true });
  };

  const handlePageToggle = () => {
    props.togglePage();
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label htmlFor="Email">Email</label>
        <input
          value={email}
          type="email"
          placeholder="abc@myemail.com"
          id="email"
          name="email"
          onChange={(e) => setEmail(e.target.value)}
        />
        <label htmlFor="Password">Password</label>
        <input
          value={password}
          type="password"
          placeholder="******"
          id="password"
          name="password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Log In</button>
      </form>
      <button onClick={handlePageToggle}>New to this? Sign up now!</button>
    </>
  );
}

export default Login;
