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
          <Route path='' element={<Home />} />
        </Routes>
        <Footer />
      </div>
    </Router>
  )
}

export default App
