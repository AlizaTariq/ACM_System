import React from 'react'
import './uploadResult.css';

const UploadResult = () => {
    return (
        <div className='My-body6'>
            <div className='container'>
                <div className="row RequestheaderUR">
                    <div className="courseTitleUR col-9">
                        CMP-100 Introduction to Computing
                        <br></br>
                        <div className="requestdateUR col-3">
                        requested date
                        </div>                      
                    </div>
                    <div className="deadlineUR col-3">
                        result upload deadline
                    </div>
                </div>
                <div className="row requestBodyUR">
                    <div className="col-8">
                        <div className="bookRecomended">
                            <label className='outlineTitleUR'>Book recomended: </label>
                            Nell Dale, John Lewis, Computer Science Illuminated, 5th Edition,
                            Jones & Bartlett Learning, 2012, ISBN-10: 1449672841,
                            ISBN-13: 978-1449672843.
                        </div>
                        <div className="CourseOutline">
                            <label className='outlineTitleUR'>Outline:</label>
                            Introduction to Information Technology, The Internet and World
                            Wide Web, Software, Types of software, Application Software, Productivity
                            Software, System Software, Digital Logic Design, Computer Organization,
                            Operating System, Utility Programs, Hardware, Storage, Computer
                            Networks, Software development, Command Line, Little Man Computer,
                            Database Systems, Software Engineering Problem Solving, Algorithms,
                            HTML.
                        </div>
                    </div>
                    <div className="col-4 uploadPaperUR" style={{ marginTop: "10px" }}>
                        <form action="http://localhost:5000//GetResult" method='post' enctype="multipart/form-data">
                            <input type="file" name="result" className="form-controlUR" required />
                            <button type="submit" className="submit-btnUR" >Upload Result</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default UploadResult