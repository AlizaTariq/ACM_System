import React from 'react'
import 'boxicons'
import { useState, useEffect } from "react";
import { NavLink } from 'react-router-dom';
import "./navbar.css";

const Navbar = () => {
  return (
    <div className='Navbar'>
      <div className="col-3">
      <a href="/" className='nav-logo'><box-icon type='logo' name='edge' animation='tada' color='#DDDBCB' size='45px'></box-icon>xaminer Portal</a>
      </div>
      <div className='nav-items col-4'>
        <form action="post">
          <div className="maindiv">
             <input type="text" className="inputsearch" name='q' placeholder='Search' required />
             <button  className="btnsubmit" type="submit"><box-icon name='search-alt' animation='tada' color='#DDDBCB' size='45px'></box-icon></button>
          </div>
        </form>
      </div>
      <div className='header-btn col-3' style={{"text-align" : "end"}}>
        <a href="/Profile" className='progap'><box-icon name='user-circle' size='30px' color="#DDDBCB"></box-icon></a>
        <a href="/Recent" className='progap'><box-icon type='solid' name='bell-ring' animation='tada' size='30px' color="#DDDBCB"></box-icon></a>
        <a href="/Settings" className='progap'><box-icon name='cog' animation='spin' size='30px' color="#DDDBCB"></box-icon></a>
      </div>
      <div className='header-btn col-2'  style={{"text-align" : "end"}}>
        <a href="/SignupPersonalInfo" className='signlog'><box-icon name='log-out' size='22px' color="#DDDBCB"></box-icon>Log Out</a>
      </div>
      <div className='VerNavbar'>
        <div className='vernav'>
          <a href="/Home">Home</a>
          <a href="/Notifications">Requests</a>
          <a href="/DuePaper">Due Paper</a>
          <a href="ResultPending">Result Pending</a>
        </div>
      </div>
    </div>
    


  )
}

export default Navbar
