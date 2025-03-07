import React from 'react'
import "./dashboard.css"
import { useEffect, useState } from 'react';
import { Appointment } from "./AppTable/AppointmentsTable";
import UserCard from "./User/UserCard";
import { Box, Typography, Paper, Button,
         Dialog, DialogActions, DialogContent } from "@mui/material";
import { useNavigate } from "react-router-dom";



interface Slot {
  id: number;
  date: string;
  day_of_week: string;
  appointments: Appointment[];
}

const API: string = "http://nobtic.ir/backend/schedule/api/v1";
const USER_API: string = "https://nobtic.ir/backend/users/api"

const Dashboard: React.FC<{ availableAccess: string}> = ({ availableAccess }) => {
  const [slots, setSlots] = useState<Slot[]>([]);
  const [_, setAppointments] = useState<Appointment[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<Slot| null>(null);
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState<boolean>(false);

  const access_token = availableAccess;
  const navigate = useNavigate();

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

  const refreshAccessToken = async () => {
    const response = await fetch(`${USER_API}/token/refresh/`, {
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
      navigate('/login');
      console.error("Failed to refresh token:", data);
    }
  };


  
  // Approved funcs
  function convertPersianDigitsToEnglish(input: string): string {
    return input.replace(/[۰-۹]/g, (d) =>
      String(d.charCodeAt(0) - 1776)
    );
  }

  const normalizeDate = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate());

  const getSlotLabel = (dateStr: string): string => {
    const slotDate = new Date(dateStr);
    const today = new Date();
    const tommorow = new Date();
    tommorow.setDate(today.getDate() + 1);

    const normSlot = normalizeDate(slotDate).getTime();
    const normToday = normalizeDate(today).getTime();
    const normTommorow = normalizeDate(tommorow).getTime();

    if (normSlot === normToday) {
      return "امروز";
    } else if (normSlot === normTommorow) {
      return "فردا"
    } else {
      return convertPersianDigitsToEnglish(slotDate.toLocaleDateString('fa-IR'))
    }
  }


  const handleApprove = async(appId: number) => {
    const response = await fetch(`${API}/app/approve/${appId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()
    console.log(data)
  }
  
  const handleDecline = async(appId: number) => {
    const response = await fetch(`${API}/app/decline/${appId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    const data = await response.json()
    console.log("Declined", data)
  }

  useEffect(() => {
    const interval = setInterval(() => {
      if (refreshToken) {
        refreshAccessToken();
      }  
    }, 4 * 60 * 1000);
    return () => clearInterval(interval);
  }, [refreshToken]);

  

  return (
    <Box>
      <>
        <Box sx={{ mb: 2, p: 4}}>
          <UserCard token={access_token} />
        </Box>
        <Typography variant="h6" sx={{ mb: 1 }}>
          انتخاب روز
        </Typography>
        <Box sx={{ display: 'flex', gap: 1, overflowX: 'scroll', pb: 2, maxWidth: "100vw", borderBottom: "1px solid rgb(98, 98, 98)"}}>
          {slots.map((slot) => (
            <Paper
              key={slot.id}
              sx={{
                flex: '0 0 auto',
                p: 2,
                minWidth: 80,
                textAlign: 'center',
                cursor: 'pointer',
                borderRadius: "50px",
                border: selectedSlot?.id === slot.id ? '2px solid #1976d2': '0.5px solid #ccc',
                bgcolor: selectedSlot?.id === slot.id ? 'primary.light' : 'white',
                transition: 'transform 0.2s ease',
                '&:hover': {transform: 'scale(1.05'},
              }}
              onClick={() => handleSlotClick(slot.id)}
              >
                {getSlotLabel(slot.date)}
              </Paper>
          ))}
        </Box>
        {selectedSlot && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6" sx={{ mb: 2 }}>
              نوبت های {getSlotLabel(selectedSlot.date)}
            </Typography>
            {selectedSlot.appointments.length === 0 ? (
              <Typography variant="body1" color="text.secondary" fontWeight="bold" align='center'>
                بدون رزرو
              </Typography>
            ) : (
              <Box sx={{margin: "auto 8px"}}>
              {selectedSlot.appointments.map((app) => (
                <Paper key={app.id} sx={{ p: 2, mb: 2 , borderRadius: "4px"}}>
                  <Typography variant="subtitle1" fontWeight="bold">
                    {app.customer_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" fontWeight='bold'>
                    {app.service} | از {app.app_start} تا {app.app_end}
                  </Typography>
                  {app.status === "تایید شده" ? (
                    <Typography sx={{
                      backgroundColor: "#0c8408",
                      color: "#f9f9f9",
                      borderRadius: "10px",
                      textAlign: "center",
                      width: "25%",
                      margin: "0 auto",
                      marginTop: "8px"
                    }}>
                      تایید شده
                    </Typography>
                  ) : app.status === 'رد شده' ? (
                    <Typography variant="h4">
                      رد شده
                    </Typography>
                  ) : (
                      <>
                        {app.receipt_img ? (
                          <Button 
                            variant="contained"
                            type='button' 
                            onClick={() => setIsOpen(true)}
                            > 
                              تصویر تراکنش
                          </Button>                          
                        ) : app.receipt_txt ? (
                        <Typography variant="body2" sx={{ mt: 1, p: 1, border: "1px dashed gray", borderRadius: 1 }}>
                          {app.receipt_txt}
                        </Typography>
                        ) : "رسیدی دریافت نشده"}
                        {isOpen && (
                          <Dialog 
                            open={isOpen}
                            onClose={() => setIsOpen(false)}
                            maxWidth="md"
                            fullWidth>
                              {/* <DialogTitle>رسید</DialogTitle> */}
                              <DialogContent>
                                <img 
                                  src={app.receipt_img}
                                  alt='رسید'
                                  style={{
                                    width: "100%",
                                    maxHeight: "70vh",
                                    objectFit: "contain"
                                  }} />
                              </DialogContent>
                              <DialogActions>
                                  <Button onClick={() => setIsOpen(false)} color='primary'>
                                    بستن
                                  </Button>
                              </DialogActions>  
                          </Dialog>
                        )}
                        <Box sx={{ display: 'flex', justifyContent: "end", gap: 1, mt: 2}}>
                          <Button variant="contained" color="success" onClick={() => handleApprove(app.id)}>
                            تایید
                          </Button>
                          <Button variant="outlined" color="error" onClick={() => handleDecline(app.id)}>
                            رد
                          </Button>
                        </Box>
                      </>
                    )}
                </Paper>
              ))}
              </Box>
            )}
          </Box>
        )}
      </>
    </Box>
  )
}

export default Dashboard