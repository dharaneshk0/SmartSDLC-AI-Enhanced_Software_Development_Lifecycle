import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FileText, Upload, Loader, CheckCircle, AlertCircle, Wifi, WifiOff } from 'lucide-react';
import { mockApiService } from '../services/mockApi';

const PDFClassifier = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [isDragActive, setIsDragActive] = useState(false);
  const [isUsingMockApi, setIsUsingMockApi] = useState(false);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);

    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type === 'application/pdf') {
      setFile(files[0]);
      setError(null);
    } else {
      setError('Please select a valid PDF file');
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      if (files[0].type === 'application/pdf') {
        setFile(files[0]);
        setError(null);
      } else {
        setError('Please select a valid PDF file');
      }
    }
  };

  const handleClassify = async () => {
    if (!file) return;

    setIsProcessing(true);
    setError(null);

    try {
      // Try real API first
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/ai/upload-pdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setResult(data);
        setIsUsingMockApi(false);
      } else {
        throw new Error('Backend not available');
      }
    } catch (err) {
      // Fallback to mock API if backend is not available
      console.log('Backend not available, using mock API');
      try {
        const mockData = await mockApiService.uploadPdf(file);
        setResult(mockData);
        setIsUsingMockApi(true);
      } catch (mockErr) {
        setError('Error processing PDF. Please try again.');
        console.error(mockErr);
      }
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 pt-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
              <FileText className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            PDF Classifier
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Upload unstructured PDF documents and automatically classify content into SDLC phases
          </p>
          
          {/* API Status Indicator */}
          <div className="mt-6 flex justify-center">
            <div className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm ${
              isUsingMockApi 
                ? 'bg-yellow-500/20 border border-yellow-500/50 text-yellow-300'
                : 'bg-green-500/20 border border-green-500/50 text-green-300'
            }`}>
              {isUsingMockApi ? (
                <>
                  <WifiOff className="w-4 h-4" />
                  Demo Mode (Backend Offline)
                </>
              ) : (
                <>
                  <Wifi className="w-4 h-4" />
                  Connected to Backend
                </>
              )}
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Upload Section */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
          >
            <h2 className="text-2xl font-semibold text-white mb-6">Upload PDF</h2>
            
            <div
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-all duration-300 ${
                isDragActive
                  ? 'border-blue-500 bg-blue-500/10'
                  : 'border-gray-600 hover:border-gray-500'
              }`}
            >
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="hidden"
                id="pdf-upload"
              />
              <label htmlFor="pdf-upload" className="cursor-pointer">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                {isDragActive ? (
                  <p className="text-blue-400">Drop the PDF file here...</p>
                ) : (
                  <div>
                    <p className="text-gray-300 mb-2">
                      Drag & drop a PDF file here, or click to select
                    </p>
                    <p className="text-gray-500 text-sm">
                      Only PDF files are supported
                    </p>
                  </div>
                )}
              </label>
            </div>

            {file && (
              <div className="mt-4 p-4 bg-gray-700/50 rounded-lg">
                <div className="flex items-center gap-3">
                  <FileText className="w-5 h-5 text-blue-400" />
                  <span className="text-white">{file.name}</span>
                  <span className="text-gray-400 text-sm">
                    ({(file.size / 1024 / 1024).toFixed(2)} MB)
                  </span>
                </div>
              </div>
            )}

            <button
              onClick={handleClassify}
              disabled={!file || isProcessing}
              className="w-full mt-6 px-6 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all duration-300 flex items-center justify-center gap-2"
            >
              {isProcessing ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <FileText className="w-5 h-5" />
                  Classify PDF
                </>
              )}
            </button>

            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-400" />
                <span className="text-red-300">{error}</span>
              </div>
            )}
          </motion.div>

          {/* Results Section */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
          >
            <h2 className="text-2xl font-semibold text-white mb-6">Classification Results</h2>
            
            {!result ? (
              <div className="text-center py-12">
                <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                <p className="text-gray-400">
                  Upload and process a PDF to see classification results
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="flex items-center gap-3 p-4 bg-green-500/20 border border-green-500/50 rounded-lg">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  <span className="text-green-300">
                    Successfully processed: {result.filename}
                  </span>
                  {isUsingMockApi && (
                    <span className="text-yellow-300 text-sm ml-auto">
                      (Demo Mode)
                    </span>
                  )}
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">
                    Extracted Text Preview
                  </h3>
                  <div className="bg-gray-900/50 rounded-lg p-4 max-h-40 overflow-y-auto">
                    <pre className="text-gray-300 text-sm whitespace-pre-wrap">
                      {result.extracted_text}
                    </pre>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">
                    SDLC Classification
                  </h3>
                  <div className="bg-gray-900/50 rounded-lg p-4">
                    <pre className="text-gray-300 text-sm whitespace-pre-wrap">
                      {typeof result.classification === 'string' 
                        ? result.classification 
                        : JSON.stringify(result.classification, null, 2)
                      }
                    </pre>
                  </div>
                </div>

                <div className="text-sm text-gray-400">
                  Text length: {result.text_length} characters
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default PDFClassifier;