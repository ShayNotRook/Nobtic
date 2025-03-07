import React from 'react';
import './appointment.css';
import {
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Typography,
  Box,
  Button,
  Divider
} from '@mui/material';

import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

export interface Appointment {
    id: number,
    customer_name: string,
    service: string
    app_start: string;
    app_end: string;
    slot: number;
    status: string;
    receipt_img?: string;
    receipt_txt?: string;
}

interface DayAppointment {
    dayLabel: string;
    appointments: Appointment[];
}

interface AppointmentsTabProps {
    data: DayAppointment[];
    onApprove: (appointmentId: number) => void;
    onDecline: (appointmentId: number) => void;
}

const AppointmentsTab: React.FC<AppointmentsTabProps> = ({ data, onApprove, onDecline }) => {
  return (
      <Box sx={{ p: 2 }}>
        {data.map((day) => (
          <Box key={day.dayLabel} sx={{ mb: 3 }}>
            <Typography variant='h6' sx={{ mb: 1}}>
              {day.dayLabel}
            </Typography>
            {day.appointments.map((app) => (
              <Accordion key={app.id} sx={{ mb: 1 }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                {/* Top-level summary (customer_name, service, app_start)*/}
                  <Box sx={{ display: "flex", flexDirection: "column", width: "100%" }}>                    
                    <Typography variant='subtitle1' sx={{ fontWeight: 600 }}>
                      {app.customer_name}
                    </Typography>
                    <Typography variant="body2" sx={{ color: "text.secondary" }}>
                      {app.service} | شروع: {app.app_start}
                    </Typography>
                  </Box>
                </AccordionSummary>
                <AccordionDetails>
                  {/* Receipt info or image*/}
                  {app.receipt_img ? (
                    <Box
                    component="img"
                    src={app.receipt_img}
                    alt='رسید تراکنش'
                    sx={{
                        width: "100%",
                        height: "auto",
                        borderRadius: 1,
                        mb: 2
                      }}
                    />
                  ) : app.receipt_txt ? (
                    <Typography
                      variant='body2'
                      sx={{
                        p: 2,
                        border: "1px dashed gray",
                        borderRadius: 1,
                        mb: 2
                      }}
                    >
                      {app.receipt_txt}
                    </Typography>
                  ) : (
                    <Typography variant='body2' sx={{ color: 'text.secondary', mb: 2}}>
                        هیچ رسیدی دریافت نشده است.
                    </Typography>
                  )}

                  <Divider sx={{ mb: 2 }} />
                  
                  {/* Approve / Decline buttons */}
                  <Box sx={{ display: "flex", justifyContent: "space-around" }}>
                    <Button
                      variant='contained'
                      color='success'
                      onClick={() => onApprove(app.id)}
                    >
                      تایید
                    </Button>
                    <Button
                      variant='contained'
                      color='error'
                      onClick={() => onDecline(app.id)}
                    >
                      رد
                    </Button>
                  </Box>
                </AccordionDetails>
              </Accordion>
            ))}
          </Box>
        ))}
      </Box>
  )
}
export default AppointmentsTab;