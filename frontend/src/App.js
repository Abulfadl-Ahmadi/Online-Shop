// import logo from './logo.svg';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './App.css';
import Login from './components/Login';
import Register from './components/Register';
import UserProfile from './components/UserProfile';

function App() {
  return (
    <div className="App">
      <Router>
        <div>
        <Routes>
          <Route path='/login' element={<Login/>} />
          <Route path='/profile' element={<UserProfile/>} />
          <Route path='/register' element={<Register/>} />
        </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
