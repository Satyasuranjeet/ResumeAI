# Resume Analyzer Web Application

A sophisticated web application that analyzes resumes against job descriptions and provides a match score with improvement suggestions.

## Features

- **PDF Resume Upload**: Drag & drop or click to upload PDF resumes
- **Text Extraction**: Automatically extracts text from uploaded PDF files
- **Keyword Analysis**: Removes stopwords and extracts meaningful keywords
- **Job Matching**: Compares resume keywords with job description keywords
- **Score Calculation**: Provides a percentage match score out of 100
- **Smart Suggestions**: Recommends keywords to add for better matching
- **Dark Theme**: Beautiful dark UI with smooth animations
- **Responsive Design**: Works on desktop and mobile devices

## Deployment

### Local Development

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app_web.py
   ```

4. **Open your browser and go to**:
   ```
   http://localhost:5000
   ```

### Deploy to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy the application**:
   ```bash
   vercel
   ```

4. **Follow the prompts**:
   - Set up and deploy: **Yes**
   - Which scope: Select your account
   - Link to existing project: **No**
   - Project name: `ai-resume-analyzer` (or your preferred name)
   - Directory: `./` (current directory)

5. **Production deployment**:
   ```bash
   vercel --prod
   ```

Your application will be deployed to a Vercel URL like `https://ai-resume-analyzer.vercel.app`

### Environment Variables (Vercel)

No additional environment variables are required for basic functionality.

## How to Use

1. **Upload Resume**: Click the upload area or drag & drop a PDF resume file
2. **Enter Company Name**: (Optional) Add the company name for reference
3. **Paste Job Description**: Copy and paste the complete job description
4. **Click Analyze**: The system will process your resume and provide results

## Results Display

- **Match Score**: Percentage score showing how well your resume matches the job
- **Statistics**: Number of matched keywords vs total keywords
- **Matched Keywords**: Keywords found in both resume and job description
- **Suggestions**: Keywords from job description missing in your resume
- **Resume Preview**: First 500 characters of extracted resume text

## Technical Details

### Backend (Flask)
- PDF text extraction using PyPDF2
- Keyword cleaning and normalization with regex
- Stopword filtering for meaningful analysis
- Score calculation based on keyword overlap
- Error handling for corrupted or protected PDFs

### Frontend
- Modern dark theme with CSS animations
- Responsive grid layout
- Drag & drop file upload
- Real-time feedback and loading states
- Smooth scrolling and transitions

### Security Features
- File type validation (PDF only)
- Secure filename handling
- Temporary file cleanup
- File size limits (16MB max)

## File Structure

```
├── api/
│   └── index.py            # Vercel serverless function entry point
├── templates/
│   └── index.html          # Frontend HTML template
├── app_web.py              # Main Flask application (for local development)
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel deployment configuration
├── .vercelignore          # Files to exclude from Vercel deployment
├── uploads/               # Temporary file storage (auto-created, local only)
└── README.md             # This file
```

## Customization

### Adding More Stopwords
Edit the `stopwords` set in `app_web.py` to add or remove stopwords.

### Changing UI Colors
Modify the CSS gradients and color variables in `templates/index.html`.

### Adjusting Score Calculation
Update the `calculate_score()` function in `app_web.py` for different scoring algorithms.

## Error Handling

The application handles various error scenarios:
- Invalid file types
- Corrupted PDF files
- Password-protected PDFs
- Files with no extractable text
- Network/server errors

## Performance Notes

- Files are processed in memory and deleted immediately after analysis
- Maximum file size is limited to 16MB
- Text extraction is optimized for speed
- Keyword processing uses efficient set operations

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Troubleshooting

**PDF text extraction fails**: 
- Ensure PDF is not password-protected
- Check if PDF contains searchable text (not just images)
- Try with a different PDF file

**Upload not working**:
- Check file size (must be under 16MB)
- Ensure file is a valid PDF
- Try refreshing the page

**Poor match scores**:
- Use more specific keywords in resume
- Include technical terms from job description
- Add relevant skills and technologies

**Vercel Deployment Issues**:
- Ensure all dependencies are listed in `requirements.txt`
- Check Vercel function logs for detailed error messages
- Verify the `api/index.py` file is properly configured
- Make sure file size limits are respected (Vercel has 50MB limit for serverless functions)

**Performance on Vercel**:
- Large PDF files may take longer to process due to cold starts
- Consider optimizing PDF files before upload
- Function timeout is set to 60 seconds for complex processing
