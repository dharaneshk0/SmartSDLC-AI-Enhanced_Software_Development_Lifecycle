// Mock API service for development when backend is not available
export const mockApiService = {
  async uploadPdf(file: File) {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Mock successful response
    return {
      filename: file.name,
      extracted_text: `This is a mock extracted text from ${file.name}. 

In a real implementation, this would contain the actual text extracted from the PDF document. The text would then be processed by IBM Watsonx AI to classify it into different SDLC phases.

Sample content that might be classified:
- Requirements gathering and analysis
- System design and architecture
- Implementation and coding
- Testing and quality assurance
- Deployment and maintenance

This mock response demonstrates how the PDF classifier would work with actual backend integration.`,
      classification: `SDLC Phase Classification Results:

1. REQUIREMENTS ANALYSIS (40%)
   - Document contains requirement specifications
   - User stories and acceptance criteria identified
   - Functional and non-functional requirements present

2. DESIGN PHASE (30%)
   - System architecture diagrams mentioned
   - Database design elements found
   - UI/UX design considerations noted

3. IMPLEMENTATION (20%)
   - Code snippets and technical specifications
   - Development guidelines and standards
   - Programming language references

4. TESTING (10%)
   - Test case documentation
   - Quality assurance procedures
   - Bug tracking and resolution processes

Primary Classification: REQUIREMENTS ANALYSIS
Confidence Score: 85%`,
      text_length: 1247
    };
  }
};