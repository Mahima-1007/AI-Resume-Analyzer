import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from '../components/Sidebar';
import axios from 'axios';
import {
    Brain, Building2, PlayCircle, Clock, ChevronRight,
    ChevronLeft, CheckCircle, XCircle, RotateCcw,
    BookOpen, TrendingUp, Award, AlertCircle, Lightbulb,
    Trophy, Target, BarChart3, Eye, ArrowRight
} from 'lucide-react';

const API_URL = "http://localhost:8001";
const TIMER_SECONDS = 25 * 60; // 25 minutes

const ROLES = [
    { label: "Software Developer",    value: "software developer" },
    { label: "Full Stack Developer",  value: "full stack developer" },
    { label: "Data Analyst",          value: "data analyst" },
    { label: "AI / ML Engineer",      value: "ai/ml engineer" },
    { label: "Cybersecurity Analyst", value: "cybersecurity analyst" },
    { label: "Backend Developer",     value: "backend developer" },
];

const COMPANIES = [
    { label: "Google",    value: "google" },
    { label: "Amazon",    value: "amazon" },
    { label: "Microsoft", value: "microsoft" },
    { label: "Meta",      value: "meta" },
    { label: "TCS",       value: "tcs" },
    { label: "Infosys",   value: "infosys" },
    { label: "General",   value: "general" },
];

const TYPE_COLORS = {
    mcq:        { bg: "bg-blue-100",   text: "text-blue-700",   label: "Technical MCQ" },
    aptitude:   { bg: "bg-orange-100", text: "text-orange-700", label: "Aptitude" },
    logical:    { bg: "bg-purple-100", text: "text-purple-700", label: "Logical Reasoning" },
    behavioural:{ bg: "bg-green-100",  text: "text-green-700",  label: "Behavioural" },
    coding:     { bg: "bg-red-100",    text: "text-red-700",    label: "Coding" },
};

const DIFF_COLORS = {
    easy:   { bg: "bg-green-100",  text: "text-green-700"  },
    medium: { bg: "bg-yellow-100", text: "text-yellow-700" },
    hard:   { bg: "bg-red-100",    text: "text-red-700"    },
};

function formatTime(secs) {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

// ── Setup Screen ──────────────────────────────────────────────────────────────
function SetupScreen({ onStart }) {
    const [role, setRole]       = useState(ROLES[0].value);
    const [company, setCompany] = useState(COMPANIES[0].value);
    const [loading, setLoading] = useState(false);
    const token = localStorage.getItem("token");

    const handleStart = async () => {
        setLoading(true);
        try {
            const res = await axios.post(`${API_URL}/api/mock-test/generate`,
                { role, company, count: 20 },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            if (res.data.success) {
                onStart(res.data.questions, role, company);
            }
        } catch (e) {
            alert("Failed to generate test. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto">
            {/* Hero banner */}
            <div className="relative overflow-hidden bg-gradient-to-br from-violet-600 via-purple-600 to-indigo-700 rounded-3xl p-10 mb-8 text-white">
                <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
                <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />
                <div className="relative">
                    <div className="flex items-center gap-3 mb-4">
                        <div className="w-12 h-12 bg-white/20 rounded-2xl flex items-center justify-center">
                            <Brain size={28} />
                        </div>
                        <div>
                            <p className="text-purple-200 text-sm font-medium">AI-Powered</p>
                            <h1 className="text-2xl font-bold">Mock Interview Test</h1>
                        </div>
                    </div>
                    <p className="text-purple-100 text-sm leading-relaxed mb-6 max-w-md">
                        20 questions · 25 minutes · Tailored to your role & company
                    </p>
                    <div className="flex flex-wrap gap-3">
                        {["Technical MCQ", "Aptitude", "Logical", "Behavioural"].map(t => (
                            <span key={t} className="px-3 py-1 bg-white/15 rounded-full text-xs font-medium">{t}</span>
                        ))}
                    </div>
                </div>
            </div>

            {/* Config card */}
            <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-8 space-y-6">
                <h2 className="text-slate-800 font-bold text-lg">Configure Your Test</h2>

                <div>
                    <label className="flex items-center gap-2 text-sm font-semibold text-slate-600 mb-3">
                        <Target size={16} className="text-violet-500" />
                        Target Job Role
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                        {ROLES.map(r => (
                            <button
                                key={r.value}
                                onClick={() => setRole(r.value)}
                                className={`px-4 py-3 rounded-xl text-sm font-medium text-left transition-all ${
                                    role === r.value
                                        ? "bg-violet-600 text-white shadow-lg shadow-violet-200"
                                        : "bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200"
                                }`}
                            >
                                {r.label}
                            </button>
                        ))}
                    </div>
                </div>

                <div>
                    <label className="flex items-center gap-2 text-sm font-semibold text-slate-600 mb-3">
                        <Building2 size={16} className="text-violet-500" />
                        Target Company
                    </label>
                    <div className="grid grid-cols-3 sm:grid-cols-4 gap-2">
                        {COMPANIES.map(c => (
                            <button
                                key={c.value}
                                onClick={() => setCompany(c.value)}
                                className={`px-3 py-2 rounded-xl text-sm font-medium transition-all ${
                                    company === c.value
                                        ? "bg-indigo-600 text-white shadow-lg shadow-indigo-200"
                                        : "bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200"
                                }`}
                            >
                                {c.label}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-50 rounded-2xl p-4 text-sm text-slate-600 space-y-1">
                    <p>📋 <strong>20 questions</strong> — Mixed difficulty & types</p>
                    <p>⏱️ <strong>25 minute timer</strong> — Auto-submits on timeout</p>
                    <p>📊 <strong>Detailed results</strong> — Score, explanations & skill gaps</p>
                </div>

                <button
                    onClick={handleStart}
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-3 bg-gradient-to-r from-violet-600 to-indigo-600 text-white py-4 rounded-2xl font-bold text-base hover:from-violet-700 hover:to-indigo-700 transition-all shadow-lg shadow-violet-200 disabled:opacity-60"
                >
                    <PlayCircle size={22} />
                    {loading ? "Generating Test..." : "Start Mock Test"}
                </button>
            </div>
        </div>
    );
}

// ── Testing Screen ────────────────────────────────────────────────────────────
function TestingScreen({ questions, role, company, onSubmit }) {
    const [current, setCurrent]   = useState(0);
    const [selected, setSelected] = useState({});  // { qId: answerIndex }
    const [timeLeft, setTimeLeft] = useState(TIMER_SECONDS);

    // Timer
    const handleSubmit = useCallback(() => {
        onSubmit(selected, questions);
    }, [selected, questions, onSubmit]);

    useEffect(() => {
        const interval = setInterval(() => {
            setTimeLeft(t => {
                if (t <= 1) { clearInterval(interval); handleSubmit(); return 0; }
                return t - 1;
            });
        }, 1000);
        return () => clearInterval(interval);
    }, [handleSubmit]);

    const q = questions[current];
    const answered = Object.keys(selected).length;
    const progress = (answered / questions.length) * 100;
    const timerWarning = timeLeft < 300;

    const pickAnswer = (idx) => setSelected(prev => ({ ...prev, [q.id]: idx }));

    return (
        <div className="max-w-2xl mx-auto">
            {/* Header bar */}
            <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-4 mb-6 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-violet-100 rounded-xl flex items-center justify-center">
                        <Brain size={18} className="text-violet-600" />
                    </div>
                    <div>
                        <p className="text-xs text-slate-500">Mock Test</p>
                        <p className="text-sm font-semibold text-slate-700 capitalize">{role} · {company}</p>
                    </div>
                </div>
                <div className={`flex items-center gap-2 px-4 py-2 rounded-xl font-mono font-bold text-lg ${
                    timerWarning ? "bg-red-100 text-red-600 animate-pulse" : "bg-slate-100 text-slate-700"
                }`}>
                    <Clock size={18} />
                    {formatTime(timeLeft)}
                </div>
            </div>

            {/* Progress */}
            <div className="mb-4">
                <div className="flex justify-between text-xs text-slate-500 mb-1">
                    <span>Question {current + 1} of {questions.length}</span>
                    <span>{answered} answered</span>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2">
                    <div
                        className="bg-gradient-to-r from-violet-500 to-indigo-500 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${((current + 1) / questions.length) * 100}%` }}
                    />
                </div>
            </div>

            {/* Question card */}
            <div className="bg-white rounded-3xl border border-slate-100 shadow-sm p-8 mb-6">
                <div className="flex items-center gap-2 mb-4">
                    {q.type && (
                        <span className={`px-2 py-0.5 rounded-lg text-xs font-bold ${TYPE_COLORS[q.type]?.bg || 'bg-slate-100'} ${TYPE_COLORS[q.type]?.text || 'text-slate-600'}`}>
                            {TYPE_COLORS[q.type]?.label || q.type}
                        </span>
                    )}
                    <span className={`px-2 py-0.5 rounded-lg text-xs font-bold ${DIFF_COLORS[q.difficulty]?.bg || 'bg-slate-100'} ${DIFF_COLORS[q.difficulty]?.text || 'text-slate-600'}`}>
                        {q.difficulty}
                    </span>
                </div>

                <h2 className="text-slate-800 font-semibold text-base leading-relaxed mb-6">{q.question}</h2>

                <div className="space-y-3">
                    {q.options.map((opt, idx) => {
                        const isSelected = selected[q.id] === idx;
                        return (
                            <button
                                key={idx}
                                onClick={() => pickAnswer(idx)}
                                className={`w-full text-left p-4 rounded-2xl border-2 transition-all text-sm font-medium flex items-center gap-3 ${
                                    isSelected
                                        ? "border-violet-500 bg-violet-50 text-violet-800"
                                        : "border-slate-100 hover:border-slate-300 bg-slate-50 text-slate-700 hover:bg-white"
                                }`}
                            >
                                <div className={`w-6 h-6 rounded-full border-2 font-bold text-xs flex items-center justify-center shrink-0 ${
                                    isSelected ? "border-violet-500 bg-violet-500 text-white" : "border-slate-300 text-slate-500"
                                }`}>
                                    {String.fromCharCode(65 + idx)}
                                </div>
                                {opt}
                            </button>
                        );
                    })}
                </div>
            </div>

            {/* Nav buttons */}
            <div className="flex gap-3">
                <button
                    onClick={() => setCurrent(c => Math.max(0, c - 1))}
                    disabled={current === 0}
                    className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl border border-slate-200 text-slate-600 font-semibold hover:bg-slate-50 transition disabled:opacity-40"
                >
                    <ChevronLeft size={18} /> Previous
                </button>

                {current < questions.length - 1 ? (
                    <button
                        onClick={() => setCurrent(c => c + 1)}
                        className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-violet-600 text-white font-semibold hover:bg-violet-700 transition"
                    >
                        Next <ChevronRight size={18} />
                    </button>
                ) : (
                    <button
                        onClick={handleSubmit}
                        className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-600 text-white font-bold hover:from-green-600 hover:to-emerald-700 transition shadow-lg"
                    >
                        <CheckCircle size={18} /> Submit Test
                    </button>
                )}
            </div>

            {/* Quick question navigator */}
            <div className="mt-6 bg-white rounded-2xl border border-slate-100 p-4">
                <p className="text-xs text-slate-500 mb-3 font-medium">Jump to question</p>
                <div className="flex flex-wrap gap-2">
                    {questions.map((ques, i) => (
                        <button
                            key={i}
                            onClick={() => setCurrent(i)}
                            className={`w-8 h-8 rounded-lg text-xs font-bold transition-all ${
                                i === current
                                    ? "bg-violet-600 text-white"
                                    : selected[ques.id] !== undefined
                                        ? "bg-green-100 text-green-700 border border-green-200"
                                        : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                            }`}
                        >
                            {i + 1}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

// ── Results Screen ────────────────────────────────────────────────────────────
function ResultsScreen({ results, onRetake, onReview }) {
    const { score, total, percentage, grade, breakdown, suggestions } = results;

    const gradeColor = percentage >= 75 ? "text-green-600" : percentage >= 50 ? "text-yellow-600" : "text-red-500";
    const gradeRing  = percentage >= 75 ? "border-green-400" : percentage >= 50 ? "border-yellow-400" : "border-red-400";

    return (
        <div className="max-w-2xl mx-auto">
            {/* Score card */}
            <div className="bg-gradient-to-br from-violet-600 to-indigo-700 rounded-3xl p-8 mb-6 text-white text-center">
                <Trophy size={40} className="mx-auto mb-3 text-yellow-300" />
                <h1 className="text-2xl font-bold mb-1">Test Complete!</h1>
                <p className="text-purple-200 text-sm mb-6">Here's how you performed</p>

                <div className={`w-32 h-32 mx-auto rounded-full border-8 ${gradeRing} bg-white/10 flex flex-col items-center justify-center mb-4`}>
                    <span className={`text-4xl font-black ${gradeColor}`}>{percentage}%</span>
                </div>
                <p className="text-lg font-bold">{grade}</p>
                <p className="text-purple-200 text-sm mt-1">{score} / {total} correct</p>
            </div>

            {/* Difficulty breakdown */}
            <div className="grid grid-cols-3 gap-4 mb-6">
                {[
                    { label: "Easy",   data: breakdown.easy,   color: "text-green-600",  bg: "bg-green-50",  border: "border-green-200" },
                    { label: "Medium", data: breakdown.medium, color: "text-yellow-600", bg: "bg-yellow-50", border: "border-yellow-200" },
                    { label: "Hard",   data: breakdown.hard,   color: "text-red-600",    bg: "bg-red-50",    border: "border-red-200"   },
                ].map(({ label, data, color, bg, border }) => (
                    <div key={label} className={`${bg} ${border} border rounded-2xl p-4 text-center`}>
                        <p className={`text-2xl font-black ${color}`}>
                            {data.total > 0 ? `${Math.round((data.correct / data.total) * 100)}%` : "–"}
                        </p>
                        <p className="text-xs text-slate-600 font-medium mt-1">{label}</p>
                        <p className="text-xs text-slate-500">{data.correct}/{data.total}</p>
                    </div>
                ))}
            </div>

            {/* Suggestions */}
            {suggestions && suggestions.length > 0 && (
                <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 mb-6">
                    <h3 className="flex items-center gap-2 text-amber-800 font-bold text-sm mb-3">
                        <Lightbulb size={16} className="text-amber-500" /> Skill Improvement Suggestions
                    </h3>
                    <ul className="space-y-2">
                        {suggestions.map((s, i) => (
                            <li key={i} className="flex items-start gap-2 text-amber-900 text-sm">
                                <span className="text-amber-500 mt-0.5">•</span> {s}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Action buttons */}
            <div className="flex gap-4">
                <button
                    onClick={onRetake}
                    className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl border border-violet-300 text-violet-700 font-semibold hover:bg-violet-50 transition"
                >
                    <RotateCcw size={18} /> Retake Test
                </button>
                <button
                    onClick={onReview}
                    className="flex-1 flex items-center justify-center gap-2 py-3 rounded-2xl bg-violet-600 text-white font-semibold hover:bg-violet-700 transition"
                >
                    <Eye size={18} /> Review Answers
                </button>
            </div>
        </div>
    );
}

// ── Review Screen ─────────────────────────────────────────────────────────────
function ReviewScreen({ results, onRetake }) {
    const { results: qs } = results;
    return (
        <div className="max-w-2xl mx-auto">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-slate-800">Answer Review</h2>
                <button
                    onClick={onRetake}
                    className="flex items-center gap-2 px-4 py-2 rounded-xl bg-violet-600 text-white text-sm font-semibold hover:bg-violet-700 transition"
                >
                    <RotateCcw size={16} /> New Test
                </button>
            </div>

            <div className="space-y-5">
                {qs.map((q, i) => (
                    <div
                        key={q.id}
                        className={`bg-white rounded-2xl border-2 p-6 ${q.isCorrect ? "border-green-200" : "border-red-200"}`}
                    >
                        {/* Header */}
                        <div className="flex items-start justify-between gap-3 mb-3">
                            <div className="flex items-center gap-2">
                                <span className="text-slate-400 text-xs font-bold">Q{i + 1}</span>
                                {q.type && (
                                    <span className={`px-2 py-0.5 rounded-lg text-xs font-bold ${TYPE_COLORS[q.type]?.bg} ${TYPE_COLORS[q.type]?.text}`}>
                                        {TYPE_COLORS[q.type]?.label}
                                    </span>
                                )}
                            </div>
                            {q.isCorrect
                                ? <CheckCircle size={20} className="text-green-500 shrink-0" />
                                : <XCircle size={20} className="text-red-500 shrink-0" />
                            }
                        </div>

                        <p className="text-slate-800 font-medium text-sm mb-4 leading-relaxed">{q.question}</p>

                        {/* Options */}
                        <div className="space-y-2 mb-4">
                            {q.options.map((opt, idx) => {
                                const isCorrectOpt = idx === q.correctAnswer;
                                const isUserOpt    = idx === q.userAnswer;
                                let cls = "border-slate-100 bg-slate-50 text-slate-600";
                                if (isCorrectOpt) cls = "border-green-400 bg-green-50 text-green-800 font-semibold";
                                else if (isUserOpt && !isCorrectOpt) cls = "border-red-300 bg-red-50 text-red-700";
                                return (
                                    <div key={idx} className={`px-4 py-3 rounded-xl border-2 text-sm flex items-center gap-2 ${cls}`}>
                                        <span className="font-bold text-xs">{String.fromCharCode(65 + idx)}.</span>
                                        <span>{opt}</span>
                                        {isCorrectOpt && <CheckCircle size={14} className="ml-auto text-green-500" />}
                                        {isUserOpt && !isCorrectOpt && <XCircle size={14} className="ml-auto text-red-500" />}
                                    </div>
                                );
                            })}
                        </div>

                        {/* Explanation */}
                        <div className="bg-blue-50 border border-blue-100 rounded-xl p-3">
                            <p className="text-blue-800 text-xs font-semibold flex items-center gap-1 mb-1">
                                <BookOpen size={12} /> Explanation
                            </p>
                            <p className="text-blue-900 text-sm">{q.explanation}</p>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

// ── Main Component ────────────────────────────────────────────────────────────
export default function TestAwareness() {
    const [stage, setStage]         = useState("setup");   // setup | testing | results | review
    const [questions, setQuestions] = useState([]);
    const [role, setRole]           = useState("");
    const [company, setCompany]     = useState("");
    const [results, setResults]     = useState(null);
    const token = localStorage.getItem("token");

    const handleStart = (qs, r, c) => {
        setQuestions(qs);
        setRole(r);
        setCompany(c);
        setStage("testing");
    };

    const handleSubmit = async (answers, qs) => {
        try {
            const res = await axios.post(
                `${API_URL}/api/mock-test/submit`,
                { answers },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            if (res.data.success) {
                setResults(res.data);
                setStage("results");
            }
        } catch (e) {
            alert("Failed to submit test. Please try again.");
        }
    };

    const handleRetake = () => {
        setStage("setup");
        setQuestions([]);
        setResults(null);
    };

    return (
        <div className="flex bg-slate-50 min-h-screen">
            <Sidebar />
            <main className="flex-1 p-6 lg:p-8 overflow-auto">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
                        Mock Interview Test
                    </h1>
                    <p className="text-slate-500 text-sm mt-1">
                        AI-powered aptitude & technical assessment tailored to your role
                    </p>

                    {/* Stage indicator */}
                    <div className="flex items-center gap-2 mt-4">
                        {["Setup", "Test", "Results", "Review"].map((s, i) => {
                            const stageOrder = ["setup", "testing", "results", "review"];
                            const done = stageOrder.indexOf(stage) > i;
                            const active = stageOrder[i] === stage;
                            return (
                                <React.Fragment key={s}>
                                    <div className={`px-3 py-1 rounded-full text-xs font-semibold ${
                                        active ? "bg-violet-600 text-white"
                                        : done  ? "bg-green-100 text-green-700"
                                        :         "bg-slate-100 text-slate-400"
                                    }`}>
                                        {done && "✓ "}{s}
                                    </div>
                                    {i < 3 && <ArrowRight size={12} className="text-slate-300" />}
                                </React.Fragment>
                            );
                        })}
                    </div>
                </div>

                {stage === "setup"   && <SetupScreen onStart={handleStart} />}
                {stage === "testing" && <TestingScreen questions={questions} role={role} company={company} onSubmit={handleSubmit} />}
                {stage === "results" && results && <ResultsScreen results={results} onRetake={handleRetake} onReview={() => setStage("review")} />}
                {stage === "review"  && results && <ReviewScreen results={results} onRetake={handleRetake} />}
            </main>
        </div>
    );
}
