from django.core.management.base import BaseCommand
from chat.models import LearningModule, LearningVideo


class Command(BaseCommand):
    help = 'Create initial learning modules and videos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating initial learning modules...'))
        
        # Create Getting Started module
        getting_started, created = LearningModule.objects.get_or_create(
            slug='getting-started',
            defaults={
                'title': 'Getting Started',
                'description': 'Learn the fundamentals of cybersecurity and ethical hacking',
                'icon': 'fas fa-seedling',
                'order': 1
            }
        )
        
        if created:
            # Add videos for Getting Started
            videos_data = [
                {'title': 'Introduction to Cybersecurity', 'youtube_id': 'ePD7cLWkt-E', 'duration': 15, 'order': 1},
                {'title': 'Types of Cyber Threats', 'youtube_id': 'inWWhr5tnEA', 'duration': 20, 'order': 2},
                {'title': 'Basic Security Principles', 'youtube_id': 'U_P23SqJaDc', 'duration': 25, 'order': 3},
                {'title': 'Ethical Hacking Fundamentals', 'youtube_id': 'inWWhr5tnEA', 'duration': 30, 'order': 4},
            ]
            
            for video_data in videos_data:
                LearningVideo.objects.create(
                    module=getting_started,
                    title=video_data['title'],
                    youtube_id=video_data['youtube_id'],
                    duration_minutes=video_data['duration'],
                    order=video_data['order']
                )
        
        # Create Network Security module
        network_security, created = LearningModule.objects.get_or_create(
            slug='network-security',
            defaults={
                'title': 'Network Security',
                'description': 'Understand network protocols, scanning, and penetration testing',
                'icon': 'fas fa-network-wired',
                'order': 2
            }
        )
        
        if created:
            videos_data = [
                {'title': 'Network Protocols Overview', 'youtube_id': 'inWWhr5tnEA', 'duration': 25, 'order': 1},
                {'title': 'Network Scanning Techniques', 'youtube_id': '3Kq1MIfTWCE', 'duration': 35, 'order': 2},
                {'title': 'Vulnerability Assessment', 'youtube_id': 'qPmKzI6U9IY', 'duration': 40, 'order': 3},
                {'title': 'Penetration Testing Methods', 'youtube_id': 'fKuqYQdqRIs', 'duration': 45, 'order': 4},
            ]
            
            for video_data in videos_data:
                LearningVideo.objects.create(
                    module=network_security,
                    title=video_data['title'],
                    youtube_id=video_data['youtube_id'],
                    duration_minutes=video_data['duration'],
                    order=video_data['order']
                )
        
        # Create Web Security module
        web_security, created = LearningModule.objects.get_or_create(
            slug='web-security',
            defaults={
                'title': 'Web Application Security',
                'description': 'Learn about OWASP Top 10, XSS, SQL injection and secure coding',
                'icon': 'fas fa-globe',
                'order': 3
            }
        )
        
        if created:
            videos_data = [
                {'title': 'OWASP Top 10 Vulnerabilities', 'youtube_id': 'VufzQOuJTjQ', 'duration': 30, 'order': 1},
                {'title': 'SQL Injection Attacks', 'youtube_id': '_jKylhJtPmI', 'duration': 35, 'order': 2},
                {'title': 'Cross-Site Scripting (XSS)', 'youtube_id': 'EoaDgUgS6QA', 'duration': 30, 'order': 3},
                {'title': 'Secure Coding Practices', 'youtube_id': 'w9F4mpuoHUU', 'duration': 40, 'order': 4},
            ]
            
            for video_data in videos_data:
                LearningVideo.objects.create(
                    module=web_security,
                    title=video_data['title'],
                    youtube_id=video_data['youtube_id'],
                    duration_minutes=video_data['duration'],
                    order=video_data['order']
                )
        
        # Create Bug Bounty module
        bug_bounty, created = LearningModule.objects.get_or_create(
            slug='bug-bounty',
            defaults={
                'title': 'Bug Bounty Hunting',
                'description': 'Master bug bounty methodology, reconnaissance, and ethical reporting',
                'icon': 'fas fa-bug',
                'order': 4
            }
        )
        
        if created:
            videos_data = [
                {'title': 'Bug Bounty Methodology', 'youtube_id': 'p4JgIu1mceI', 'duration': 25, 'order': 1},
                {'title': 'Reconnaissance Techniques', 'youtube_id': 'uKWu6yhnhbQ', 'duration': 40, 'order': 2},
                {'title': 'Vulnerability Discovery', 'youtube_id': 'gd6QLYH5F5E', 'duration': 45, 'order': 3},
                {'title': 'Report Writing & Ethics', 'youtube_id': 'Rp69edBmFFo', 'duration': 20, 'order': 4},
            ]
            
            for video_data in videos_data:
                LearningVideo.objects.create(
                    module=bug_bounty,
                    title=video_data['title'],
                    youtube_id=video_data['youtube_id'],
                    duration_minutes=video_data['duration'],
                    order=video_data['order']
                )
        
        # Create Digital Forensics module
        digital_forensics, created = LearningModule.objects.get_or_create(
            slug='digital-forensics',
            defaults={
                'title': 'Digital Forensics',
                'description': 'Learn digital evidence handling, file analysis, and memory forensics',
                'icon': 'fas fa-search',
                'order': 5
            }
        )
        
        if created:
            videos_data = [
                {'title': 'Digital Evidence Handling', 'youtube_id': 'G2s7vTXXMPY', 'duration': 30, 'order': 1},
                {'title': 'File System Analysis', 'youtube_id': 'o8NPllzkFhE', 'duration': 40, 'order': 2},
                {'title': 'Memory Forensics', 'youtube_id': 'BMFCdAGxVN4', 'duration': 35, 'order': 3},
                {'title': 'Network Traffic Analysis', 'youtube_id': 'p7-o298fu0c', 'duration': 45, 'order': 4},
            ]
            
            for video_data in videos_data:
                LearningVideo.objects.create(
                    module=digital_forensics,
                    title=video_data['title'],
                    youtube_id=video_data['youtube_id'],
                    duration_minutes=video_data['duration'],
                    order=video_data['order']
                )
        
        # Create Advanced Security module
        advanced_security, created = LearningModule.objects.get_or_create(
            slug='advanced-security',
            defaults={
                'title': 'Advanced Security',
                'description': 'Advanced penetration testing, red team operations, and exploit development',
                'icon': 'fas fa-shield-alt',
                'order': 6
            }
        )
        
        if created:
            videos_data = [
                {'title': 'Advanced Penetration Testing', 'youtube_id': 'x4bTteXjiuw', 'duration': 60, 'order': 1},
                {'title': 'Red Team Operations', 'youtube_id': 'qOYyJu_tJFE', 'duration': 50, 'order': 2},
                {'title': 'Advanced Persistent Threats', 'youtube_id': '6tzq7lQrNkg', 'duration': 45, 'order': 3},
                {'title': 'Exploit Development', 'youtube_id': 'vAKkBan-6iM', 'duration': 90, 'order': 4},
            ]
            
            for video_data in videos_data:
                LearningVideo.objects.create(
                    module=advanced_security,
                    title=video_data['title'],
                    youtube_id=video_data['youtube_id'],
                    duration_minutes=video_data['duration'],
                    order=video_data['order']
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully created learning modules and videos!'))
        self.stdout.write(self.style.SUCCESS('You can now manage videos through the Django admin at /admin/'))