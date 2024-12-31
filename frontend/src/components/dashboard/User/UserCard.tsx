import { useState, useEffect } from 'react';

import './usercard.css';

interface User {
    id: number,
    username: string,
    email: string,
    first_name: string,
    last_name: string,
}

const API: string = "http://localhost:8000/users/api/" 


const UserCard: React.FC<{ token: string, className?: string }> = ({ token, className }) => {
    const [user, setUser] = useState<User | null>(null);

    useEffect(() => {
        fetch(`${API}user/detail/`, {
            headers: {
                "Authorization": `Bearer ${token}`,
            }
        })
            .then(response => response.json())
            .then(data => setUser(data))
            .catch(error => console.error("Error fetching user data: ", error))
    }, [token])
    
    if (!user) {
        return <div className={`loading ${className}`}>Loading...</div>
    }
    return (
        <div className={`user-card-${className}`}>
            <h3 className='user-card-header'>اطلاعات کاربر</h3>
            <p><strong>نام کاربری:</strong> {user.username}</p>
            <p><strong>نام:</strong> {user.first_name}</p>
            <p><strong>نام خانوادگی:</strong> {user.last_name}</p>
            <p><strong>ایمیل:</strong> {user.email}</p>
        </div>
    )
}

export default UserCard