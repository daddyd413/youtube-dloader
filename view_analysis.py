import json

# Load and display the analysis results
with open('analysis_raleigh_20250812_145741.json', 'r') as f:
    data = json.load(f)

print('🏗️ TRIANGLE DEVELOPMENT INTELLIGENCE EXTRACTED')
print('=' * 60)

# Meeting Info
meeting = data.get('meeting_info', {})
print(f"📅 Meeting: {meeting.get('jurisdiction')} {meeting.get('type')}")
print(f"📆 Date: {meeting.get('date')}")
print()

# Projects
analysis = data.get('analysis', {})
projects = analysis.get('projects', [])

if projects:
    print(f"🏗️ DEVELOPMENT PROJECTS FOUND: {len(projects)}")
    print('=' * 60)
    
    for i, project in enumerate(projects, 1):
        print(f"\n📍 PROJECT {i}:")
        print(f"   Name: {project.get('name', 'Unknown')}")
        print(f"   Address: {project.get('address', 'TBD')}")
        print(f"   Case Number: {project.get('case_number', 'N/A')}")
        print(f"   Type: {project.get('project_type', 'Unknown')}")
        print(f"   Status: {project.get('current_status', 'Unknown')}")
        print(f"   Vote: {project.get('vote_outcome', 'No vote')} ({project.get('vote_details', '')})")
        print(f"   Size: {project.get('acreage', 'Not specified')}")
        print(f"   Developer: {project.get('developer', 'Unknown')}")
        print(f"   Staff Rec: {project.get('staff_recommendation', 'Not specified')}")
        print(f"   History: {project.get('previous_action', 'None noted')}")

# Key People
people = analysis.get('key_people', [])
if people:
    print(f"\n👥 KEY PEOPLE ({len(people)}):")
    print('=' * 40)
    for person in people:
        print(f"   • {person.get('name')} ({person.get('role')})")
        if person.get('notable_positions'):
            print(f"     Position: {person.get('notable_positions')}")

# Newsletter Highlights
highlights = analysis.get('newsletter_highlights', [])
if highlights:
    print(f"\n💡 NEWSLETTER HIGHLIGHTS:")
    print('=' * 40)
    for i, highlight in enumerate(highlights, 1):
        print(f"   {i}. {highlight}")

print('\n' + '=' * 60)
print('🎉 Analysis Complete - Ready for Newsletter Generation!')