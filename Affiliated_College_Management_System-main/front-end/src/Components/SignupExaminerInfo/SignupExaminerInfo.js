import React, { useState, useRef } from 'react';
import axios from 'axios';
import './signupExaminerInfo.css';

const SignupExaminerInfo = () => {
  const [institution, setInstitution] = useState('');
  const fileInputRef = useRef(null);
  const [error, setError] = useState('');

  const handleSignUpExaminer = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('institution', institution);
    formData.append('resume', fileInputRef.current.files[0]);
    try {
      const response = await axios.post('http://127.0.0.1:5000/SignUpExaminerInfo', formData);
      localStorage.setItem('access_token', response.data.access_token);
      // Redirect the user to the protected route
      window.location.href = '/ExaminerQualification';
    } catch (error) {
      console.error("error: ", error);
      setError('Some Input is Wrong');
    }
  };
  return (
    <div className='FormBg'>
      <div className='bg-img'>
        <div className="content" style={{ width: "510px" }}>
          <header type="EI"style={{ fontFamily: "Poppins", color: "#171d1f" }}>Examiner Information</header>
          {/* <form action="http://localhost:5000//SignUpExaminerInfo" method='post' enctype="multipart/form-data"> */}
          <form onSubmit={handleSignUpExaminer}>
            <div className="maindiv">
              <span></span>
              <input type="text" className="input-box" placeholder='Enter Your Institution Name' name='institution' onChange={(e) => setInstitution(e.target.value)} required />
            </div>
            <span></span>
            <input type="file" name="resume" className="form-control" ref={fileInputRef} required />
            <div>
              <button type="submit" className="submit-btn" >Next</button>
            </div>
            <div>
              {error && <div>{error}</div>}
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}

// ReactDOM.render(<SignupExaminerInfo />, document.getElementById('root'));
export default SignupExaminerInfo