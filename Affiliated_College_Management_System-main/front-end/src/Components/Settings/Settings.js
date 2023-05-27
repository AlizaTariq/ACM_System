// import React from 'react'

// const Settings = () => {
//   return (
//     <div className='FormBg'>
//         Settings       
//     </div>
//   )
// }

import React, { useState } from "react";
import './settings.css'

function Settings() {
  const [darkMode, setDarkMode] = useState(false);
  const [file, setFile] = useState(null);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission here
  };

  return (
    <div className={`settings-container ${darkMode ? "dark-mode" : ""}`}>
      <h1>Settings</h1>
      <form onSubmit={handleSubmit}>
        <h2>Profile</h2>
        <label htmlFor="name">Full Name</label>
        <input type="texts" id="name" name="name" />

        <label htmlFor="email">Email</label>
        <input type="emails" id="email" name="email" />

        <label htmlFor="password">Password</label>
        <input type="passwords" id="password" name="password" />

        <label htmlFor="profile-pic">Profile Picture</label>
        <input
          type="file"
          id="profile-pic"
          name="profile-pic"
          onChange={handleFileChange}
        />

        <h2>Notifications</h2>
        <div className="notification">
          <label htmlFor="email-notif">Email Notifications</label>
          <input type="checkbox" id="email-notif" name="email-notif" />
        </div>

        <div className="notification">
          <label htmlFor="push-notif">Push Notifications</label>
          <input type="checkbox" id="push-notif" name="push-notif" />
        </div>

        <h2>Examiner Settings</h2>
        <label htmlFor="examiner-id">Examiner ID</label>
        <input type="texts" id="examiner-id" name="examiner-id" />

        <label htmlFor="examiner-name">Examiner Name</label>
        <input type="texts" id="examiner-name" name="examiner-name" />

        <label htmlFor="examiner-email">Examiner Email</label>
        <input type="emails" id="examiner-email" name="examiner-email" />

        <button type="submits">Save Settings</button>
      </form>
    </div>
  );
}

export default Settings;

// import React, { useState } from "react";
// import "./settings.css";

// function Settings() {
//   const [darkMode, setDarkMode] = useState(false);
//   const [file, setFile] = useState(null);

//   const toggleDarkMode = () => {
//     setDarkMode(!darkMode);
//   };

//   const handleFileChange = (event) => {
//     setFile(event.target.files[0]);
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     // Handle form submission here
//   };

//   return (
//     <div className={`settings-container ${darkMode ? "dark-mode" : ""}`}>
//       <h1>Settings</h1>
//       <form onSubmit={handleSubmit}>
//         <h2>Profile</h2>
//         <label htmlFor="name"style={{ fontFamily: "Poppins", color: "#171d1f" }}>Full Name</label>
//         <input type="texts" id="name" name="name" />

//         <label htmlFor="email">Email</label>
//         <input type="emails" id="email" name="email" />

//         <label htmlFor="password">Password</label>
//         <input type="passwords" id="password" name="password" />

//         <label htmlFor="profile-pic">Profile Picture</label>
//         <input
//           type="file"
//           id="profile-pic"
//           name="profile-pic"
//           onChange={handleFileChange}
//         />

//         <h2>Notifications</h2>
//         <div className="notification">
//           <label htmlFor="email-notif">Email Notifications</label>
//           <input type="checkbox" id="email-notif" name="email-notif" />
//         </div>

//         <div className="notification">
//           <label htmlFor="push-notif">Push Notifications</label>
//           <input type="checkbox" id="push-notif" name="push-notif" />
//         </div>

//         <h2>Examiner Settings</h2>
//         <label htmlFor="examiner-id">Examiner ID</label>
//         <input type="texts" id="examiner-id" name="examiner-id" />

//         <label htmlFor="examiner-name">Examiner Name</label>
//         <input type="texts" id="examiner-name" name="examiner-name" />

//         <label htmlFor="examiner-email">Examiner Email</label>
//         <input type="emails" id="examiner-email" name="examiner-email" />

//         <button type="submits">Save Settings</button>
//       </form>
//     </div>
//   );
// }

// export default Settings;

