import React from 'react';
import { useNavigate, Link } from 'react-router-dom';

export default function Home() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
            {/* Navbar */}
            <nav className="flex justify-between items-center px-10 py-5">
                <h1 className="text-2xl font-extrabold gradient-text">AI Resume Pro</h1>
                <div className="flex items-center gap-4">
                    <Link to="/login" className="font-semibold text-slate-600 hover:text-blue-600 transition">Login</Link>
                    <Link to="/signup" className="px-5 py-2 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition shadow">Sign Up</Link>
                </div>
            </nav>

            {/* Hero Section */}
            <div className="flex flex-col items-center justify-center py-32 px-6 text-center">
                <span className="mb-4 px-4 py-1 bg-blue-100 text-blue-700 text-sm font-bold rounded-full uppercase tracking-widest">AI + NLP Powered</span>
                <h1 className="text-6xl font-extrabold gradient-text mb-6 leading-tight max-w-3xl">
                    Automated Resume & Job Matching
                </h1>
                <p className="text-xl text-slate-500 mb-10 max-w-2xl">
                    Generate ATS-optimized resumes, analyze compatibility with any job description, and discover your perfect job matches — all powered by AI.
                </p>
                <div className="flex gap-4">
                    <button
                        onClick={() => navigate('/signup')}
                        className="px-8 py-4 bg-blue-600 text-white font-bold text-lg rounded-xl hover:bg-blue-700 transition shadow-xl"
                    >
                        Get Started Free
                    </button>
                    <button
                        onClick={() => navigate('/login')}
                        className="px-8 py-4 bg-white text-blue-600 font-bold text-lg rounded-xl border border-blue-200 hover:bg-blue-50 transition shadow"
                    >
                        Login
                    </button>
                </div>
            </div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto px-6 pb-24">
                {[
                    { emoji: "📄", title: "Resume Generator", desc: "Build a professional, ATS-compliant resume in minutes." },
                    { emoji: "🎯", title: "ATS Score Analyzer", desc: "Match your resume against any job description instantly." },
                    { emoji: "💼", title: "Job Recommendations", desc: "AI-powered job matches based on your exact skillset." },
                ].map(card => (
                    <div key={card.title} className="glass p-8 rounded-2xl text-center hover:shadow-2xl transition-all duration-300">
                        <div className="text-4xl mb-4">{card.emoji}</div>
                        <h3 className="text-xl font-bold mb-2">{card.title}</h3>
                        <p className="text-slate-500">{card.desc}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
