import React, { useState, useEffect } from "react";
// npm install axios
import axios from 'axios';
import './login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            console.log("in try")
            const response = await axios.post('http://127.0.0.1:5000/ExaminerLogin', { email, password });
            localStorage.setItem('access_token', response.data.access_token);
            // Redirect the user to the protected route
            window.location.href = '/Notifications';
        } catch (error) {
            // document.getElementById("msj").textContent = error;
            console.error(error);
            setError('Invalid username or password');
        }
    };
    useEffect(() => {
        const showBtn = document.getElementById("show");
        showBtn.addEventListener("click", function () {
            const pass_field = document.getElementById("pass-key");
            console.log(pass_field.type);
            if (pass_field.type === "password") {
                pass_field.type = "text";
                showBtn.textContent = "Hide";
                showBtn.style.color = "#3498db";
            }
            else {
                pass_field.type = "password";
                showBtn.textContent = "Show";
                showBtn.style.color = "#222";
            }
        });
    });

    return (
        <>
            <div className='FormBglogin'>
                <div className='loginExaminer'>
                    <style>
                        <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css' />
                    </style>
                    <div className="bg-imglogin">
                        <div className="contentlogin">
                            <header><h1 style={{ color: "#171d1f", fontFamily: "Poppins", fontWeight: "600" }}>Log In form</h1></header>
                            <header type="PI" style={{ fontFamily: "Poppins", color: "#171d1f" }}>Enter your registered mail and password:</header>
                            <form onSubmit={handleLogin}>

                                <div className="maindivlogin">
                                    <span className="fa fa-user"></span>
                                    <input type="text" name='email' className="fa input-boxlogin" placeholder='Enter Email' onChange={(e) => setEmail(e.target.value)} required />
                                </div>

                                <div className="maindivlogin">
                                    <span className='fa fa-lock'></span>
                                    <input type="password" className="pass-keylogin" id='pass-key' name='password' placeholder='Password' onChange={(e) => setPassword(e.target.value)} required />
                                    <span className='showlogin' id='show'>Show</span>
                                </div>

                                <div className="passlogin">
                                    <a href="/SignupPersonalInfo">Don't have an account? Sign up</a>
                                </div>
                                <div>
                                    <button type="submit" className="submit-btnlogin" >Login</button>
                                </div>
                                <div>
                                    {error && <div>{error}</div>}
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

export default Login