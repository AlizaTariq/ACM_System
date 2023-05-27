import React, { useState, useEffect } from 'react'
import axios from 'axios';
import './resultPending.css'

const ResultPending = () => {
    const [dataList, setDataList] = useState([]);
    const [Duty_ID, setId] = useState('');

    const handleDutyID = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('duty_id', Duty_ID);
        try {
            const response = await axios.post('http://127.0.0.1:5000/getRequestRecievedId', formData);
            localStorage.setItem('access_token', response.data.access_token);
            // Redirect the user to the protected route
            window.location.href = '/UploadResult';
        } catch (error) {
            console.error("error: ", error);
        }
    };
    useEffect(() => {
        fetch('http://127.0.0.1:5000/ResultUploadPending')
            .then(response => response.json())
            .then(data => setDataList(data))
            .catch(error => console.error(error));
    }, []);
    return (
        <div className='My-body3'>
            <div class="subject3-box">
                <h2 class="subject3-name">Result Pending</h2>
                <box-icon name='receipt' animation='' size='90px' color="#ffffff"></box-icon>
                <box-icon name='search-alt-2' animation='tada' size='120px' color="#ffffff"></box-icon>
                <box-icon name='math' animation='tada' size='120px' color="#ffffff"></box-icon>
                <box-icon name='book-open' animation='tada' size='100px' color="#ffffff"></box-icon>
                <div class="subject3-description">
                    <p>description if needed.</p>
                </div>
            </div>
            <div className='container'>
                <div className="row">
                    <div className='adjustment4'>
                        {dataList.map(item => (
                            <form onSubmit={handleDutyID}>
                                <div className="notification_block4">
                                    <div className='CourseTitle4'>{item[1]}</div>
                                    <div className='papertype4'>
                                        {item[3]}
                                        <button className='detail-btn' type="deatils" onClick={() => setId(item)}>See Details</button>
                                    </div>
                                    <div className='date4'>{item[2]}</div>
                                </div>
                            </form>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default ResultPending