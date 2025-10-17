#!/usr/bin/env python
"""
Create Sample Practice Labs
This script creates sample practice labs for testing the hands-on learning feature.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from chat.models import LearningModule, PracticeLab

def create_sample_labs():
    """Create sample practice labs for each module"""
    print("🧪 Creating Sample Practice Labs...")
    print("=" * 60)
    
    # Get all active modules
    modules = LearningModule.objects.filter(is_active=True)
    
    for module in modules:
        print(f"\n📚 Module: {module.title}")
        
        # Create beginner lab
        lab1, created1 = PracticeLab.objects.get_or_create(
            module=module,
            slug=f'{module.slug}-basics',
            defaults={
                'title': f'{module.title} - Basics Lab',
                'description': f'Practice the fundamental concepts of {module.title} in this hands-on lab.',
                'objectives': f'''Master basic concepts
Apply fundamental techniques
Build practical skills
Test your knowledge''',
                'difficulty': 'beginner',
                'lab_type': 'interactive',
                'instructions': f'''Welcome to the {module.title} Basics Lab!

**Step 1:** Review the core concepts
- Study the foundational principles
- Understand the basic terminology
- Identify key components

**Step 2:** Set up your environment
- Install required tools
- Configure your workspace
- Verify setup

**Step 3:** Complete the exercises
- Follow along with examples
- Practice on your own
- Test your understanding

**Step 4:** Document your findings
- Take notes on key learnings
- Record any challenges faced
- Save your work for reference''',
                'hints': 'Start with the basics and build up gradually. Make sure to test each step before moving on.',
                'solution': 'The solution involves understanding the core concepts and applying them systematically.',
                'tools_required': 'Web Browser\nText Editor\nTerminal/Command Line',
                'estimated_time_minutes': 30,
                'points': 100,
                'order': 1,
                'is_active': True
            }
        )
        if created1:
            print(f"  ✅ Created: {lab1.title}")
        
        # Create intermediate lab
        lab2, created2 = PracticeLab.objects.get_or_create(
            module=module,
            slug=f'{module.slug}-challenge',
            defaults={
                'title': f'{module.title} - Challenge Lab',
                'description': f'Take on more complex challenges and scenarios in this intermediate {module.title} lab.',
                'objectives': f'''Apply advanced concepts
Solve complex problems
Develop critical thinking
Master practical scenarios''',
                'difficulty': 'intermediate',
                'lab_type': 'scenario',
                'instructions': f'''Advanced Challenge: {module.title}

**Scenario:**
You are tasked with applying your knowledge of {module.title} in a real-world scenario.

**Your Mission:**
1. Analyze the given situation
2. Identify potential security issues
3. Develop a mitigation strategy
4. Implement your solution
5. Test and verify results

**Requirements:**
- Document all findings
- Explain your reasoning
- Provide step-by-step walkthrough
- Include screenshots or logs

**Submission:**
Write up your complete analysis and solution below.''',
                'hints': 'Think about the big picture. Consider multiple approaches and choose the most effective one.',
                'solution': 'Success requires combining multiple techniques and thinking creatively about the problem.',
                'tools_required': 'Kali Linux or similar\nNetwork scanning tools\nAnalysis software',
                'estimated_time_minutes': 60,
                'points': 200,
                'order': 2,
                'is_active': True
            }
        )
        if created2:
            print(f"  ✅ Created: {lab2.title}")
        
        # Create CTF lab for some modules
        if module.slug in ['network-security', 'web-security', 'bug-bounty']:
            lab3, created3 = PracticeLab.objects.get_or_create(
                module=module,
                slug=f'{module.slug}-ctf',
                defaults={
                    'title': f'{module.title} - CTF Challenge',
                    'description': f'Capture the flag challenge for {module.title}. Find the hidden flag!',
                    'objectives': f'''Find security vulnerabilities
Exploit discovered weaknesses
Capture the flag
Document your methodology''',
                    'difficulty': 'advanced',
                    'lab_type': 'ctf',
                    'instructions': f'''CTF Challenge: {module.title}

**Objective:** Find and capture the flag!

**Instructions:**
1. Investigate the target system/application
2. Identify vulnerabilities
3. Exploit the weakness
4. Locate the flag
5. Submit: flag{{your_captured_flag}}

**Rules:**
- Document your process
- Use ethical hacking principles
- No brute-forcing
- Creative thinking encouraged

**Flag Format:** flag{{...}}

Good luck, hacker! 🏴‍☠️''',
                    'hints': 'Look for common vulnerabilities. Check the obvious places first, then dig deeper.',
                    'solution': 'Flag location and exploitation technique: [Hidden until completed]',
                    'tools_required': 'Burp Suite\nnmap\ncurl or wget\nBrowser DevTools',
                    'estimated_time_minutes': 90,
                    'points': 300,
                    'order': 3,
                    'is_active': True
                }
            )
            if created3:
                print(f"  ✅ Created: {lab3.title}")
    
    # Count total labs
    total_labs = PracticeLab.objects.filter(is_active=True).count()
    print("\n" + "=" * 60)
    print(f"🎉 Success! Created practice labs for {modules.count()} modules")
    print(f"📊 Total Active Labs: {total_labs}")
    print("\n📝 Next Steps:")
    print("1. Start server: python manage.py runserver")
    print("2. Login to admin: http://127.0.0.1:8000/admin/")
    print("3. View labs: http://127.0.0.1:8000/chat/learning/")
    print("4. Click on any module to see its practice labs!")

def main():
    """Main function"""
    try:
        create_sample_labs()
        return True
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    main()
