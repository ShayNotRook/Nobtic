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
        <div className="user-card">
            <h3 className='user-card-header'>کاربر {user.username}</h3>
            <p><strong>{user.first_name} {user.last_name}</strong> به پنل کاربری خوش امدید!</p>
        </div>
    )
}

export default UserCard