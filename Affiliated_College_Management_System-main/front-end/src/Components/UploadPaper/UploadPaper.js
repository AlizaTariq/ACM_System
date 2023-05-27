import React from 'react'
import './uploadPaper.css';

const UploadPaper = () => {
    return (
        <div className='My-body5'>
            <div className='container'>
                <div className="row RequestheaderUP">
                    <div className="courseTitleUP col-9">
                        CMP-100 Introduction to Computing
                        <br></br>
                        <div className="requestdateUP col-3">
                        requested date
                        </div>      
                    </div>
                    <div className="deadlineUP col-3">
                        paper upload deadline
                    </div>
                </div>
                <div className="row requestBodyUP">
                    <div className="col-8">
                        <div className="bookRecomended">
                            <label className='outlineTitleUP'>Book recomended: </label>
                            Nell Dale, John Lewis, Computer Science Illuminated, 5th Edition,
                            Jones & Bartlett Learning, 2012, ISBN-10: 1449672841,
                            ISBN-13: 978-1449672843.
                        </div>
                        <div className="CourseOutlineUP">
                            <label className='outlineTitleUP'>Outline:</label>
                            Introduction to Information Technology, The Internet and World
                            Wide Web, Software, Types of software, Application Software, Productivity
                            Software, System Software, Digital Logic Design, Computer Organization,
                            Operating System, Utility Programs, Hardware, Storage, Computer
                            Networks, Software development, Command Line, Little Man Computer,
                            Database Systems, Software Engineering Problem Solving, Algorithms,
                            HTML.
                        </div>
                    </div>
                    <div className="col-4 uploadPaperUP" style={{marginTop:  "10px"}}>
                        <form action="http://localhost:5000//GetPaper" method='post' enctype="multipart/form-data">
                            <input type="file" name="Paper" className="form-controlUP" required />
                            <button type="submit" className="submit-btnUP" >Upload Paper</button>
                        </form>                        
                    </div>
                </div>
            </div>
        </div>
    )
}

export default UploadPaper