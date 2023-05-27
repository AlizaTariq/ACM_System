import React, { useState, useEffect } from 'react'
import Avatar from './componnets/avatar'
import UserDetails from './componnets/user-details'
import QualificationDetails from './componnets/qualification-details'
import ExperienceDetails from './componnets/experience-details'
import { useNavigate, useParams } from 'react-router-dom'
import axios from 'axios'

const ExaminerDetails = () => {
    // const navigate = useNavigate();
    // const { user_id } = useParams();
    // const [userDetails, setUserDetails] = useState({});

    // const getDetails = async () => {
    //     try {
    //         const response = await axios.post('http://localhost:5000/ExaminerDetails', { user_id });
    //         const { data } = response;
    //         setUserDetails(data);
    //     } catch (error) {
    //         console.error(error, "errop");
    //     }
    // }
    // useEffect(() => {
    //     getDetails();
    // }, [user_id]);

    return (
        <>
            <h1>hello</h1>
            {/* <div className="d-flex align-items-end justify-content-end p-5">
                <button className="btn btn-primary" onClick={() => navigate("/")}>
                    Logout
                </button>
            </div>
            <div className="container py-5">
                <div className="row">

                    <div className="col-lg-3 col-md-6">

                        <Avatar
                            src={userDetails?.personal_details?.image}
                            name={userDetails?.personal_details?.name}
                        />
                    </div>
                    <div className="col-lg-9 col-md-6">
                        <h2 className="mb-4 mt-4 mt-md-0">User Details</h2>
                        <div className="card mb-4">

                            <UserDetails data={{ ...userDetails?.personal_details, ...userDetails?.examiner_details }} />
                        </div>
                        <div className="row">
                            <div className="col-lg-6 col-12">
                                <h2 className="mb-4">Qualification Details</h2>
                                <div className="card">
                                    <QualificationDetails
                                        data={userDetails?.qualification_details}
                                    />
                                </div>
                            </div>
                            <div className="col-lg-6 col-12">
                                <h2 className="mb-4 mt-4 mt-md-0">Experience Details</h2>
                                <div className="card">
                                    <ExperienceDetails data={userDetails?.experience_details} />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div> */}
        </>
    )
}

export default ExaminerDetails
