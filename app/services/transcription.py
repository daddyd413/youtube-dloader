# app/services/transcription.py

import openai
import os
from pathlib import Path
import aiofiles
from typing import Optional, Dict, Any
import asyncio
import json
from datetime import datetime

class TranscriptionService:
    def __init__(self):
        self.client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.max_file_size = 25 * 1024 * 1024  # 25MB limit for Whisper
    
    async def transcribe_meeting(self, file_path: str, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transcribe meeting audio and prepare for analysis
        """
        try:
            file_path = Path(file_path)
            
            # Check if file exists
            if not file_path.exists():
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "transcript": None
                }
            
            # Check file size and handle large files
            if file_path.stat().st_size > self.max_file_size:
                return await self._handle_large_file(file_path, meeting_info)
            
            # Transcribe the file
            transcript_result = await self._transcribe_file(file_path)
            
            if not transcript_result["success"]:
                return transcript_result
            
            # Enhance transcript with meeting context
            enhanced_result = await self._enhance_transcript(
                transcript_result["transcript"], 
                meeting_info
            )
            
            return {
                "success": True,
                "transcript": enhanced_result["text"],
                "meeting_info": meeting_info,
                "duration": transcript_result.get("duration"),
                "language": transcript_result.get("language"),
                "segments": transcript_result.get("segments", []),
                "cost_estimate": self._calculate_cost(transcript_result.get("duration", 0)),
                "processed_at": datetime.now().isoformat(),
                "enhanced_sections": enhanced_result.get("sections", [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Transcription failed: {str(e)}",
                "transcript": None
            }
    
    async def _transcribe_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Core transcription using OpenAI Whisper
        """
        try:
            async with aiofiles.open(file_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",  # Get timestamps and confidence
                    prompt="This is a Triangle area planning commission meeting discussing development projects, zoning, and permits."
                )
            
            return {
                "success": True,
                "transcript": transcript.text,
                "duration": getattr(transcript, 'duration', None),
                "language": getattr(transcript, 'language', None),
                "segments": getattr(transcript, 'segments', [])
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"OpenAI Whisper error: {str(e)}",
                "transcript": None
            }
    
    async def _enhance_transcript(self, raw_transcript: str, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use Claude to clean up transcript and identify speakers/sections
        """
        try:
            enhancement_prompt = f"""
            Clean up this Triangle planning meeting transcript and organize it for analysis.
            
            Meeting Context:
            - Jurisdiction: {meeting_info.get('jurisdiction', 'Unknown')}
            - Date: {meeting_info.get('date', 'Unknown')}
            - Meeting Type: {meeting_info.get('type', 'Planning Commission')}
            
            Please:
            1. Fix obvious transcription errors
            2. Identify distinct speakers when possible (Chair, Commissioners, Staff, Public)
            3. Break into logical sections (Agenda items, Project discussions, Public comments)
            4. Preserve all project names, addresses, developer names, and vote outcomes
            
            Return JSON format:
            {{
                "text": "cleaned_full_transcript",
                "sections": [
                    {{
                        "title": "section_name",
                        "content": "section_content",
                        "speakers": ["list_of_speakers"],
                        "key_topics": ["project_names", "addresses"]
                    }}
                ]
            }}
            
            Original Transcript:
            {raw_transcript[:8000]}  # Limit to avoid token limits
            """
            
            # This would use Claude API - placeholder for now
            # In production, you'd call Claude API here
            return {
                "text": raw_transcript,  # Return original for now
                "sections": []
            }
            
        except Exception as e:
            return {
                "text": raw_transcript,
                "sections": [],
                "error": f"Enhancement failed: {str(e)}"
            }
    
    async def _handle_large_file(self, file_path: Path, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Split large files into chunks for processing
        """
        # For now, reject large files - implement chunking later
        return {
            "success": False,
            "error": f"File too large ({file_path.stat().st_size / 1024 / 1024:.1f}MB). Maximum size is 25MB.",
            "transcript": None,
            "suggestion": "Please use audio optimization tools to reduce file size or implement file chunking."
        }
    
    def _calculate_cost(self, duration_minutes: float) -> float:
        """
        Calculate estimated cost for OpenAI Whisper transcription
        """
        if duration_minutes is None:
            return 0.0
        return duration_minutes * 0.006  # $0.006 per minute

# Meeting Analysis Service
class MeetingAnalysisService:
    def __init__(self):
        # Initialize Claude/OpenAI clients for analysis
        self.openai_client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    async def analyze_transcript(self, transcript: str, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract development intelligence from meeting transcript
        """
        try:
            analysis_prompt = self._build_analysis_prompt(transcript, meeting_info)
            
            # Use GPT-4 for comprehensive analysis
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert Triangle area development analyst who extracts key information from planning meetings."},
                    {"role": "user", "content": analysis_prompt}
                ],
                temperature=0.1  # Low temperature for consistent extraction
            )
            
            # Parse the structured response
            analysis_text = response.choices[0].message.content
            
            # Try to parse as JSON, fall back to text if needed
            try:
                analysis_data = json.loads(analysis_text)
            except json.JSONDecodeError:
                analysis_data = {"raw_analysis": analysis_text}
            
            return {
                "success": True,
                "analysis": analysis_data,
                "meeting_info": meeting_info,
                "analyzed_at": datetime.now().isoformat(),
                "token_usage": response.usage.total_tokens if hasattr(response, 'usage') else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}",
                "analysis": None
            }
    
    def _build_analysis_prompt(self, transcript: str, meeting_info: Dict[str, Any]) -> str:
        """
        Build comprehensive analysis prompt for Triangle development intelligence
        """
        return f"""
        Analyze this {meeting_info.get('jurisdiction', 'Triangle')} planning meeting transcript and extract development intelligence for a professional newsletter.
        
        Meeting Details:
        - Jurisdiction: {meeting_info.get('jurisdiction', 'Unknown')}
        - Date: {meeting_info.get('date', 'Unknown')}
        - Type: {meeting_info.get('type', 'Planning Commission')}
        
        Extract and return JSON with these sections:
        
        {{
            "projects": [
                {{
                    "name": "project_name",
                    "address": "street_address",
                    "developer": "developer_company",
                    "applicant": "applicant_name",
                    "project_type": "residential/commercial/mixed-use/etc",
                    "current_status": "application/review/approval/denial/deferred",
                    "vote_outcome": "approved/denied/deferred/no_vote",
                    "vote_details": "vote_count_if_available",
                    "key_concerns": ["list", "of", "concerns"],
                    "conditions": ["approval", "conditions"],
                    "timeline": "next_steps_or_deadlines",
                    "opposition": "summary_of_public_opposition",
                    "staff_recommendation": "staff_position"
                }}
            ],
            "regulatory_changes": [
                {{
                    "topic": "ordinance/fee/policy_change",
                    "description": "what_changed",
                    "impact": "effect_on_development",
                    "effective_date": "when_it_takes_effect"
                }}
            ],
            "market_intelligence": [
                {{
                    "trend": "observed_pattern",
                    "description": "trend_details",
                    "implications": "what_it_means_for_developers"
                }}
            ],
            "key_people": [
                {{
                    "name": "person_name",
                    "role": "commissioner/staff/developer",
                    "notable_positions": "key_statements_or_positions"
                }}
            ],
            "newsletter_highlights": [
                "Most important takeaway 1",
                "Most important takeaway 2",
                "Most important takeaway 3"
            ]
        }}
        
        Focus on actionable intelligence that Triangle development professionals need to know.
        
        Transcript:
        {transcript[:12000]}  # Limit transcript to avoid token limits
        """

# Usage example and integration
class MeetingProcessor:
    def __init__(self):
        self.transcription_service = TranscriptionService()
        self.analysis_service = MeetingAnalysisService()
    
    async def process_meeting_file(self, file_path: str, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete pipeline: audio -> transcript -> analysis
        """
        # Step 1: Transcribe
        transcript_result = await self.transcription_service.transcribe_meeting(file_path, meeting_info)
        
        if not transcript_result["success"]:
            return transcript_result
        
        # Step 2: Analyze
        analysis_result = await self.analysis_service.analyze_transcript(
            transcript_result["transcript"], 
            meeting_info
        )
        
        # Combine results
        return {
            "success": analysis_result["success"],
            "transcript": transcript_result["transcript"],
            "analysis": analysis_result.get("analysis"),
            "meeting_info": meeting_info,
            "processing_summary": {
                "transcription_cost": transcript_result.get("cost_estimate", 0),
                "transcript_length": len(transcript_result["transcript"]) if transcript_result["transcript"] else 0,
                "analysis_tokens": analysis_result.get("token_usage"),
                "processed_at": datetime.now().isoformat()
            },
            "errors": {
                "transcription_error": None if transcript_result["success"] else transcript_result.get("error"),
                "analysis_error": None if analysis_result["success"] else analysis_result.get("error")
            }
        }