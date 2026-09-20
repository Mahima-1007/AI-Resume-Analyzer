import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import ResumeGenerator from './pages/ResumeGenerator'
import ResumeAnalyzer from './pages/ResumeAnalyzer'
import Jobs from './pages/Jobs'
import TestAwareness from './pages/TestAwareness'
import Applications from './pages/Applications'

function App() {
    return (
        <div className="min-h-screen">
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/generator" element={<ResumeGenerator />} />
                <Route path="/analyzer" element={<ResumeAnalyzer />} />
                <Route path="/jobs" element={<Jobs />} />
                <Route path="/test-awareness" element={<TestAwareness />} />
                <Route path="/applications" element={<Applications />} />
            </Routes>
        </div>
    )
}

export default App
