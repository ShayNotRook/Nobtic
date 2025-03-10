import { useState }from "react";

import './login.css';
import { useNavigate } from "react-router-dom";

const API: string = "https://nobtic.ir/backend/users/api/token/";


interface LoginFormProps {
    onLogin: (access: string, refresh: string) => void;
    // className: string;
}



const LoginForm = ({ onLogin }: LoginFormProps) => {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const navigate = useNavigate();

    
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.name === "username") {
            setUsername(e.target.value);
        } else if (e.target.name === "password") {
            setPassword(e.target.value);
        }
    }

    const handleSubmit = async (e: { preventDefault: () => void; }) => {
        e.preventDefault()
        const response = await fetch(API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();
        if (response.ok) {
            onLogin(data.access, data.refresh);
            navigate("/");
        } else {
            alert("Login failed")
        }
    };

    return (
        <form className="login-form" onSubmit={handleSubmit}>
            <h3>ورود</h3>
            <div>
                <input
                    type="text"
                    name="username"
                    value={username}
                    onChange={handleChange}
                    placeholder="نام کاربری"
                />
                <input
                    type="password"
                    name="password"
                    value={password}
                    onChange={handleChange}
                    placeholder="رمز عبور"
                />
            </div>
            <button type="submit">Login</button>
        </form>
    )
};


export default LoginForm;