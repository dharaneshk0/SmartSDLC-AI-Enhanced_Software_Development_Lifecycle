import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Bug, Loader, Copy, Download, CheckCircle, AlertTriangle } from 'lucide-react';

const BugFixer = () => {
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [isFixing, setIsFixing] = useState(false);
  const [fixedCode, setFixedCode] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const languages = [
    { value: 'python', label: 'Python' },
    { value: 'javascript', label: 'JavaScript' },
    { value: 'java', label: 'Java' },
    { value: 'cpp', label: 'C++' },
    { value: 'go', label: 'Go' },
  ];

  const handleFixBugs = async () => {
    if (!code.trim()) return;

    setIsFixing(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/ai/fix-bug', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          code: code.trim(),
          language,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setFixedCode(data.fixed_code);
      } else {
        throw new Error('Failed to fix bugs');
      }
    } catch (err) {
      setError('Error fixing bugs. Please try again.');
      console.error(err);
    } finally {
      setIsFixing(false);
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(fixedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  const handleDownload = () => {
    const extension = language === 'cpp' ? 'cpp' : language === 'javascript' ? 'js' : language;
    const blob = new Blob([fixedCode], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `fixed_code.${extension}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-12"
        >
          <div className="flex justify-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-red-500 to-orange-500 rounded-xl flex items-center justify-center">
              <Bug className="w-8 h-8 text-white" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Bug Fixer
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Automatically detect and fix bugs in your code with AI assistance
          </p>
        </motion.div>

        <div className="space-y-8">
          {/* Input Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
          >
            <h2 className="text-2xl font-semibold text-white mb-6 flex items-center gap-3">
              <AlertTriangle className="w-6 h-6 text-orange-400" />
              Buggy Code
            </h2>
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Programming Language
                </label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:ring-2 focus:ring-red-500 focus:border-transparent"
                >
                  {languages.map((lang) => (
                    <option key={lang.value} value={lang.value}>
                      {lang.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Paste your buggy code
                </label>
                <div className="bg-gray-900/50 rounded-lg overflow-hidden">
                  <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    placeholder="Paste your code here..."
                    rows={12}
                    className="w-full px-4 py-3 bg-transparent text-white placeholder-gray-400 focus:outline-none resize-none font-mono text-sm"
                  />
                </div>
              </div>

              <button
                onClick={handleFixBugs}
                disabled={!code.trim() || isFixing}
                className="w-full px-6 py-3 bg-gradient-to-r from-red-500 to-orange-500 text-white font-semibold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transition-all duration-300 flex items-center justify-center gap-2"
              >
                {isFixing ? (
                  <>
                    <Loader className="w-5 h-5 animate-spin" />
                    Fixing Bugs...
                  </>
                ) : (
                  <>
                    <Bug className="w-5 h-5" />
                    Fix Bugs
                  </>
                )}
              </button>

              {error && (
                <div className="p-4 bg-red-500/20 border border-red-500/50 rounded-lg">
                  <span className="text-red-300">{error}</span>
                </div>
              )}
            </div>
          </motion.div>

          {/* Output Section */}
          {fixedCode && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-white flex items-center gap-3">
                  <CheckCircle className="w-6 h-6 text-green-400" />
                  Fixed Code
                </h2>
                <div className="flex gap-2">
                  <button
                    onClick={handleCopy}
                    className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors duration-200 flex items-center gap-2"
                  >
                    {copied ? (
                      <>
                        <CheckCircle className="w-4 h-4" />
                        Copied!
                      </>
                    ) : (
                      <>
                        <Copy className="w-4 h-4" />
                        Copy
                      </>
                    )}
                  </button>
                  <button
                    onClick={handleDownload}
                    className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors duration-200 flex items-center gap-2"
                  >
                    <Download className="w-4 h-4" />
                    Download
                  </button>
                </div>
              </div>
              
              <div className="bg-gray-900/50 rounded-lg overflow-hidden">
                <pre className="p-4 text-gray-300 text-sm overflow-x-auto whitespace-pre-wrap font-mono">
                  {fixedCode}
                </pre>
              </div>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BugFixer;