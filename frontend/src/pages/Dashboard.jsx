import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import axios from 'axios';
import { User, FileCheck, Briefcase, Zap } from 'lucide-react';

const API_URL = "http://localhost:8001";

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [stats, setStats] = useState({ resumes: 0, applications: 0, avgScore: 0 });

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem("token");
            if (!token) return;

            try {
                const userRes = await axios.get(`${API_URL}/auth/me`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setUser(userRes.data);

                const appRes = await axios.get(`${API_URL}/api/applications`, {
                    headers: { Authorization: `Bearer ${token}` }
                });

                setStats({
                    resumes: 1, // Mock or fetch actual
                    applications: appRes.data.length,
                    avgScore: 85
                });
            } catch (err) {
                console.error(err);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="flex bg-slate-50 min-h-screen">
            <Sidebar />
            <main className="flex-1 p-8">
                <header className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-2xl font-bold text-slate-800">Welcome back, {user?.full_name || 'Student'}!</h1>
                        <p className="text-slate-500">Here's what's happening with your job search today.</p>
                    </div>
                    <div className="flex items-center space-x-4 bg-white p-2 rounded-full shadow-sm pr-4">
                        <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
                            {user?.full_name?.charAt(0) || 'S'}
                        </div>
                        <span className="font-medium text-slate-700">{user?.full_name}</span>
                    </div>
                </header>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <StatCard icon={<FileCheck className="text-blue-600" />} label="Resumes Analyzed" value={stats.resumes} color="bg-blue-50" />
                    <StatCard icon={<Briefcase className="text-purple-600" />} label="Jobs Applied" value={stats.applications} color="bg-purple-50" />
                    <StatCard icon={<Zap className="text-yellow-600" />} label="Average ATS Score" value={`${stats.avgScore}%`} color="bg-yellow-50" />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                        <h3 className="text-lg font-bold mb-4">Quick Actions</h3>
                        <div className="space-y-3">
                            <ActionButton label="Analyze New Resume" description="Check ATS compatibility for a job." />
                            <ActionButton label="Generate Resume" description="Create a professional PDF in minutes." />
                            <ActionButton label="Explore Job Matches" description="See roles fitting your profile." />
                        </div>
                    </div>

                    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                        <h3 className="text-lg font-bold mb-4">Upcoming Assessments</h3>
                        <p className="text-slate-500 text-sm">No assessments scheduled yet. Apply to jobs to see them here!</p>
                    </div>
                </div>
            </main>
        </div>
    );
}

function StatCard({ icon, label, value, color }) {
    return (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex items-center space-x-4">
            <div className={`w-12 h-12 ${color} rounded-xl flex items-center justify-center`}>
                {icon}
            </div>
            <div>
                <p className="text-slate-500 text-sm">{label}</p>
                <p className="text-2xl font-bold text-slate-800">{value}</p>
            </div>
        </div>
    );
}

function ActionButton({ label, description }) {
    return (
        <button className="w-full text-left p-4 rounded-xl border border-slate-100 hover:border-blue-200 hover:bg-blue-50/30 transition group">
            <p className="font-semibold text-slate-700 group-hover:text-blue-600">{label}</p>
            <p className="text-xs text-slate-400">{description}</p>
        </button>
    );
}
