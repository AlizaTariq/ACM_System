// import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';  //npm i react-router-dom 

import DuePaper from './Components/DuePaper/DuePaper';
import Home from './Components/Home/Home';
import Login from './Components/Login/Login';
import Navbar from './Components/Navbar/Navbar';
import Notifications from './Components/Notifications/Notifications';
import RequestReceived from './Components/RequestReceived/RequestReceived';
import ResultPending from './Components/ResultPending/ResultPending';
import Settings from './Components/Settings/Settings';
import SignupExaminerInfo from './Components/SignupExaminerInfo/SignupExaminerInfo';
import SignupPersonalInfo from './Components/SignupPersonalInfo/SignupPersonalInfo';
import UploadPaper from './Components/UploadPaper/UploadPaper';
import UploadResult from './Components/UploadResult/UploadResult';
import ExaminerExp from './Components/ExaminerExp/ExaminerExp';
import ExaminerQualification from './Components/ExaminerQualification/ExaminerQualification';
import Profile from './Components/Profile/Profile';
import AcceptedRequest from './Components/AcceptedRequest/AcceptedRequest';
import 'boxicons'
import ExaminerDetails from './Components/ExaminerDetails/ExaminerDetails';

// function App() {
  // return (
  //   <div className="App">
      {/* <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/SignupPersonalInfo" element={<SignupPersonalInfo />} />
          <Route path="/SignupExaminerInfo" element={<SignupExaminerInfo />} />
          <Route path="/ExaminerQualification" element={<ExaminerQualification />} />
          <Route path="/ExaminerExp" element={<ExaminerExp />} />
          <Route element={<Navbar />}>
            <Route path="/UploadPaper" element={<UploadPaper />} />
            <Route path="/RequestRecieved" element={<RequestReceived />} />
            <Route path="/Notifications" element={<Notifications />} />
            <Route path="/Profile" element={<Profile />} />
            <Route path="/Home" element={<Home />} />
            <Route path="/DuePaper" element={<DuePaper />} />
            <Route path="/ResultPending" element={<ResultPending />} />
            <Route path="/UploadResult" element={<UploadResult />} />
            <Route path="/Settings" element={<Settings />} />
          </Route>
        </Routes>
      </Router> */}
    {/* </div>
  ); */}
// }
// function App() {
//   return (
//     <div className="App">
//       <Router>
//         <Routes>
//           <Route path="/" element={<Login />} />
//           <Route path="/SignupPersonalInfo" element={<SignupPersonalInfo />} />
//           <Route path="/SignupExaminerInfo" element={<SignupExaminerInfo />} />
//           <Route path="/ExaminerQualification" element={<ExaminerQualification />} />
//           <Route path="/ExaminerExp" element={<ExaminerExp />} />
//           <Route element={<Navbar />}>
//               <Route path="/UploadPaper" element={<UploadPaper />} />
//               <Route path="/RequestRecieved" element={<RequestReceived />} />
//               <Route path="/Notifications" element={<Notifications />} />
//               <Route path="/Profile" element={<Profile />} />
//               <Route path="/Home" element={<Home />} />
//               <Route path="/DuePaper" element={<DuePaper />} />
//               <Route path="/ResultPending" element={<ResultPending />} />
//               <Route path="/UploadResult" element={<UploadResult />} />
//               <Route path="/Settings" element={<Settings />} />
//           </Route>
//         </Routes>
//       </Router>
//     </div>
//   );
// }

function App() {
  return (
    <div className="App">
      <Router>
        <Navbar />
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/SignupPersonalInfo" element={<SignupPersonalInfo />} />
            <Route path="/SignupExaminerInfo" element={<SignupExaminerInfo />} />
            <Route path="/ExaminerQualification" element={<ExaminerQualification />} />
            <Route path="/ExaminerExp" element={<ExaminerExp />} />
            <Route path="/UploadPaper" element={<UploadPaper />} />
            <Route path="/RequestRecieved" element={<RequestReceived />} />
            <Route path="/Notifications" element={<Notifications />} />
            <Route path="/Profile" element={<Profile />} />
            <Route path="/Home" element={<Home />} />
            <Route path="/DuePaper" element={<DuePaper />} />
            <Route path="/ResultPending" element={<ResultPending />} />
            <Route path="/UploadResult" element={<UploadResult />} />
            <Route path="/Settings" element={<Settings />} />
            <Route path="/AcceptedRequest" element={<AcceptedRequest />} />
          </Routes >
      </Router>
    </div>
  );
}

export default App