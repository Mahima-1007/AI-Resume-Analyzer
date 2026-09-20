import React from 'react';
import { X } from 'lucide-react';

export default function TemplatePreviewModal({ isOpen, onClose, htmlContent, loading }) {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
            <div className="bg-slate-200 w-full max-w-5xl h-[90vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in zoom-in duration-200">

                {/* Header */}
                <div className="bg-white px-6 py-4 flex justify-between items-center border-b border-slate-300 shadow-sm z-10">
                    <div>
                        <h3 className="font-bold text-lg">Live Template Preview</h3>
                        <p className="text-xs text-slate-500">This HTML accurately reflects the final PDF export layout.</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 hover:bg-slate-100 rounded-full transition-colors text-slate-500 hover:text-slate-800"
                    >
                        <X size={24} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-auto p-8 flex justify-center items-start">
                    {loading ? (
                        <div className="h-full flex items-center justify-center font-medium text-slate-500 animate-pulse">
                            Rendering template...
                        </div>
                    ) : htmlContent ? (
                        <div
                            className="bg-white shadow-2xl origin-top"
                            style={{
                                width: '210mm',
                                minHeight: '297mm',
                                transform: 'scale(0.85)',
                                marginBottom: '-15%'
                            }}
                            dangerouslySetInnerHTML={{ __html: htmlContent }}
                        />
                    ) : (
                        <div className="h-full flex items-center justify-center text-red-500">
                            Failed to load preview.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
