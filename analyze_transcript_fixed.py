#!/usr/bin/env python3
"""
AI Analysis Test for Triangle Meeting Transcripts - Fixed Version
Extract structured development intelligence from meeting transcripts
"""

import openai
import os
import json
from datetime import datetime

def analyze_transcript(transcript_file: str, meeting_info: dict):
    """
    Analyze meeting transcript to extract development intelligence
    """
    print(f"🧠 Triangle Development Intelligence Analysis")
    print(f"📄 Transcript: {transcript_file}")
    print(f"🏛️ Meeting: {meeting_info['jurisdiction']} {meeting_info['type']}")
    print("=" * 60)
    
    # Read the transcript
    try:
        with open(transcript_file, 'r', encoding='utf-8') as f:
            transcript = f.read()
        print(f"📝 Transcript loaded: {len(transcript)} characters")
    except FileNotFoundError:
        print(f"❌ Transcript file not found: {transcript_file}")
        return None
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    print("🤖 Starting AI analysis with GPT-4...")
    
    # Build analysis prompt
    analysis_prompt = build_analysis_prompt(transcript, meeting_info)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert Triangle area development analyst who extracts key information from planning meetings for professional newsletters."
                },
                {
                    "role": "user", 
                    "content": analysis_prompt
                }
            ],
            temperature=0.1  # Low temperature for consistent extraction
        )
        
        analysis_text = response.choices[0].message.content
        print("✅ AI analysis completed!")
        
        # Try to parse as JSON, fall back to text if needed
        try:
            analysis_data = json.loads(analysis_text)
            print("✅ Structured data extracted successfully!")
        except json.JSONDecodeError:
            print("⚠️ Received text analysis, attempting to structure...")
            analysis_data = {"raw_analysis": analysis_text}
        
        # Display results
        display_analysis_results(analysis_data, meeting_info)
        
        # Save results
        output_file = f"analysis_{meeting_info['jurisdiction'].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "meeting_info": meeting_info,
                "analysis": analysis_data,
                "transcript_length": len(transcript),
                "analyzed_at": datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"💾 Analysis saved to: {output_file}")
        
        return analysis_data
        
    except Exception as e:
        print(f"❌ AI analysis failed: {str(e)}")
        return None

def build_analysis_prompt(transcript: str, meeting_info: dict) -> str:
    """
    Build comprehensive analysis prompt for Triangle development intelligence
    """
    return f"""
Analyze this {meeting_info.get('jurisdiction', 'Triangle')} planning meeting transcript and extract development intelligence for the Triangle Development Digest newsletter.

Meeting Details:
- Jurisdiction: {meeting_info.get('jurisdiction', 'Unknown')}
- Date: {meeting_info.get('date', 'Unknown')}
- Type: {meeting_info.get('type', 'Planning Commission')}

Extract and return JSON with these sections:

{{
    "projects": [
        {{
            "name": "project_name or case_number",
            "address": "street_address or location", 
            "case_number": "zoning_case_number if mentioned",
            "developer": "developer_company",
            "applicant": "applicant_name",
            "project_type": "residential/commercial/mixed-use/rezoning/etc",
            "current_status": "application/review/approval/denial/deferred",
            "vote_outcome": "approved/denied/deferred/no_vote",
            "vote_details": "vote_count_if_available (e.g. 9-0, 7-2)",
            "key_concerns": ["list", "of", "concerns", "raised"],
            "conditions": ["approval", "conditions", "if any"],
            "timeline": "next_steps_or_deadlines",
            "opposition": "summary_of_public_opposition",
            "staff_recommendation": "staff_position",
            "acreage": "land_size_if_mentioned",
            "previous_action": "history_from_previous_meetings"
        }}
    ],
    "key_people": [
        {{
            "name": "person_name",
            "role": "commissioner/staff/developer/citizen",
            "notable_positions": "key_statements_or_positions"
        }}
    ],
    "newsletter_highlights": [
        "Most important takeaway for Triangle developers 1",
        "Most important takeaway for Triangle developers 2", 
        "Most important takeaway for Triangle developers 3"
    ]
}}

Focus on actionable intelligence that Triangle development professionals need to know. Pay special attention to:
- Specific project names, addresses, and case numbers
- Vote outcomes and commissioner positions  
- Timeline and next steps
- Staff recommendations and their success rate

Transcript:
{transcript}
"""

def display_analysis_results(analysis_data: dict, meeting_info: dict):
    """
    Display analysis results in a readable format
    """
    print(f"\n📊 Analysis Results for {meeting_info['jurisdiction']}:")
    print("=" * 60)
    
    # Projects found
    projects = analysis_data.get("projects", [])
    if projects:
        print(f"\n🏗️ Development Projects Found: {len(projects)}")
        for i, project in enumerate(projects, 1):
            print(f"\n  📍 Project {i}:")
            print(f"    • Name: {project.get('name', 'Unknown')}")
            print(f"    • Address: {project.get('address', 'TBD')}")
            print(f"    • Case: {project.get('case_number', 'N/A')}")
            print(f"    • Type: {project.get('project_type', 'Unknown')}")
            print(f"    • Status: {project.get('current_status', 'Unknown')}")
            
            if project.get('vote_outcome'):
                print(f"    • Vote: {project['vote_outcome']}")
                if project.get('vote_details'):
                    print(f"    • Details: {project['vote_details']}")
            
            if project.get('developer'):
                print(f"    • Developer: {project['developer']}")
            
            if project.get('acreage'):
                print(f"    • Size: {project['acreage']}")
            
            if project.get('timeline'):
                print(f"    • Next Steps: {project['timeline']}")
            
            if project.get('previous_action'):
                print(f"    • History: {project['previous_action']}")
    
    # Key People
    people = analysis_data.get("key_people", [])
    if people:
        print(f"\n👥 Key People Mentioned: {len(people)}")
        for person in people:
            print(f"    • {person.get('name', 'Unknown')} ({person.get('role', 'Unknown role')})")
    
    # Newsletter Highlights
    highlights = analysis_data.get("newsletter_highlights", [])
    if highlights:
        print(f"\n💡 Newsletter Highlights:")
        for i, highlight in enumerate(highlights, 1):
            print(f"    {i}. {highlight}")
    
    # Show raw analysis if structured parsing failed
    if "raw_analysis" in analysis_data:
        print(f"\n📄 Raw Analysis:")
        print("-" * 40)
        print(analysis_data["raw_analysis"][:1000] + "..." if len(analysis_data["raw_analysis"]) > 1000 else analysis_data["raw_analysis"])
        print("-" * 40)
    
    print("\n" + "=" * 60)

def main():
    """
    Test the analysis with the Raleigh transcript
    """
    meeting_info = {
        "jurisdiction": "Raleigh",
        "date": "2025-08-12", 
        "type": "Planning Commission",
        "description": "Middle 10-minute sample analysis test"
    }
    
    transcript_file = "transcript_raleigh_middle_sample.txt"
    
    print("🚀 PermitRDU AI Analysis Test")
    print("Testing Triangle development intelligence extraction")
    print()
    
    analysis_result = analyze_transcript(transcript_file, meeting_info)
    
    if analysis_result:
        print("\n🎉 Analysis completed successfully!")
        print("📈 Ready to generate newsletter content!")
        print(f"💰 Estimated cost: ~$0.10-0.20 for analysis")
    else:
        print("\n❌ Analysis failed - check errors above")

if __name__ == "__main__":
    main()