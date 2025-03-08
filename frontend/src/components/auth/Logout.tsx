import { useNavigate } from 'react-router-dom'

const API: string = "https://nobtic.ir/backend/users/api/token";


const Logout = () => {
    const refreshToken = localStorage.getItem('refreshToken');
    console.log(refreshToken)
    const handleLogout = async(_: { preventDefault: () => void; }) => {
        const response = await fetch(`${API}/blacklist/`, {
            method: 'POST',
            headers: {
                'Content-Type': "application/json",
            },
            body: JSON.stringify({"refresh": refreshToken})
        });
        if (response.ok) {
            localStorage.clear()
            goToHomepage();
        } else {
            alert("Logout failed");
        }
    }

    const navigate = useNavigate();
    const handleRevert = () => {
        navigate(-1);
    }

    const goToHomepage = () => {
        navigate('/');
    }
    
  return (
    <div className='logout-actions'>
        <h2>ایا میخواهید از پنل خود خارج شوید؟</h2>
        <button className='logout-btn' onClick={handleLogout} >Logout</button>
        <button className='cancel-btn' onClick={handleRevert}>Cancel</button>
    </div>
  )
}

export default Logout