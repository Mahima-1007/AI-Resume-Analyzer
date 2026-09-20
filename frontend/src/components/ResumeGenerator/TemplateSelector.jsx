import React from 'react';

const templates = [
    { id: "modern", name: "Modern Professional", desc: "Clean blue accents, tech-focused", color: "bg-blue-50 border-blue-200" },
    { id: "minimal", name: "Minimal ATS", desc: "No formatting, max parsability", color: "bg-slate-50 border-slate-200" },
    { id: "twocolumn", name: "Two Column", desc: "Side panel for skills & contact", color: "bg-indigo-50 border-indigo-200" },
    { id: "fresher", name: "Fresher Compact", desc: "For 0-2 years experience", color: "bg-emerald-50 border-emerald-200" },
    { id: "corporate", name: "Classic Corporate", desc: "Traditional serif fonts", color: "bg-amber-50 border-amber-200" }
];

export default function TemplateSelector({ templateId, setTemplateId, onPreview }) {
    return (
        <section>
            <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-bold">1. Choose Template</h2>
                <button
                    onClick={onPreview}
                    className="px-4 py-2 bg-slate-800 text-white text-sm font-bold rounded-lg hover:bg-slate-700 transition"
                >
                    🔍 Live Preview
                </button>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                {templates.map(t => (
                    <button
                        key={t.id}
                        onClick={() => setTemplateId(t.id)}
                        className={`p-4 rounded-xl border text-left transition-all relative overflow-hidden ${templateId === t.id ? `ring-2 ring-blue-500 shadow-md ${t.color}` : 'bg-white hover:bg-slate-50'}`}
                    >
                        {templateId === t.id && (
                            <div className="absolute top-0 right-0 bg-blue-500 text-white text-[10px] uppercase font-bold px-2 py-1 rounded-bl-lg">
                                Selected
                            </div>
                        )}
                        <div className={`w-full h-24 rounded border mb-3 flex items-center justify-center text-xs opacity-70 ${t.color}`}>Preview</div>
                        <h3 className="font-bold text-sm">{t.name}</h3>
                        <p className="text-xs text-slate-500 mt-1">{t.desc}</p>
                    </button>
                ))}
            </div>
        </section>
    );
}
