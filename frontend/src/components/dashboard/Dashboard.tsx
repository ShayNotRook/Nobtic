// import React from 'react'
import "./dashboard.css"


const Dashboard = () => {
  return (
    <>
      {/* <h2 className="dashboard-header">Dashboard</h2> */}
      <div className="dashboard">
        <div className="appointments-box">
          <h3 className="appointments-box-header">نوبت ها</h3>
          <p>Number of appointments: </p>
          <p>Number of upcoming appointments: </p>
          <p>Number of past appointments: </p>
        </div>
        <div className="user-box">
          <h3>User</h3>
          <p>Username: </p>
          <p>Email: </p>
        </div>
      </div>
    </>
  )
}

export default Dashboard