// import React from 'react'
import "./dashboard.css"
import { useEffect, useState } from 'react';
import AppointmentsTable, { Appointment } from "./AppTable/AppointmentsTable";
import LoginForm from "../auth/Login";
import UserCard from "./User/UserCard";


interface Slot {
  id: number;
  date: string;
  day_of_week: string;
  appointments: Appointment[];
}

const API: string = "http://localhost:8000/schedule/api/v1";

const Dashboard = () => {
  const [slots, setSlots] = useState<Slot[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<Slot| null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);

  
  useEffect(() => {
    const access = localStorage.getItem('accessToken');
    const refresh = localStorage.getItem('refreshToken');
    if (access && refresh) {
      setAccessToken(access);
      setRefreshToken(refresh);
      fetchSlots(access);
    }
  }, []);

  const fetchSlots = (token: string) => {
    fetch(`${API}/appointmentslots/`, {
      headers: {
        "Authorization": `Bearer ${token}`
      }
    })
    .then(response => response.json())
    .then(data => {
      if (Array.isArray(data)) {
        setSlots(data);
        // Set default to today's slot
        const todaySlot = data.find((slot: { date: string | number | Date; }) => new Date(slot.date).toDateString());
        if (todaySlot) {
          setSelectedSlot(todaySlot);
          loadAppointments(todaySlot.id, token);
        }
      } else {
        console.error("Expected an array but got:", data);
      }
    })
    .catch(error => console.error("Error fetching slots:", error));
  }

  const loadAppointments = (slotId: number, token: string) => {
    console.log(token)
    fetch(`${API}/appointmentslots/${slotId}/appointments/`,
      {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })
        .then(response => response.json())
        .then(data => {
          if (Array.isArray(data)){
            setAppointments(data);
          } else {
            console.error("Expected an array but got:", data)
          }
      })
      .catch(error => console.error("Error fetching appointments:", error));
  };

  const handleSlotClick = (slotId: number) => {
    const slot = slots.find(s => s.id === slotId) || null;
    setSelectedSlot(slot);
    if (slot) {
      loadAppointments(slot.id, accessToken!);
    }
  };

  const handleLogin = (access: string, refresh: string) => {
    setAccessToken(access);
    setRefreshToken(refresh);
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    fetchSlots(access);
  };


  const refreshAccessToken = async () => {
    const response = await fetch(`${API}/token/refresh/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    const data = await response.json();
    if (response.ok) {
      setAccessToken(data.access);
      localStorage.setItem('accessToken', data.access);
    } else {
      console.error("Failed to refresh token:", data);
    }
  };

  useEffect(() => {
    const interval = setInterval(() => {
      if (refreshToken) {
        refreshAccessToken();
      }  
    }, 4 * 60 * 1000);
    return () => clearInterval(interval);
  }, [refreshToken]);

  

  return (
    <>
      <div className="dashboard">
        {!accessToken ? ( 
          <LoginForm onLogin={handleLogin}/>
        ) : (
          <>
          {/* <h2 className="dashboard-header">Dashboard</h2> */}
          <div className="main-content">
            <div className="content">
              {/* <div className="stats-container">
                <div className="stat-box">
                  <h3>Statistics</h3>
                  <p>Number of appointments: {appointments.length}</p>
                  <p>Number of upcoming appointments: {appointments.filter(app => new Date(app.app_start) > new Date()).length}</p>
                  <p>Number of past appointments: {appointments.filter(app => new Date(app.app_start) <= new Date()).length}</p>
                </div>
              </div> */}
              <div className="slots-container">
                <h3>انتخاب روز</h3>
                <div className="slots">
                  {slots.map(slot => (
                    <div
                      key={slot.id}
                      className={`slot ${selectedSlot?.id === slot.id ? "selected" : ""}`}
                      onClick={() => handleSlotClick(slot.id)}
                    >
                      {new Date(slot.date).toLocaleDateString()} - {slot.day_of_week}
                    </div>
                  ))}
                </div>
              </div>
              <AppointmentsTable appointments={appointments} />
            </div>
            <div className="user-box">
              <UserCard token={accessToken!} />
            </div>
          </div>
        </>
          )}
      </div>
    </>
  )
}

export default Dashboard