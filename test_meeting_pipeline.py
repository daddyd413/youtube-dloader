#!/usr/bin/env python3
"""
Test script for PermitRDU meeting analysis pipeline

Usage:
1. Download a Triangle meeting using the YouTube downloader
2. Run this script to test transcription and analysis
3. Review the generated content

Example:
python test_meeting_pipeline.py --file downloads/raleigh_planning_20241210.mp3 --jurisdiction "Raleigh" --date "2024-12-10"
"""

import asyncio
import json
import argparse
from pathlib import Path
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.transcription import MeetingProcessor

async def test_meeting_pipeline(file_path: str, jurisdiction: str, meeting_date: str, meeting_type: str = "Planning Commission"):
    """
    Test the complete meeting processing pipeline
    """
    print(f"🎯 Testing PermitRDU Meeting Pipeline")
    print(f"📁 File: {file_path}")
    print(f"🏛️ Jurisdiction: {jurisdiction}")
    print(f"📅 Date: {meeting_date}")
    print(f"📋 Type: {meeting_type}")
    print("=" * 50)
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File not found - {file_path}")
        return False
    
    # Check file size
    file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
    print(f"📊 File size: {file_size_mb:.1f} MB")
    
    if file_size_mb > 25:
        print("⚠️  Warning: File larger than 25MB - may need chunking")
    
    # Initialize the processor
    processor = MeetingProcessor()
    
    # Prepare meeting info
    meeting_info = {
        "jurisdiction": jurisdiction,
        "date": meeting_date,
        "type": meeting_type,
        "description": f"Test processing of {jurisdiction} {meeting_type} meeting",
        "test_run": True
    }
    
    print("🤖 Starting AI processing...")
    print("1️⃣ Transcribing audio with OpenAI Whisper...")
    
    try:
        # Process the meeting
        result = await processor.process_meeting_file(file_path, meeting_info)
        
        if not result["success"]:
            print(f"❌ Processing failed: {result.get('errors')}")
            return False
        
        print("✅ Transcription completed!")
        print(f"📝 Transcript length: {len(result['transcript'])} characters")
        
        print("\n2️⃣ Analyzing content with GPT-4...")
        
        analysis = result.get("analysis")
        if analysis:
            print("✅ Analysis completed!")
            
            # Display key findings
            projects = analysis.get("projects", [])
            regulatory_changes = analysis.get("regulatory_changes", [])
            highlights = analysis.get("newsletter_highlights", [])
            
            print(f"\n📊 Analysis Results:")
            print(f"🏗️ Projects found: {len(projects)}")
            print(f"📋 Regulatory changes: {len(regulatory_changes)}")
            print(f"💡 Key highlights: {len(highlights)}")
            
            # Show project details
            if projects:
                print(f"\n🏗️ Development Projects:")
                for i, project in enumerate(projects[:3], 1):  # Show first 3
                    print(f"  {i}. {project.get('name', 'Unnamed')} - {project.get('address', 'TBD')}")
                    print(f"     Developer: {project.get('developer', 'Unknown')}")
                    print(f"     Status: {project.get('current_status', 'Unknown')}")
                    if project.get('vote_outcome'):
                        print(f"     Vote: {project['vote_outcome']}")
                    print()
            
            # Show highlights
            if highlights:
                print("💡 Key Takeaways:")
                for highlight in highlights:
                    print(f"  • {highlight}")
                print()
            
            # Save detailed results
            output_file = f"test_results_{jurisdiction.lower()}_{meeting_date.replace('-', '')}.json"
            with open(output_file, "w") as f:
                json.dump(result, f, indent=2)
            
            print(f"💾 Detailed results saved to: {output_file}")
            
            # Display cost estimate
            processing_summary = result.get("processing_summary", {})
            transcription_cost = processing_summary.get("transcription_cost", 0)
            print(f"💰 Estimated cost: ${transcription_cost:.3f}")
            
            return True
        else:
            print("❌ Analysis failed or returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        return False

def check_environment():
    """
    Check if required environment variables are set
    """
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   • {var}")
        print("\nPlease set these variables before running the test:")
        print("export OPENAI_API_KEY='your-key-here'")
        return False
    
    print("✅ Environment variables configured")
    return True

async def main():
    parser = argparse.ArgumentParser(description="Test PermitRDU meeting analysis pipeline")
    parser.add_argument("--file", required=True, help="Path to meeting audio/video file")
    parser.add_argument("--jurisdiction", required=True, help="Meeting jurisdiction (Raleigh, Durham, etc.)")
    parser.add_argument("--date", required=True, help="Meeting date (YYYY-MM-DD)")
    parser.add_argument("--type", default="Planning Commission", help="Meeting type")
    
    args = parser.parse_args()
    
    print("🚀 PermitRDU Meeting Pipeline Test")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        return
    
    # Run the test
    success = await test_meeting_pipeline(
        args.file,
        args.jurisdiction,
        args.date,
        args.type
    )
    
    if success:
        print("\n🎉 Pipeline test completed successfully!")
        print("🔄 Ready to process Triangle meetings for newsletter content")
    else:
        print("\n❌ Pipeline test failed")
        print("🔧 Check error messages above and try again")

if __name__ == "__main__":
    asyncio.run(main())