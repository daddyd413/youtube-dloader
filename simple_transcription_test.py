#!/usr/bin/env python3
"""
Simple transcription test for large files
"""

import asyncio
import openai
import os
from pathlib import Path

async def simple_transcribe_test(file_path: str):
    """
    Simple test that handles large files by using OpenAI Whisper directly
    """
    print(f"🎯 Testing Transcription")
    print(f"📁 File: {file_path}")
    
    # Check if file exists
    if not Path(file_path).exists():
        print(f"❌ Error: File not found - {file_path}")
        return False
    
    # Check file size
    file_size_mb = Path(file_path).stat().st_size / (1024 * 1024)
    print(f"📊 File size: {file_size_mb:.1f} MB")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set")
        return False
    
    print("✅ Environment ready")
    
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        print("🤖 Starting transcription with OpenAI Whisper...")
        print("⏱️ This may take several minutes for large files...")
        
        # Open and transcribe the file
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text",
                prompt="This is a Raleigh Planning Commission meeting discussing development projects, zoning, and permits."
            )
        
        print("✅ Transcription completed!")
        print(f"📝 Transcript length: {len(transcript)} characters")
        print(f"💰 Estimated cost: ${(file_size_mb * 0.006 / 60):.3f}")
        
        # Show first 500 characters as preview
        print("\n📄 Transcript Preview:")
        print("-" * 50)
        print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
        print("-" * 50)
        
        # Save full transcript
        output_file = f"transcript_raleigh_{Path(file_path).stem}.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        print(f"💾 Full transcript saved to: {output_file}")
        
        # Basic analysis - count key words
        transcript_lower = transcript.lower()
        keywords = {
            "projects": transcript_lower.count("project"),
            "development": transcript_lower.count("development"),
            "zoning": transcript_lower.count("zoning"),
            "approve": transcript_lower.count("approve"),
            "deny": transcript_lower.count("deny"),
            "motion": transcript_lower.count("motion"),
            "vote": transcript_lower.count("vote")
        }
        
        print(f"\n📊 Quick Analysis:")
        for word, count in keywords.items():
            if count > 0:
                print(f"  • {word.title()}: {count} mentions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during transcription: {str(e)}")
        return False

async def main():
    file_path = "downloads/Raleigh Planning Commission Meeting - August 12, 2025.m4a"
    success = await simple_transcribe_test(file_path)
    
    if success:
        print("\n🎉 Transcription test completed successfully!")
        print("📈 Ready to build the full analysis pipeline!")
    else:
        print("\n❌ Transcription test failed")

if __name__ == "__main__":
    asyncio.run(main())