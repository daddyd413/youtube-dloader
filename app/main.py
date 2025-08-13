# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from pathlib import Path

# Import your existing and new API routers
from .api.downloads import router as downloads_router
from .api.meetings import router as meetings_router

app = FastAPI(
    title="PermitRDU API",
    description="Triangle Development Intelligence & Permitting Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(downloads_router, prefix="/api/downloads", tags=["downloads"])
app.include_router(meetings_router, prefix="/api/meetings", tags=["meetings"])

# Serve static files for downloads
downloads_dir = Path("downloads")
downloads_dir.mkdir(exist_ok=True)
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

# Serve static files for meetings
meetings_dir = Path("meetings")
meetings_dir.mkdir(exist_ok=True)
app.mount("/meetings", StaticFiles(directory="meetings"), name="meetings")

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Main landing page with API documentation and quick start guide
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PermitRDU - Triangle Development Intelligence</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px; 
                margin: 0 auto; 
                padding: 2rem;
                line-height: 1.6;
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 2rem; 
                border-radius: 10px; 
                margin-bottom: 2rem;
            }
            .section { 
                background: #f8f9fa; 
                padding: 1.5rem; 
                border-radius: 8px; 
                margin-bottom: 1.5rem;
                border-left: 4px solid #007bff;
            }
            .api-link { 
                display: inline-block; 
                background: #007bff; 
                color: white; 
                padding: 12px 24px; 
                text-decoration: none; 
                border-radius: 6px; 
                margin: 10px 10px 10px 0;
                font-weight: 500;
            }
            .api-link:hover { background: #0056b3; }
            .endpoint { 
                background: #e9ecef; 
                padding: 8px 12px; 
                border-radius: 4px; 
                font-family: 'Monaco', 'Consolas', monospace;
                margin: 5px 0;
                font-size: 14px;
            }
            ul { padding-left: 20px; }
            li { margin: 8px 0; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏗️ PermitRDU</h1>
            <p>Triangle Development Intelligence & Permitting Platform</p>
            <p>Automated meeting analysis and newsletter generation for Triangle development professionals</p>
        </div>

        <div class="section">
            <h2>🚀 Quick Start</h2>
            <a href="/docs" class="api-link">📚 API Documentation</a>
            <a href="/redoc" class="api-link">📖 ReDoc Documentation</a>
        </div>

        <div class="section">
            <h2>📥 YouTube Video Downloads</h2>
            <p>Download Triangle planning meeting videos for analysis:</p>
            <div class="endpoint">POST /api/downloads/download</div>
            <ul>
                <li>Download YouTube videos as MP3 or MP4</li>
                <li>Perfect for capturing planning commission meetings</li>
                <li>Automatic file organization in downloads folder</li>
            </ul>
        </div>

        <div class="section">
            <h2>🎙️ Meeting Transcription & Analysis</h2>
            <p>Transform meeting audio into development intelligence:</p>
            <div class="endpoint">POST /api/meetings/upload-meeting</div>
            <div class="endpoint">POST /api/meetings/process-existing-file</div>
            <ul>
                <li>AI-powered transcription using OpenAI Whisper</li>
                <li>Extract project data, vote outcomes, and developer activity</li>
                <li>Generate Triangle development newsletter content</li>
                <li>Support for Raleigh, Durham, Chapel Hill, Cary, and Wake County</li>
            </ul>
        </div>

        <div class="section">
            <h2>📰 Newsletter Generation</h2>
            <p>Create professional Triangle development content:</p>
            <div class="endpoint">POST /api/meetings/generate-newsletter-content</div>
            <ul>
                <li>Project pipeline updates</li>
                <li>Regulatory intelligence</li>
                <li>Market trends and developer activity</li>
                <li>Ready-to-publish newsletter sections</li>
            </ul>
        </div>

        <div class="section">
            <h2>📊 Meeting Management</h2>
            <p>Track and manage all processed meetings:</p>
            <div class="endpoint">GET /api/meetings</div>
            <div class="endpoint">GET /api/meetings/{results_filename}</div>
            <ul>
                <li>View all processed meetings and analysis results</li>
                <li>Search by jurisdiction and date</li>
                <li>Download transcripts and analysis data</li>
            </ul>
        </div>

        <div class="section">
            <h2>🔧 Environment Setup Required</h2>
            <p>To use the AI features, set these environment variables:</p>
            <ul>
                <li><strong>OPENAI_API_KEY</strong> - For Whisper transcription and GPT-4 analysis</li>
                <li><strong>ANTHROPIC_API_KEY</strong> - For Claude content enhancement (optional)</li>
            </ul>
        </div>

        <div class="section">
            <h2>🏙️ Triangle Jurisdiction Coverage</h2>
            <p>Optimized for Triangle area development intelligence:</p>
            <ul>
                <li><strong>Raleigh</strong> - Planning Commission, Design Review Commission</li>
                <li><strong>Durham</strong> - City-County Planning Commission</li>
                <li><strong>Chapel Hill</strong> - Planning Commission, Board of Adjustment</li>
                <li><strong>Cary</strong> - Planning & Zoning Board</li>
                <li><strong>Wake County</strong> - Planning Board</li>
                <li><strong>Durham County</strong> - Planning Commission</li>
            </ul>
        </div>

        <div class="section">
            <h2>💡 Workflow Example</h2>
            <ol>
                <li><strong>Download Meeting</strong>: Use <code>/api/downloads/download</code> with YouTube URL</li>
                <li><strong>Process Audio</strong>: Use <code>/api/meetings/process-existing-file</code> with downloaded MP3</li>
                <li><strong>Review Analysis</strong>: Check extracted projects, votes, and insights</li>
                <li><strong>Generate Content</strong>: Create newsletter sections with <code>/api/meetings/generate-newsletter-content</code></li>
                <li><strong>Publish Intelligence</strong>: Use generated content for Triangle Development Digest</li>
            </ol>
        </div>

        <div class="section">
            <h2>📈 Development Status</h2>
            <p><strong>Current Phase</strong>: MVP Development - Manual Meeting Processing</p>
            <ul>
                <li>✅ YouTube video download system</li>
                <li>✅ AI transcription with OpenAI Whisper</li>
                <li>✅ Development project extraction</li>
                <li>✅ Newsletter content generation</li>
                <li>🔄 Live stream automation (coming soon)</li>
                <li>🔄 Web interface for content management</li>
                <li>🔄 Automated Triangle meeting monitoring</li>
            </ul>
        </div>

        <footer style="text-align: center; margin-top: 3rem; padding: 2rem; border-top: 1px solid #dee2e6;">
            <p><strong>PermitRDU</strong> - Transforming Triangle development intelligence with AI</p>
            <p><a href="/docs" style="color: #007bff;">Explore the API →</a></p>
        </footer>
    </body>
    </html>
    """