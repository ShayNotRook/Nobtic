import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import './App.css';

import Header from './components/main/partials/Header';
import Footer from './components/main/partials/Footer';
import Home from './components/main/Home/Home';


function App() {
  return (
    <Router>
      <div className='App'>
        <Header />
        <Routes>
          <Route path='dashboard/' element={<Home />} />
          {/* <Route path='apps/' element={}></Route> */}
        </Routes>
        <Footer />
      </div>
    </Router>
  )
}

export default App
