import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import './examinerQualification.css';

const ExaminerQualification = () => {

    const [dataList, setDataList] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/NewQualifications')
            .then(response => response.json())
            .then(data => setDataList(data))
            .catch(error => console.error(error));
    }, []);

    const [degree_title, setDegreeTitle] = useState('');
    const [institution, setInstitution] = useState('');
    const [starting_date, setStartingDate] = useState('');
    const [ending_date, setEndingDate] = useState('');
    const fileInputRef = useRef(null);
    const [error, setError] = useState('');
    const handleExaminerQualification = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('degree_title', degree_title);
        formData.append('institution', institution);
        formData.append('starting_date', starting_date);
        formData.append('ending_date', ending_date);
        formData.append('transcript', fileInputRef.current.files[0]);
        try {
            const response = await axios.post('http://127.0.0.1:5000/ExaminerQualification', formData);
            localStorage.setItem('access_token', response.data.access_token);
            // Redirect the user to the protected route
            window.location.href = '/ExaminerQualification';
        } catch (error) {
            console.error("error: ", error);
            setError('Some Input is Wrong');
        }
    };

    useEffect(() => {
        const modal = document.getElementById("AddNewQualification");
        const btn = document.getElementById("myBtn");
        const span = document.getElementsByClassName("close")[0];

        btn.onclick = function () {
            modal.style.display = "block";
        }
        span.onclick = function () {
            modal.style.display = "none";
        }
        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        }

    });
    
    return (
        <div className='FormBgEQ'>
            <div className='bg-imgEQ'>
                <div className="contentEQ" style={{ width: "522px", height: "87%" }}>
                    <header>
                        <h1 style={{ color: "#171d1f", fontFamily: "'Poppins'", fontWeight: "500" }}>Qualification</h1>
                    </header>
                    <table className='TableStyleEQ' border="1">
                        <tr>
                            <th>Sr #</th>
                            <th>Degree Title</th>
                            <th>Institute Name</th>
                            <th>Starting Date</th>
                            <th>Ending Date</th>
                        </tr>
                        {dataList.map((item, index) => (
                            <tr>
                            <td>{index + 1}</td>
                            <td>{item[2]}</td>
                            <td>{item[3]}</td>
                            <td>{item[4]}</td>
                            <td>{item[5]}</td>
                        </tr>
                        ))}                        
                    </table>
                    <div className="container ButtonsEQ">
                        <div>
                            <div className='NextBtnEQ'>
                                <button type="button" id='myBtn'>Add New</button>
                            </div>
                            <div id="AddNewQualification" class="modal">
                                <div class="modal-content" style={{backgroundColor : "#232323"}}>
                                    <span class="close">&times;</span>
                                    <div>
                                        <form onSubmit={handleExaminerQualification}>
                                            <div className="maindiv">
                                                <span></span>
                                                <input type="text" className='input-box' placeholder='Enter Degree Title' name='degree_title' onChange={(e) => setDegreeTitle(e.target.value)} required />
                                            </div>
                                            <div className="maindiv">
                                                <span></span>
                                                <input type="text" className='input-box' placeholder='Enter Institute Name' name='institution' onChange={(e) => setInstitution(e.target.value)} required />
                                            </div>
                                            <div className="maindiv">
                                                <span></span>
                                                <label className='label_' for="starting_date">Starting Date:</label>
                                                <input className="form-control input-box" type="date" name="starting_date" runat="server" onChange={(e) => setStartingDate(e.target.value)}
                                                    style={{ height: "30px", width: "fit-content" }} />
                                            </div>
                                            <div className="maindiv">
                                                <span></span>
                                                <label className='label_' for="ending_date">Ending Date:</label>
                                                <input className="form-control input-box" type="date" name="ending_date" runat="server" onChange={(e) => setEndingDate(e.target.value)}
                                                    style={{ height: "30px", width: "fit-content" }} />
                                            </div>
                                            <div className="maindiv">
                                                <label className='label_' for="Certificate">Transcript: </label>
                                                <input type="file" name="transcript" className="form-control" ref={fileInputRef} required />
                                            </div>
                                            <div className="AddBtn">
                                                <input type="submit" value="Add" />
                                            </div>
                                            <div>
                                                {error && <div>{error}</div>}
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div className='NextBtnEQ'>
                            <a href="http://localhost:3000/ExaminerExp">
                                <button type="submit">Next Page</button>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default ExaminerQualification