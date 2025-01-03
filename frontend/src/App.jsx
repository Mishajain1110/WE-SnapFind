import React from "react"
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom"
import Navbar from "./components/Navbar"
import NotFound from "./pages/NotFound"
import Home from "./pages/Home"
import AuthPage from "./pages/AuthPage"
import { useAuthentication } from "./auth"
import RedirectGoogleAuth from "./components/GoogleRedirectHandler"
import LostFoundForm from './components/LostFoundForm';
import FoundItemsList from './components/FoundItemsList';

function App() {

  const {isAuthorized} = useAuthentication()
  const ProtectedLogin = () => {
    return isAuthorized ? <Navigate to='/' /> : <AuthPage initialMethod='login' />
  }
  const ProtectedRegister = () => {
    return isAuthorized ? <Navigate to='/' /> : <AuthPage initialMethod='register' />
  }
 

  return (
    <div>
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/login/callback" element={<RedirectGoogleAuth />} />
          <Route path="/login" element={<ProtectedLogin />}/>
          <Route path="/register" element={<ProtectedRegister />}/>
          <Route path="/" element={<Home />} />
          <Route path="*" element={<NotFound/>} />
          <Route path="/lost-found" element={<LostFoundForm />} />
          <Route path="/lost-found/list" element={<FoundItemsList />} />
          <Route path="/found-items" element={<FoundItemsList />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
