import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import PDFClassifier from './pages/PDFClassifier';
import CodeGenerator from './pages/CodeGenerator';
import BugFixer from './pages/BugFixer';
import TestGenerator from './pages/TestGenerator';
import FloatingChatbot from './components/FloatingChatbot';
import './index.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 font-inter">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
          className="relative"
        >
          <Navbar />
          
          <main className="relative">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/pdf-classifier" element={<PDFClassifier />} />
              <Route path="/code-generator" element={<CodeGenerator />} />
              <Route path="/bug-fixer" element={<BugFixer />} />
              <Route path="/test-generator" element={<TestGenerator />} />
            </Routes>
          </main>
          
          <FloatingChatbot />
        </motion.div>
      </div>
    </Router>
  );
}

export default App;