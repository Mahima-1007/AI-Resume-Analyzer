import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { LayoutDashboard, FileText, Search, Briefcase, Info, LogOut, ClipboardList } from 'lucide-react';

export default function Sidebar() {
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const navItems = [
        { icon: <LayoutDashboard size={20} />, label: "Dashboard", path: "/dashboard" },
        { icon: <FileText size={20} />, label: "Resume Generator", path: "/generator" },
        { icon: <Search size={20} />, label: "Resume Analyzer", path: "/analyzer" },
        { icon: <Briefcase size={20} />, label: "Job Recommendations", path: "/jobs" },
        { icon: <Info size={20} />, label: "Test Awareness", path: "/test-awareness" },
        { icon: <ClipboardList size={20} />, label: "My Applications", path: "/applications" },
    ];

    return (
        <div className="w-64 min-h-screen bg-white border-r border-slate-200 flex flex-col p-4 shadow-sm">
            <div className="mb-10 text-center">
                <h1 className="text-xl font-bold gradient-text">AI Resume Pro</h1>
            </div>
            <nav className="flex-1 space-y-2">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center space-x-3 px-4 py-3 rounded-xl transition duration-200 ${isActive
                                ? "bg-blue-600 text-white shadow-md"
                                : "text-slate-600 hover:bg-slate-100"
                            }`
                        }
                    >
                        {item.icon}
                        <span className="font-medium">{item.label}</span>
                    </NavLink>
                ))}
            </nav>
            <button
                onClick={handleLogout}
                className="flex items-center space-x-3 px-4 py-3 text-red-500 hover:bg-red-50 rounded-xl transition duration-200 mt-auto"
            >
                <LogOut size={20} />
                <span className="font-medium">Logout</span>
            </button>
        </div>
    );
}
