import React, { useState, useEffect } from 'react'
import axios from 'axios';
import './duePaper.css'

const DuePaper = () => {
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
            window.location.href = '/AcceptedRequest';
        } catch (error) {
            console.error("error: ", error);
        }
    };
    useEffect(() => {
        fetch('http://127.0.0.1:5000/PaperPendingDuty')
            .then(response => response.json())
            .then(data => setDataList(data))
            .catch(error => console.error(error));
    }, []);
    return (
        <div className='My-body2'>
            <div class="subject2-box">
                <h2 class="subject2-name">Due Paper</h2>
                <box-icon name='sort-a-z' animation='tada' size='140px' color="#ffffff"></box-icon>
                <box-icon name='time-five' animation='tada' size='60px' color="#ffffff"></box-icon>
                <box-icon name='task' animation='flashing' size='100px' color="#ffffff"></box-icon>
                <box-icon name='pencil' animation='tada' size='100px' color="#ffffff"></box-icon>
                <box-icon name='calculator' animation='' size='80px' color="#ffffff"></box-icon>
                <box-icon name='detail' animation='' size='70px' color="#ffffff"></box-icon>
                <box-icon type='solid' name='graduation' animation='tada' size='110px' color="#ffffff"></box-icon>
                {/* <box-icon type='logo' name='deezer' animation='flashing' size='70px' color="#ffffff"></box-icon> */}
                <div class="subject2-description">
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

export default DuePaper