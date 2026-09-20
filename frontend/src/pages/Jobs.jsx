import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import axios from 'axios';
import { Briefcase, MapPin, ExternalLink, Search, AlertCircle, Loader2, CheckCircle } from 'lucide-react';

const API_URL = "http://localhost:8001";

const SUGGESTED_ROLES = [
    "Software Developer",
    "Java Developer",
    "Python Developer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "React Developer",
    "Machine Learning Engineer",
    "Data Scientist",
    "DevOps Engineer",
    "Android Developer",
    "Node.js Developer",
];

export default function Jobs() {
    const [role, setRole] = useState("");
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [searchedRole, setSearchedRole] = useState("");

    const handleSearch = async (searchRole) => {
        const roleToSearch = (searchRole || role).trim();
        if (!roleToSearch) {
            setError("Please enter a job role to search.");
            return;
        }

        setLoading(true);
        setError(null);
        setJobs([]);
        setSearchedRole(roleToSearch);

        const token = localStorage.getItem("token");
        if (!token) {
            setError("You are not logged in. Please log in first.");
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post(
                `${API_URL}/api/jobs/search`,
                { role: roleToSearch },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            const data = response.data;
            const jobList = data?.jobs ?? [];
            setJobs(jobList);

            if (jobList.length === 0) {
                setError(`No jobs found for "${roleToSearch}". Try a different role or a broader term.`);
            }
        } catch (err) {
            console.error("Job search error:", err);
            if (err.response?.status === 401) {
                setError("Session expired. Please log out and log in again.");
            } else if (!err.response) {
                setError("Cannot connect to server. Make sure the backend is running on port 8001.");
            } else {
                setError(err.response?.data?.detail || `Error ${err.response?.status}: Failed to fetch jobs.`);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") handleSearch();
    };

    return (
        <div className="flex bg-slate-50 min-h-screen">
            <Sidebar />
            <main className="flex-1 p-8">

                {/* Header */}
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-slate-800">Job Recommendations</h1>
                    <p className="text-slate-500 mt-1">Search real-time jobs from Arbeitnow & Remotive by entering your desired job role.</p>
                </div>

                {/* Search Box */}
                <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 mb-8 max-w-2xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-32 h-32 bg-blue-50 rounded-bl-full -z-10 opacity-70"></div>
                    <h2 className="text-xl font-bold mb-1 text-slate-800">Enter Job Role</h2>
                    <p className="text-slate-500 text-sm mb-5">We'll search real-time job boards for openings matching your role.</p>

                    <div className="flex gap-3">
                        <input
                            type="text"
                            placeholder='e.g. "Java Developer", "Python Developer"'
                            value={role}
                            onChange={(e) => setRole(e.target.value)}
                            onKeyDown={handleKeyDown}
                            className="flex-1 px-4 py-3 rounded-xl border border-slate-200 text-slate-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm font-medium"
                        />
                        <button
                            onClick={() => handleSearch()}
                            disabled={loading}
                            className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-xl font-bold hover:bg-blue-700 transition disabled:opacity-60 shadow-sm"
                        >
                            {loading ? <Loader2 className="animate-spin" size={18} /> : <Search size={18} />}
                            <span>{loading ? "Searching..." : "Search Jobs"}</span>
                        </button>
                    </div>

                    {/* Suggested Roles */}
                    <div className="mt-4">
                        <p className="text-xs text-slate-400 font-semibold uppercase tracking-wide mb-2">Popular Roles</p>
                        <div className="flex flex-wrap gap-2">
                            {SUGGESTED_ROLES.map((r) => (
                                <button
                                    key={r}
                                    onClick={() => { setRole(r); handleSearch(r); }}
                                    className="px-3 py-1.5 bg-slate-50 border border-slate-200 text-slate-600 text-xs font-semibold rounded-lg hover:bg-blue-50 hover:border-blue-200 hover:text-blue-700 transition"
                                >
                                    {r}
                                </button>
                            ))}
                        </div>
                    </div>

                    {/* Error */}
                    {error && (
                        <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-xl flex items-center space-x-2 text-sm font-medium border border-red-100">
                            <AlertCircle size={18} />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Success count */}
                    {!loading && jobs.length > 0 && (
                        <div className="mt-3 p-3 bg-green-50 text-green-700 rounded-xl flex items-center space-x-2 text-sm font-medium border border-green-100">
                            <CheckCircle size={16} />
                            <span>{jobs.length} jobs found for <strong>"{searchedRole}"</strong></span>
                        </div>
                    )}
                </div>

                {/* Loading Spinner */}
                {loading && (
                    <div className="flex flex-col items-center justify-center p-16 bg-white rounded-2xl border border-blue-100 shadow-sm border-dashed">
                        <Loader2 className="animate-spin text-blue-600 mb-6" size={48} />
                        <p className="text-slate-800 font-bold text-lg mb-2">Searching jobs for "{searchedRole}"...</p>
                        <p className="text-slate-500 text-sm mt-2 text-center max-w-md">Fetching live job listings. This may take a few seconds.</p>
                    </div>
                )}

                {/* Job Cards */}
                {!loading && jobs.length > 0 && (
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        {jobs.map((job) => (
                            <div
                                key={job.id}
                                className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 hover:shadow-lg hover:border-blue-100 transition-all duration-300 transform hover:-translate-y-1"
                            >
                                <div className="flex justify-between items-start mb-3">
                                    <div>
                                        <h3 className="text-lg font-bold text-slate-800 mb-1">{job.jobTitle}</h3>
                                        <p className="text-slate-600 font-semibold text-sm">{job.company}</p>
                                    </div>
                                    {job.score && (
                                        <div className={`px-3 py-1 rounded-full text-xs font-bold shrink-0 ml-2 ${job.score >= 70 ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-600'}`}>
                                            {job.score}% Match
                                        </div>
                                    )}
                                </div>

                                <div className="flex items-center gap-2 text-slate-500 text-sm mb-4">
                                    <MapPin size={14} className="text-slate-400 flex-shrink-0" />
                                    <span>{job.location}</span>
                                </div>

                                {job.skills && job.skills.length > 0 && (
                                    <div className="flex flex-wrap gap-2 mb-4">
                                        {job.skills.map((skill, idx) => (
                                            <span key={idx} className="px-2.5 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs font-bold border border-blue-100">
                                                {skill}
                                            </span>
                                        ))}
                                    </div>
                                )}

                                {job.jobDescription && (
                                    <p className="text-slate-500 text-sm mb-4 line-clamp-2">{job.jobDescription}</p>
                                )}

                                <div className="pt-4 border-t border-slate-50">
                                    <button
                                        onClick={() => {
                                            if (job.applyUrl) {
                                                window.open(job.applyUrl, "_blank");
                                            } else {
                                                alert("Apply link is not available for this job.");
                                            }
                                        }}
                                        className="w-full flex justify-center items-center gap-2 py-3 bg-slate-800 text-white font-bold rounded-xl hover:bg-black transition-colors"
                                    >
                                        <span>Apply Now</span>
                                        <ExternalLink size={15} />
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Empty State */}
                {!loading && jobs.length === 0 && !error && (
                    <div className="bg-white p-16 rounded-2xl text-center border-2 border-dashed border-slate-100">
                        <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
                            <Briefcase size={32} className="text-slate-400" />
                        </div>
                        <h3 className="text-xl font-bold text-slate-700 mb-2">Search for Jobs</h3>
                        <p className="text-slate-500 max-w-sm mx-auto">Enter a job role above or click one of the popular roles to find real-time openings.</p>
                    </div>
                )}

            </main>
        </div>
    );
}
