import { useState } from "react";
import { useNavigate } from "react-router-dom";

interface SignUpProps {
  togglePage: () => void;
}

function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log(email);
  };

  const handlePageToggle = () => {
    //props.togglePage();
    navigate("/Login", { replace: true });
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <label htmlFor="FirstName">First Name </label>
        <input
          value={firstName}
          type="string"
          placeholder="First Name"
          id="firstName"
          name="firstName"
          onChange={(e) => setFirstName(e.target.value)}
        ></input>
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
      <button onClick={handlePageToggle}>
        Already have an Account? Login in
      </button>
    </>
  );
}

export default SignUp;
