#!/usr/bin/env python3
"""
Newsletter Content Generator for Triangle Development Digest
Transform meeting analysis into professional newsletter sections
"""

import openai
import os
import json
from datetime import datetime

def generate_newsletter_content(analysis_file: str):
    """
    Generate professional newsletter content from meeting analysis
    """
    print(f"📰 Triangle Development Digest - Content Generator")
    print(f"📄 Analysis File: {analysis_file}")
    print("=" * 60)
    
    # Load analysis data
    try:
        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Analysis loaded successfully")
    except FileNotFoundError:
        print(f"❌ Analysis file not found: {analysis_file}")
        return None
    
    meeting_info = data.get('meeting_info', {})
    analysis = data.get('analysis', {})
    
    print(f"🏛️ Meeting: {meeting_info.get('jurisdiction')} {meeting_info.get('type')}")
    print(f"📅 Date: {meeting_info.get('date')}")
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set")
        return None
    
    client = openai.OpenAI(api_key=api_key)
    
    print("\n🤖 Generating newsletter content with GPT-4...")
    
    # Generate different newsletter sections
    newsletter_sections = {}
    
    # 1. Project Pipeline Section
    if analysis.get('projects'):
        print("📝 Generating Project Pipeline section...")
        pipeline_content = generate_project_pipeline(client, analysis, meeting_info)
        newsletter_sections['project_pipeline'] = pipeline_content
    
    # 2. Market Intelligence Section  
    print("📊 Generating Market Intelligence section...")
    market_content = generate_market_intelligence(client, analysis, meeting_info)
    newsletter_sections['market_intelligence'] = market_content
    
    # 3. Regulatory Watch Section
    print("📋 Generating Regulatory Watch section...")
    regulatory_content = generate_regulatory_watch(client, analysis, meeting_info)
    newsletter_sections['regulatory_watch'] = regulatory_content
    
    # 4. People & Politics Section
    if analysis.get('key_people'):
        print("👥 Generating People & Politics section...")
        people_content = generate_people_politics(client, analysis, meeting_info)
        newsletter_sections['people_politics'] = people_content
    
    # 5. Executive Summary
    print("📋 Generating Executive Summary...")
    executive_summary = generate_executive_summary(client, analysis, meeting_info)
    newsletter_sections['executive_summary'] = executive_summary
    
    # Display and save results
    display_newsletter_content(newsletter_sections, meeting_info)
    save_newsletter_content(newsletter_sections, meeting_info)
    
    print("✅ Newsletter content generation completed!")
    return newsletter_sections

def generate_project_pipeline(client, analysis, meeting_info):
    """Generate Project Pipeline section"""
    projects = analysis.get('projects', [])
    
    prompt = f"""
Write a professional "Project Pipeline" section for the Triangle Development Digest newsletter.

Meeting: {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}

Projects to cover:
{json.dumps(projects, indent=2)}

Style Guidelines:
- Professional but accessible tone
- Focus on actionable intelligence for developers
- Include specific project details (addresses, developers, timelines)
- Highlight vote outcomes and next steps
- 150-250 words
- Use bullet points for key details

Format as a complete newsletter section with a compelling headline.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional newsletter writer for Triangle development professionals."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating project pipeline content: {str(e)}"

def generate_market_intelligence(client, analysis, meeting_info):
    """Generate Market Intelligence section"""
    
    prompt = f"""
Write a "Market Intelligence" section for the Triangle Development Digest newsletter.

Meeting: {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}

Analysis Data:
{json.dumps(analysis, indent=2)}

Focus on:
- Development trends observed in this meeting
- Commissioner attitudes toward development
- Opposition patterns and community concerns
- Process insights that affect project timelines
- Strategic implications for developers

Style: Insightful analysis that helps developers understand the political and market landscape.
Length: 150-200 words
Include a compelling headline.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a market analyst specializing in Triangle area development trends."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating market intelligence content: {str(e)}"

def generate_regulatory_watch(client, analysis, meeting_info):
    """Generate Regulatory Watch section"""
    
    prompt = f"""
Write a "Regulatory Watch" section for the Triangle Development Digest newsletter.

Meeting: {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}

Analysis Data:
{json.dumps(analysis, indent=2)}

Focus on:
- Process changes or improvements mentioned
- New requirements or conditions being imposed
- Staff recommendation patterns
- Timeline and deadline insights
- Regulatory efficiency observations

If no major regulatory changes were discussed, focus on process insights and timing observations that would help developers navigate the system more effectively.

Style: Practical guidance for development professionals
Length: 100-150 words
Include headline focused on regulatory insights.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a regulatory affairs expert focused on Triangle development processes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating regulatory watch content: {str(e)}"

def generate_people_politics(client, analysis, meeting_info):
    """Generate People & Politics section"""
    people = analysis.get('key_people', [])
    
    prompt = f"""
Write a "People & Politics" section for the Triangle Development Digest newsletter.

Meeting: {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}

Key People:
{json.dumps(people, indent=2)}

Focus on:
- Commissioner positions and voting patterns
- Staff recommendations and their success rate
- Developer/applicant strategies and presentations
- Community opposition leaders and their concerns
- Political dynamics that affect development approval

Style: Professional insider intelligence that helps developers understand the human dynamics
Length: 100-150 words
Include headline about political insights or key relationships.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a political analyst covering Triangle development and planning politics."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating people & politics content: {str(e)}"

def generate_executive_summary(client, analysis, meeting_info):
    """Generate Executive Summary section"""
    highlights = analysis.get('newsletter_highlights', [])
    
    prompt = f"""
Write an "Executive Summary" section for the Triangle Development Digest newsletter.

Meeting: {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}

Key Highlights:
{chr(10).join([f"• {highlight}" for highlight in highlights])}

Full Analysis:
{json.dumps(analysis, indent=2)}

Create a compelling executive summary that:
- Captures the most important developments for Triangle developers
- Highlights key opportunities and risks
- Provides actionable takeaways
- Sets context for the detailed sections that follow

Style: Executive briefing tone - concise but comprehensive
Length: 75-125 words
Start with a strong headline that captures the meeting's significance.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an executive briefing writer for Triangle development professionals."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating executive summary content: {str(e)}"

def display_newsletter_content(sections, meeting_info):
    """Display the generated newsletter content"""
    print("\n" + "=" * 80)
    print("📰 TRIANGLE DEVELOPMENT DIGEST - NEWSLETTER CONTENT")
    print("=" * 80)
    
    print(f"\n📅 {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}")
    print("-" * 60)
    
    # Show sections in logical order
    section_order = [
        ('executive_summary', '📋 EXECUTIVE SUMMARY'),
        ('project_pipeline', '🏗️ PROJECT PIPELINE'),
        ('market_intelligence', '📊 MARKET INTELLIGENCE'),
        ('regulatory_watch', '📋 REGULATORY WATCH'),
        ('people_politics', '👥 PEOPLE & POLITICS')
    ]
    
    for key, title in section_order:
        if key in sections and sections[key]:
            print(f"\n{title}")
            print("-" * 40)
            print(sections[key])
            print()

def save_newsletter_content(sections, meeting_info):
    """Save newsletter content to files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    jurisdiction = meeting_info.get('jurisdiction', 'triangle').lower()
    
    # Save complete newsletter
    newsletter_file = f"newsletter_{jurisdiction}_{timestamp}.md"
    
    with open(newsletter_file, 'w', encoding='utf-8') as f:
        f.write(f"# Triangle Development Digest\n\n")
        f.write(f"## {meeting_info.get('jurisdiction')} {meeting_info.get('type')} - {meeting_info.get('date')}\n\n")
        
        section_order = [
            ('executive_summary', '## Executive Summary'),
            ('project_pipeline', '## Project Pipeline'),
            ('market_intelligence', '## Market Intelligence'), 
            ('regulatory_watch', '## Regulatory Watch'),
            ('people_politics', '## People & Politics')
        ]
        
        for key, title in section_order:
            if key in sections and sections[key]:
                f.write(f"{title}\n\n")
                f.write(f"{sections[key]}\n\n")
                f.write("---\n\n")
        
        f.write(f"*Generated by PermitRDU AI on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*\n")
    
    print(f"💾 Complete newsletter saved to: {newsletter_file}")

def main():
    """
    Generate newsletter content from the most recent analysis
    """
    # Use the analysis file we just created
    analysis_file = "analysis_raleigh_20250812_145741.json"
    
    print("🚀 PermitRDU Newsletter Generator")
    print("Transforming meeting analysis into professional newsletter content")
    print()
    
    result = generate_newsletter_content(analysis_file)
    
    if result:
        print("\n🎉 Newsletter content generated successfully!")
        print("📈 Ready for publication in Triangle Development Digest!")
        print(f"💰 Estimated cost: ~$0.15-0.30 for content generation")
    else:
        print("\n❌ Newsletter generation failed")

if __name__ == "__main__":
    main()