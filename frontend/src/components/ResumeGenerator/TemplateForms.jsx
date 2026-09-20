import React from 'react';
import { Plus, Trash2 } from 'lucide-react';

const Input = ({ label, value, onChange, placeholder = "", type = "text" }) => (
    <div className="mb-4">
        <label className="block text-sm font-semibold mb-1 text-slate-700">{label}</label>
        <input
            type={type}
            className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
            value={value || ""}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
        />
    </div>
);

const TextArea = ({ label, value, onChange, placeholder = "" }) => (
    <div className="mb-4">
        <label className="block text-sm font-semibold mb-1 text-slate-700">{label}</label>
        <textarea
            className="w-full p-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-blue-500 transition-shadow h-24"
            value={value || ""}
            onChange={(e) => onChange(e.target.value)}
            placeholder={placeholder}
        />
    </div>
);

export default function TemplateForms({ templateId, formData, setFormData, handleAddField, handleRemoveField }) {

    // Helper to update specific array items
    const updateArrayItem = (category, index, field, value) => {
        const newArray = [...(formData[category] || [])];
        if (typeof newArray[index] === 'object') {
            newArray[index] = { ...newArray[index], [field]: value };
        } else {
            newArray[index] = value;
        }
        setFormData({ ...formData, [category]: newArray });
    };

    const renderBasicInfo = (fields) => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Basic Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">
                {fields.includes('name') && <Input label="Full Name" value={formData.name} onChange={(v) => setFormData({ ...formData, name: v })} />}
                {fields.includes('title') && <Input label="Professional Title" value={formData.title} onChange={(v) => setFormData({ ...formData, title: v })} placeholder="e.g. Senior Developer" />}
                {fields.includes('email') && <Input label="Email" type="email" value={formData.email} onChange={(v) => setFormData({ ...formData, email: v })} />}
                {fields.includes('phone') && <Input label="Phone" value={formData.phone} onChange={(v) => setFormData({ ...formData, phone: v })} />}
                {fields.includes('linkedin') && <Input label="LinkedIn URL" value={formData.linkedin} onChange={(v) => setFormData({ ...formData, linkedin: v })} />}
                {fields.includes('github') && <Input label="GitHub URL" value={formData.github} onChange={(v) => setFormData({ ...formData, github: v })} />}
            </div>
            {fields.includes('summary') && <TextArea label="Professional Summary/Objective" value={formData.summary} onChange={(v) => setFormData({ ...formData, summary: v })} />}
        </section>
    );

    const renderSkills = () => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Skills</h3>
            <div className="flex flex-wrap gap-2 mb-2">
                {(formData.skills || []).map((skill, index) => (
                    <div key={index} className="flex items-center space-x-2 bg-slate-100 p-2 rounded-lg border">
                        <input
                            className="bg-transparent outline-none w-32 text-sm"
                            value={skill}
                            onChange={(e) => updateArrayItem('skills', index, null, e.target.value)}
                            placeholder="e.g. React"
                        />
                        <button onClick={() => handleRemoveField('skills', index)} className="text-red-500 hover:text-red-700"><Trash2 size={16} /></button>
                    </div>
                ))}
            </div>
            <button onClick={() => handleAddField('skills')} className="text-blue-600 text-sm font-bold flex items-center mt-2 hover:text-blue-800"><Plus size={16} className="mr-1" /> Add Skill</button>
        </section>
    );

    const renderEducation = () => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Education</h3>
            {(formData.education || []).map((edu, index) => (
                <div key={index} className="p-4 bg-slate-50 border rounded-xl mb-4 relative group">
                    <button onClick={() => handleRemoveField('education', index)} className="absolute top-4 right-4 text-slate-400 opacity-0 group-hover:opacity-100 hover:text-red-500 transition-all"><Trash2 size={18} /></button>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">
                        <Input label="Institution / University" value={edu.institution} onChange={(v) => updateArrayItem('education', index, 'institution', v)} />
                        <Input label="Degree & Major" value={edu.degree} onChange={(v) => updateArrayItem('education', index, 'degree', v)} placeholder="B.S. Computer Science" />
                        <Input label="Graduation Year" value={edu.year} onChange={(v) => updateArrayItem('education', index, 'year', v)} />
                    </div>
                </div>
            ))}
            <button onClick={() => handleAddField('education')} className="text-blue-600 text-sm font-bold flex items-center hover:text-blue-800"><Plus size={16} className="mr-1" /> Add Education</button>
        </section>
    );

    const renderExperience = () => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Work Experience</h3>
            {(formData.experience || []).map((exp, index) => (
                <div key={index} className="p-4 bg-slate-50 border rounded-xl mb-4 relative group">
                    <button onClick={() => handleRemoveField('experience', index)} className="absolute top-4 right-4 text-slate-400 opacity-0 group-hover:opacity-100 hover:text-red-500 transition-all"><Trash2 size={18} /></button>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">
                        <Input label="Company Name" value={exp.company} onChange={(v) => updateArrayItem('experience', index, 'company', v)} />
                        <Input label="Job Role / Title" value={exp.role} onChange={(v) => updateArrayItem('experience', index, 'role', v)} />
                        <Input label="Duration (e.g. Jan 2020 - Present)" value={exp.duration} onChange={(v) => updateArrayItem('experience', index, 'duration', v)} />
                    </div>
                    <TextArea label="Description & Achievements (Bullet points)" value={exp.description} onChange={(v) => updateArrayItem('experience', index, 'description', v)} placeholder={"• Led a team of 5 in deploying...\n• Increased revenue by 20%"} />
                </div>
            ))}
            <button onClick={() => handleAddField('experience')} className="text-blue-600 text-sm font-bold flex items-center hover:text-blue-800"><Plus size={16} className="mr-1" /> Add Experience</button>
        </section>
    );

    const renderProjects = () => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Projects</h3>
            {(formData.projects || []).map((proj, index) => (
                <div key={index} className="p-4 bg-slate-50 border rounded-xl mb-4 relative group">
                    <button onClick={() => handleRemoveField('projects', index)} className="absolute top-4 right-4 text-slate-400 opacity-0 group-hover:opacity-100 hover:text-red-500 transition-all"><Trash2 size={18} /></button>
                    <Input label="Project Title" value={proj.title} onChange={(v) => updateArrayItem('projects', index, 'title', v)} />
                    <Input label="Technologies Used" value={proj.technologies} onChange={(v) => updateArrayItem('projects', index, 'technologies', v)} placeholder="React, Node.js, MongoDB" />
                    <TextArea label="Project Description" value={proj.description} onChange={(v) => updateArrayItem('projects', index, 'description', v)} />
                </div>
            ))}
            <button onClick={() => handleAddField('projects')} className="text-blue-600 text-sm font-bold flex items-center hover:text-blue-800"><Plus size={16} className="mr-1" /> Add Project</button>
        </section>
    );

    const renderInternships = () => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Internships</h3>
            {(formData.internships || []).map((intern, index) => (
                <div key={index} className="p-4 bg-slate-50 border rounded-xl mb-4 relative group">
                    <button onClick={() => handleRemoveField('internships', index)} className="absolute top-4 right-4 text-slate-400 opacity-0 group-hover:opacity-100 hover:text-red-500 transition-all"><Trash2 size={18} /></button>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-x-4">
                        <Input label="Company Name" value={intern.company} onChange={(v) => updateArrayItem('internships', index, 'company', v)} />
                        <Input label="Role" value={intern.role} onChange={(v) => updateArrayItem('internships', index, 'role', v)} />
                        <Input label="Duration" value={intern.duration} onChange={(v) => updateArrayItem('internships', index, 'duration', v)} />
                    </div>
                    <TextArea label="Description" value={intern.description} onChange={(v) => updateArrayItem('internships', index, 'description', v)} />
                </div>
            ))}
            <button onClick={() => handleAddField('internships')} className="text-blue-600 text-sm font-bold flex items-center hover:text-blue-800"><Plus size={16} className="mr-1" /> Add Internship</button>
        </section>
    );

    const renderCertifications = () => (
        <section className="mb-8">
            <h3 className="text-lg font-bold border-b pb-2 mb-4 text-slate-800">Certifications</h3>
            {(formData.certifications || []).map((cert, index) => (
                <div key={index} className="p-4 bg-slate-50 border rounded-xl mb-4 relative group flex gap-4">
                    <div className="flex-1 text-red"><Input label="Certification Name" value={cert.name} onChange={(v) => updateArrayItem('certifications', index, 'name', v)} /></div>
                    <div className="flex-1"><Input label="Issuer" value={cert.issuer} onChange={(v) => updateArrayItem('certifications', index, 'issuer', v)} placeholder="e.g. AWS, Coursera" /></div>
                    <button onClick={() => handleRemoveField('certifications', index)} className="mt-6 text-slate-400 hover:text-red-500 transition-all h-10 w-10 flex items-center justify-center rounded-lg hover:bg-red-50"><Trash2 size={18} /></button>
                </div>
            ))}
            <button onClick={() => handleAddField('certifications')} className="text-blue-600 text-sm font-bold flex items-center hover:text-blue-800"><Plus size={16} className="mr-1" /> Add Certification</button>
        </section>
    );

    // Dynamic rendering mapping based on selected template ID
    switch (templateId) {
        case 'minimal':
            return (
                <div className="animate-in fade-in duration-300">
                    <p className="text-sm text-slate-500 mb-6 bg-blue-50 p-3 rounded-lg border border-blue-100">Showing fields for <strong>Minimal ATS</strong> template. It prioritizes pure data density.</p>
                    {renderBasicInfo(['name', 'email', 'phone', 'summary'])}
                    {renderSkills()}
                    {renderExperience()}
                    {renderEducation()}
                </div>
            );
        case 'modern':
        case 'twocolumn':
        case 'corporate':
            return (
                <div className="animate-in fade-in duration-300">
                    <p className="text-sm text-slate-500 mb-6 bg-blue-50 p-3 rounded-lg border border-blue-100">Showing standard professional fields for <strong>{templateId}</strong>.</p>
                    {renderBasicInfo(['name', 'title', 'email', 'phone', 'linkedin', 'github', 'summary'])}
                    {renderSkills()}
                    {renderExperience()}
                    {renderProjects()}
                    {renderEducation()}
                </div>
            );
        case 'fresher':
            return (
                <div className="animate-in fade-in duration-300">
                    <p className="text-sm text-slate-500 mb-6 bg-emerald-50 p-3 rounded-lg border border-emerald-100">Showing fields optimized for <strong>Fresher Compact</strong> template (prioritizes education, internships, and academia).</p>
                    {renderBasicInfo(['name', 'email', 'phone', 'linkedin', 'github', 'summary'])}
                    {renderEducation()}
                    {renderSkills()}
                    {renderInternships()}
                    {renderProjects()}
                    {renderCertifications()}
                </div>
            );
        default:
            return <div>Select a valid template.</div>;
    }
}
