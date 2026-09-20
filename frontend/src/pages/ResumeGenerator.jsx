import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import axios from 'axios';
import { Download, AlertCircle } from 'lucide-react';
import TemplateSelector from '../components/ResumeGenerator/TemplateSelector';
import TemplateForms from '../components/ResumeGenerator/TemplateForms';
import TemplatePreviewModal from '../components/ResumeGenerator/TemplatePreviewModal';

const API_URL = "http://localhost:8001";

export default function ResumeGenerator() {
    const location = useLocation();
    const prefillData = location.state?.prefillData;

    const [templateId, setTemplateId] = useState("modern");

    // Comprehensive default state covering all possible fields across all templates
    const [formData, setFormData] = useState(prefillData || {
        name: "", title: "", email: "", phone: "", linkedin: "", github: "", summary: "",
        education: [{ institution: "", degree: "", year: "" }],
        skills: [""],
        experience: [{ company: "", role: "", duration: "", description: "" }],
        projects: [{ title: "", description: "", technologies: "" }],
        internships: [{ company: "", role: "", duration: "", description: "" }],
        certifications: [{ name: "", issuer: "" }]
    });

    // Preview Modal State
    const [previewOpen, setPreviewOpen] = useState(false);
    const [previewHtml, setPreviewHtml] = useState(null);
    const [previewLoading, setPreviewLoading] = useState(false);
    const [generatingPdf, setGeneratingPdf] = useState(false);

    const handleAddField = (category) => {
        const newItem = category === 'skills' ? "" :
            category === 'education' ? { institution: "", degree: "", year: "" } :
                category === 'experience' ? { company: "", role: "", duration: "", description: "" } :
                    category === 'internships' ? { company: "", role: "", duration: "", description: "" } :
                        category === 'certifications' ? { name: "", issuer: "" } :
                            { title: "", description: "", technologies: "" };

        setFormData({ ...formData, [category]: [...(formData[category] || []), newItem] });
    };

    const handleRemoveField = (category, index) => {
        const newArray = [...(formData[category] || [])];
        newArray.splice(index, 1);
        setFormData({ ...formData, [category]: newArray });
    };

    // Fetches live HTML layout from backend for previewing
    const loadPreview = async () => {
        setPreviewOpen(true);
        setPreviewLoading(true);
        try {
            const payload = { ...formData, template_id: templateId };
            const response = await axios.post(`${API_URL}/api/preview_html`, payload, {
                headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
            });
            setPreviewHtml(response.data.html_content);
        } catch (err) {
            console.error(err);
            alert("Failed to load preview");
        } finally {
            setPreviewLoading(false);
        }
    };

    const handleDownload = async () => {
        setGeneratingPdf(true);
        try {
            const payload = { ...formData, template_id: templateId };
            const response = await axios.post(`${API_URL}/api/generate`, payload, {
                headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
                responseType: 'blob'
            });
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `Resume_${templateId}.pdf`);
            document.body.appendChild(link);
            link.click();
        } catch (err) {
            alert("Failed to generate resume PDF");
        } finally {
            setGeneratingPdf(false);
        }
    };

    return (
        <div className="flex bg-slate-50 min-h-screen relative">
            <Sidebar />
            <main className="flex-1 p-8 overflow-y-auto max-h-screen">
                <div className="flex justify-between items-center mb-8">
                    <h1 className="text-3xl font-bold gradient-text">Resume Generator</h1>
                    <button
                        onClick={handleDownload}
                        disabled={generatingPdf}
                        className="px-6 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition shadow-lg flex items-center space-x-2 disabled:opacity-50"
                    >
                        {generatingPdf ? "Processing..." : <><Download size={20} /> <span>Download as PDF</span></>}
                    </button>
                </div>

                <div className="bg-white p-8 rounded-2xl shadow-sm border border-slate-100 max-w-4xl space-y-8 pb-32">

                    <TemplateSelector
                        templateId={templateId}
                        setTemplateId={setTemplateId}
                        onPreview={loadPreview}
                    />

                    <hr className="border-slate-100" />
                    <div className="flex items-center space-x-2 mb-4">
                        <h2 className="text-xl font-bold">2. Fill Dynamic Details</h2>
                    </div>

                    <TemplateForms
                        templateId={templateId}
                        formData={formData}
                        setFormData={setFormData}
                        handleAddField={handleAddField}
                        handleRemoveField={handleRemoveField}
                    />

                </div>
            </main>

            <TemplatePreviewModal
                isOpen={previewOpen}
                onClose={() => setPreviewOpen(false)}
                htmlContent={previewHtml}
                loading={previewLoading}
            />
        </div>
    );
}
