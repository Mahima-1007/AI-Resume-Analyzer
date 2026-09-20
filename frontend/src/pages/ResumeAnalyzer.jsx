import React, { useState } from 'react';
import Sidebar from '../components/Sidebar';
import axios from 'axios';
import { Upload, CheckCircle2, AlertCircle, Search } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const API_URL = "http://localhost:8001";

export default function ResumeAnalyzer() {
    const [file, setFile] = useState(null);
    const [jd, setJd] = useState("");
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);

    const navigate = useNavigate();

    const handleAnalyze = async () => {
        if (!file || !jd) return alert("Please upload a resume and paste a job description.");
        setLoading(true);

        const formData = new FormData();
        formData.append("file", file);
        formData.append("jd_text", jd);

        try {
            const response = await axios.post(`${API_URL}/api/analyze`, formData, {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                    "Content-Type": "multipart/form-data"
                }
            });
            setResults(response.data);
        } catch (err) {
            console.error("ANALYSIS HTTP ERROR:", err.response?.data || err.message);
            const errorMsg = err.response?.data?.detail || err.message || "Unknown error";
            alert(`Analysis failed: ${errorMsg}`);
        } finally {
            setLoading(false);
        }
    };

    const handleRegenerate = async () => {
        if (!results) return;
        setLoading(true);
        try {
            const response = await axios.post(`${API_URL}/api/regenerate_resume`, {
                missing_skills: results.missing_skills
            }, {
                headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
            });

            const improvedData = response.data.improved_data;
            alert(response.data.message);
            // Navigate to generator with the improved data pre-filled
            navigate('/generator', { state: { prefillData: improvedData } });

        } catch (err) {
            alert("Failed to regenerate resume.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex bg-slate-50 min-h-screen">
            <Sidebar />
            <main className="flex-1 p-8">
                <h1 className="text-3xl font-bold gradient-text mb-8">ATS Resume Analyzer</h1>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="space-y-6">
                        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                            <h3 className="font-bold mb-4 flex items-center space-x-2">
                                <Upload size={18} /> <span>Upload Resume (PDF/DOCX)</span>
                            </h3>
                            <input
                                type="file"
                                onChange={(e) => setFile(e.target.files[0])}
                                className="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
                            />
                        </div>

                        <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
                            <h3 className="font-bold mb-4">Paste Job Description</h3>
                            <textarea
                                className="w-full p-4 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 h-64"
                                placeholder="Paste the job description here..."
                                value={jd}
                                onChange={(e) => setJd(e.target.value)}
                            />
                            <button
                                onClick={handleAnalyze}
                                disabled={loading}
                                className="w-full mt-4 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition flex items-center justify-center space-x-2 disabled:opacity-50"
                            >
                                {loading ? "Analyzing..." : <><Search size={20} /> <span>Run AI Analysis</span></>}
                            </button>
                        </div>
                    </div>

                    <div>
                        {results ? (
                            <div className="bg-white p-8 rounded-2xl shadow-xl border border-blue-100 space-y-6">
                                <div className="text-center">
                                    <div className="inline-block p-4 rounded-full bg-blue-50 text-blue-600 mb-2 font-bold text-4xl border-4 border-blue-200">
                                        {results.ats_score}%
                                    </div>
                                    <h2 className="text-xl font-bold mb-2">ATS Matching Score</h2>
                                    <div className="w-full bg-slate-200 rounded-full h-2.5">
                                        <div className="bg-blue-600 h-2.5 rounded-full transition-all duration-1000" style={{ width: `${results.ats_score}%` }}></div>
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-4 bg-slate-50 rounded-xl text-center border">
                                        <p className="text-slate-500 text-xs uppercase font-bold">Keyword Match</p>
                                        <p className="text-lg font-bold">{results.keyword_match_percent}%</p>
                                    </div>
                                    <div className="p-4 bg-slate-50 rounded-xl text-center border">
                                        <p className="text-slate-500 text-xs uppercase font-bold">Semantic Similarity</p>
                                        <p className="text-lg font-bold">{results.semantic_similarity}%</p>
                                    </div>
                                </div>

                                {/* Skills Section */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div>
                                        <h4 className="font-bold mb-2 flex items-center space-x-2 text-green-600 text-sm">
                                            <CheckCircle2 size={16} /> <span>Matched Skills</span>
                                        </h4>
                                        <div className="flex flex-wrap gap-1">
                                            {results.matched_skills && results.matched_skills.length > 0 ? results.matched_skills.map(skill => (
                                                <span key={skill} className="px-2 py-1 bg-green-50 text-green-700 rounded text-xs font-medium border border-green-200">
                                                    {skill}
                                                </span>
                                            )) : <span className="text-xs text-slate-400">None found</span>}
                                        </div>
                                    </div>
                                    <div>
                                        <h4 className="font-bold mb-2 flex items-center space-x-2 text-red-600 text-sm">
                                            <AlertCircle size={16} /> <span>Missing Skills</span>
                                        </h4>
                                        <div className="flex flex-wrap gap-1">
                                            {results.missing_skills && results.missing_skills.length > 0 ? results.missing_skills.map(skill => (
                                                <span key={skill} className="px-2 py-1 bg-red-50 text-red-600 rounded text-xs font-medium border border-red-100">
                                                    {skill}
                                                </span>
                                            )) : <span className="text-xs text-slate-400">None missing!</span>}
                                        </div>
                                    </div>
                                </div>

                                {/* Strengths and Weaknesses */}
                                {results.strengths && results.strengths.length > 0 && (
                                    <div className="p-4 bg-emerald-50 rounded-xl border border-emerald-100">
                                        <h4 className="font-bold mb-2 flex items-center space-x-2 text-emerald-800">
                                            <CheckCircle2 size={16} /> <span>Resume Strengths</span>
                                        </h4>
                                        <ul className="list-disc pl-5 text-sm text-emerald-900 space-y-1">
                                            {results.strengths.map((s, i) => <li key={i}>{s}</li>)}
                                        </ul>
                                    </div>
                                )}

                                {results.weaknesses && results.weaknesses.length > 0 && (
                                    <div className="p-4 bg-orange-50 rounded-xl border border-orange-100">
                                        <h4 className="font-bold mb-2 flex items-center space-x-2 text-orange-800">
                                            <AlertCircle size={16} /> <span>Areas for Improvement</span>
                                        </h4>
                                        <ul className="list-disc pl-5 text-sm text-orange-900 space-y-1">
                                            {results.weaknesses.map((w, i) => <li key={i}>{w}</li>)}
                                        </ul>
                                    </div>
                                )}

                                {/* Suggestions */}
                                {results.suggestions && results.suggestions.length > 0 && (
                                    <div className="p-4 bg-blue-50 rounded-xl border border-blue-100">
                                        <h4 className="font-bold mb-2 text-blue-800">💡 Actionable Suggestions</h4>
                                        <ul className="list-disc pl-5 text-sm text-blue-900 space-y-2">
                                            {results.suggestions.map((s, i) => <li key={i}>{s}</li>)}
                                        </ul>
                                    </div>
                                )}

                                {/* AI Regenerate Button */}
                                <button
                                    className="w-full mt-4 py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold rounded-xl hover:shadow-lg transition flex items-center justify-center space-x-2 disabled:opacity-50"
                                    onClick={handleRegenerate}
                                    disabled={loading}
                                >
                                    <span>{loading ? "Regenerating..." : "✨ Auto-Regenerate Improved Resume"}</span>
                                </button>
                            </div>
                        ) : (
                            <div className="bg-slate-100 h-full rounded-2xl border-2 border-dashed border-slate-200 flex flex-col items-center justify-center text-slate-400 p-8 text-center">
                                <Search size={48} className="mb-4 opacity-20" />
                                <p>Upload your resume and paste a JD to see results.</p>
                            </div>
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
