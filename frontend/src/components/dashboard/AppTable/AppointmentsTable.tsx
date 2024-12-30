import React from 'react';

import './appointment.css';

export interface Appointment {
    id: number,
    customer_name: string,
    service: null | {name: string},
    app_start: string;
    app_end: string;
    taken: boolean;
    slot: number;
}

interface AppointmentsTableProps {
    appointments: Appointment[];
}

const AppointmentsTable: React.FC<AppointmentsTableProps> = ({ appointments }) => {
  return (
    <table className="appointments-table">
      <thead>
        <tr>
          <th>نام مشتری</th>
          <th>سرویس</th>
          <th>شروع نوبت</th>
          <th>پایان نوبت</th>
          <th>وضعیت</th>
        </tr>
      </thead>
      <tbody>
        {appointments.map(app => (
          <tr key={app.id}>
            <td>{app.customer_name ? app.customer_name : "بدون رزرو"}</td>
            <td>{app.service ? app.service.name : 'بدون خدمت'}</td>
            <td>{app.app_start}</td>
            <td>{app.app_end}</td>
            <td>{app.taken ? "تایید شده" : "در انتظار تایید"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default AppointmentsTable;