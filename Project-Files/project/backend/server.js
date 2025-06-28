import express from 'express';
import cors from 'cors';
import multer from 'multer';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads/');
  },
  filename: (req, file, cb) => {
    cb(null, Date.now() + '-' + file.originalname);
  }
});

const upload = multer({ storage });

// Mock AI service (replace with actual AI integration)
class AIService {
  static async generateResponse(message) {
    // Simulate AI response - replace with actual AI service
    return {
      response: `AI Response to: "${message}". This is a mock response. Please integrate with your preferred AI service.`,
      timestamp: new Date().toISOString()
    };
  }

  static async analyzeDocument(filePath) {
    // Simulate document analysis - replace with actual document processing
    return {
      summary: "This is a mock document analysis. Please integrate with your preferred document processing service.",
      keyPoints: [
        "Mock key point 1",
        "Mock key point 2",
        "Mock key point 3"
      ],
      timestamp: new Date().toISOString()
    };
  }
}

// Routes
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Backend server is running' });
});

app.post('/api/chat', async (req, res) => {
  try {
    const { message } = req.body;
    
    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    const aiResponse = await AIService.generateResponse(message);
    
    res.json({
      success: true,
      data: aiResponse
    });
  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to process chat message' 
    });
  }
});

app.post('/api/upload', upload.single('document'), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const analysis = await AIService.analyzeDocument(req.file.path);
    
    res.json({
      success: true,
      data: {
        filename: req.file.filename,
        originalName: req.file.originalname,
        analysis
      }
    });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to process document' 
    });
  }
});

app.post('/api/feedback', (req, res) => {
  try {
    const { rating, comment, messageId } = req.body;
    
    // Store feedback (implement your preferred storage solution)
    console.log('Feedback received:', { rating, comment, messageId });
    
    res.json({
      success: true,
      message: 'Feedback received successfully'
    });
  } catch (error) {
    console.error('Feedback error:', error);
    res.status(500).json({ 
      success: false, 
      error: 'Failed to submit feedback' 
    });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ 
    success: false, 
    error: 'Something went wrong!' 
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});