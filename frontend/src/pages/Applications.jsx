import React, { useEffect, useState } from 'react';
import Sidebar from '../components/Sidebar';
import axios from 'axios';
import { Clock, CheckCircle2, ChevronRight } from 'lucide-react';

const API_URL = "http://localhost:8001";

export default function Applications() {
    const [apps, setApps] = useState([]);

    useEffect(() => {
        const fetchApps = async () => {
            try {
                const response = await axios.get(`${API_URL}/api/applications`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
                });
                setApps(response.data);
            } catch (err) {
                console.error(err);
            }
        };
        fetchApps();
    }, []);

    return (
        <div className="flex bg-slate-50 min-h-screen">
            <Sidebar />
            <main className="flex-1 p-8">
                <h1 className="text-3xl font-bold gradient-text mb-8">My Mock Applications</h1>

                <div className="bg-white rounded-2xl shadow-sm border border-slate-100 overflow-hidden">
                    <table className="w-full text-left">
                        <thead className="bg-slate-50 border-b border-slate-100">
                            <tr>
                                <th className="px-6 py-4 text-sm font-bold text-slate-600 uppercase">Job ID</th>
                                <th className="px-6 py-4 text-sm font-bold text-slate-600 uppercase">Status</th>
                                <th className="px-6 py-4 text-sm font-bold text-slate-600 uppercase">Applied Date</th>
                                <th className="px-6 py-4 text-sm font-bold text-slate-600 uppercase"></th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {apps.length > 0 ? apps.map((app) => (
                                <tr key={app.id} className="hover:bg-slate-50 transition">
                                    <td className="px-6 py-4 font-semibold text-slate-800">#{app.job_id}</td>
                                    <td className="px-6 py-4">
                                        <span className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-bold ${app.status === 'Applied' ? 'bg-blue-50 text-blue-600' : 'bg-green-50 text-green-600'
                                            }`}>
                                            <Clock size={12} />
                                            <span>{app.status}</span>
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-slate-500">{new Date(app.applied_at).toLocaleDateString()}</td>
                                    <td className="px-6 py-4 text-right">
                                        <button className="text-slate-300 hover:text-blue-600"><ChevronRight /></button>
                                    </td>
                                </tr>
                            )) : (
                                <tr>
                                    <td colSpan="4" className="px-6 py-12 text-center text-slate-400">No applications yet. Go to Job Recommendations to apply!</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </main>
        </div>
    );
}
