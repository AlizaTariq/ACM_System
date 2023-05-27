import React, { useState, useEffect } from 'react'
import './requestReceived.css';

const RequestReceived = () => {

    const [getData, setData] = useState([]);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/DutyDetails')
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error(error));
    }, []);

    return (
        <div className='My-body7'>
            <div className='container'>
                <div className="row RequestheaderRR">
                    <div className="courseTitleRR col-9">
                        CMP-100 Introduction to Computing
                        <br></br>
                        <div className="requestdateRR col-3">
                        requested date
                        </div>
                    </div>
                    <div className="deadlineRR col-3">
                        deadline of paper upload
                    </div>
                </div>
                <div className="row">
                    <div className="requestBodyRR">
                        <div className="bookRecomended">
                            <label className='outlineTitleRR'>Book recomended: </label>
                            Nell Dale, John Lewis, Computer Science Illuminated, 5th Edition,
                            Jones & Bartlett Learning, 2012, ISBN-10: 1449672841,
                            ISBN-13: 978-1449672843.
                        </div>
                        <div className="CourseOutlineRR">
                            <label className='outlineTitleRR'>Outline:</label>
                            Introduction to Information Technology, The Internet and World
                            Wide Web, Software, Types of software, Application Software, Productivity
                            Software, System Software, Digital Logic Design, Computer Organization,
                            Operating System, Utility Programs, Hardware, Storage, Computer
                            Networks, Software development, Command Line, Little Man Computer,
                            Database Systems, Software Engineering Problem Solving, Algorithms,
                            HTML.
                        </div>
                    </div>
                </div>
                <div className="row requestFooterRR">
                    <button type='accept'className='col-4 AcceptBtn'>Accept</button>
                    <button type='accept'className='col-4 RejectBtn'>Reject</button>
                </div>
            </div>
        </div>
    )
}

export default RequestReceived