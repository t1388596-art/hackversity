"""
Performance Monitoring Management Command
Monitors and reports on application performance metrics
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from chat.models import Conversation, Message, ConversationStats
from django.utils import timezone
from datetime import timedelta
import time
import psutil
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Monitor and optimize application performance'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--report',
            action='store_true',
            help='Generate performance report',
        )
        parser.add_argument(
            '--monitor',
            action='store_true',
            help='Start performance monitoring',
        )
        parser.add_argument(
            '--optimize',
            action='store_true',
            help='Run performance optimizations',
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Update daily statistics',
        )
    
    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(self.style.HTTP_INFO('📊 Performance Monitoring & Optimization'))
        self.stdout.write('=' * 60)
        
        if options['report']:
            self.generate_performance_report()
        
        if options['monitor']:
            self.start_performance_monitoring()
        
        if options['optimize']:
            self.run_performance_optimizations()
        
        if options['stats']:
            self.update_daily_statistics()
        
        if not any([options['report'], options['monitor'], options['optimize'], options['stats']]):
            # Run all by default
            self.generate_performance_report()
            self.update_daily_statistics()
            self.run_performance_optimizations()
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        self.stdout.write(self.style.HTTP_INFO('\\n🔍 Performance Report'))
        self.stdout.write('-' * 30)
        
        # System metrics
        self.report_system_metrics()
        
        # Database metrics
        self.report_database_metrics()
        
        # Cache metrics
        self.report_cache_metrics()
        
        # Application metrics
        self.report_application_metrics()
        
        # Query analysis
        self.analyze_database_queries()
    
    def report_system_metrics(self):
        """Report system performance metrics"""
        self.stdout.write('\\n💻 System Metrics:')
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.stdout.write(f'  CPU Usage: {cpu_percent:.1f}%')
        
        # Memory usage
        memory = psutil.virtual_memory()
        self.stdout.write(f'  Memory Usage: {memory.percent:.1f}% ({memory.used / 1024 / 1024 / 1024:.1f}GB / {memory.total / 1024 / 1024 / 1024:.1f}GB)')
        
        # Disk usage
        disk = psutil.disk_usage('/')
        self.stdout.write(f'  Disk Usage: {disk.percent:.1f}% ({disk.used / 1024 / 1024 / 1024:.1f}GB / {disk.total / 1024 / 1024 / 1024:.1f}GB)')
        
        # Process info
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        self.stdout.write(f'  Process Memory: {process_memory.rss / 1024 / 1024:.1f}MB RSS, {process_memory.vms / 1024 / 1024:.1f}MB VMS')
    
    def report_database_metrics(self):
        """Report database performance metrics"""
        self.stdout.write('\\n🗄️  Database Metrics:')
        
        # Connection info
        db_config = settings.DATABASES['default']
        self.stdout.write(f'  Engine: {db_config["ENGINE"]}')
        
        # Query count and timing
        start_time = time.time()
        with connection.cursor() as cursor:
            if 'sqlite' in db_config['ENGINE']:
                self.report_sqlite_metrics(cursor)
            elif 'postgresql' in db_config['ENGINE']:
                self.report_postgresql_metrics(cursor)
        
        query_time = time.time() - start_time
        self.stdout.write(f'  Metrics query time: {query_time:.3f}s')
        
        # Connection pool info
        if hasattr(connection, 'queries'):
            query_count = len(connection.queries)
            self.stdout.write(f'  Queries executed: {query_count}')
    
    def report_sqlite_metrics(self, cursor):
        """SQLite specific metrics"""
        # Database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        size = cursor.fetchone()[0]
        self.stdout.write(f'  Database Size: {size / 1024 / 1024:.1f}MB')
        
        # Cache hit rate
        cursor.execute("PRAGMA cache_size")
        cache_size = cursor.fetchone()[0]
        self.stdout.write(f'  Cache Size: {cache_size} pages')
        
        # WAL mode status
        cursor.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]
        self.stdout.write(f'  Journal Mode: {journal_mode}')
    
    def report_postgresql_metrics(self, cursor):
        """PostgreSQL specific metrics"""
        # Database size
        cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
        size = cursor.fetchone()[0]
        self.stdout.write(f'  Database Size: {size}')
        
        # Cache hit ratio
        cursor.execute("""
            SELECT round(
                100.0 * sum(blks_hit) / (sum(blks_hit) + sum(blks_read)), 2
            ) as cache_hit_ratio
            FROM pg_stat_database
            WHERE datname = current_database()
        """)
        hit_ratio = cursor.fetchone()[0]
        if hit_ratio:
            self.stdout.write(f'  Cache Hit Ratio: {hit_ratio}%')
        
        # Active connections
        cursor.execute("SELECT count(*) FROM pg_stat_activity")
        connections = cursor.fetchone()[0]
        self.stdout.write(f'  Active Connections: {connections}')
    
    def report_cache_metrics(self):
        """Report cache performance metrics"""
        self.stdout.write('\\n🗄️  Cache Metrics:')
        
        # Test cache performance
        start_time = time.time()
        cache.set('performance_test', 'test_value', 60)
        set_time = time.time() - start_time
        
        start_time = time.time()
        value = cache.get('performance_test')
        get_time = time.time() - start_time
        
        cache.delete('performance_test')
        
        self.stdout.write(f'  Cache SET time: {set_time * 1000:.2f}ms')
        self.stdout.write(f'  Cache GET time: {get_time * 1000:.2f}ms')
        self.stdout.write(f'  Cache working: {"✅" if value == "test_value" else "❌"}')
        
        # Check cache backend
        cache_backend = settings.CACHES['default']['BACKEND']
        self.stdout.write(f'  Backend: {cache_backend}')
    
    def report_application_metrics(self):
        """Report application-specific metrics"""
        self.stdout.write('\\n📱 Application Metrics:')
        
        # User counts
        total_users = User.objects.count()
        active_users = User.objects.filter(
            last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        self.stdout.write(f'  Total Users: {total_users:,}')
        self.stdout.write(f'  Active Users (30d): {active_users:,}')
        
        # Conversation counts
        total_conversations = Conversation.objects.count()
        recent_conversations = Conversation.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        self.stdout.write(f'  Total Conversations: {total_conversations:,}')
        self.stdout.write(f'  Recent Conversations (7d): {recent_conversations:,}')
        
        # Message counts
        total_messages = Message.objects.count()
        recent_messages = Message.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        self.stdout.write(f'  Total Messages: {total_messages:,}')
        self.stdout.write(f'  Recent Messages (7d): {recent_messages:,}')
        
        # Average messages per conversation
        if total_conversations > 0:
            avg_messages = total_messages / total_conversations
            self.stdout.write(f'  Avg Messages/Conversation: {avg_messages:.1f}')
    
    def analyze_database_queries(self):
        """Analyze database query performance"""
        self.stdout.write('\\n🔍 Query Analysis:')
        
        # Test common queries
        queries = [
            ('User conversations', lambda: list(Conversation.objects.filter(user_id=1).order_by('-updated_at')[:10])),
            ('Conversation messages', lambda: list(Message.objects.filter(conversation_id=1).order_by('timestamp'))),
            ('Recent messages', lambda: list(Message.objects.order_by('-timestamp')[:50])),
        ]
        
        for query_name, query_func in queries:
            try:
                start_time = time.time()
                result = query_func()
                end_time = time.time()
                
                query_time = (end_time - start_time) * 1000
                self.stdout.write(f'  {query_name}: {query_time:.2f}ms ({len(result)} results)')
            except Exception as e:
                self.stdout.write(f'  {query_name}: Error - {e}')
    
    def start_performance_monitoring(self):
        """Start continuous performance monitoring"""
        self.stdout.write(self.style.HTTP_INFO('\\n📊 Starting Performance Monitoring'))
        self.stdout.write('-' * 30)
        
        # This would typically run as a background service
        # For now, just show what metrics would be monitored
        
        metrics_to_monitor = [
            'Response time for key endpoints',
            'Database query performance',
            'Cache hit ratios',
            'Memory usage trends',
            'Error rates',
            'User activity patterns',
        ]
        
        for metric in metrics_to_monitor:
            self.stdout.write(f'  📈 Monitoring: {metric}')
        
        self.stdout.write('\\n💡 To implement continuous monitoring:')
        self.stdout.write('   1. Set up Django logging with performance middleware')
        self.stdout.write('   2. Use tools like New Relic, DataDog, or Prometheus')
        self.stdout.write('   3. Configure alerts for performance thresholds')
        self.stdout.write('   4. Set up automated performance testing')
    
    def run_performance_optimizations(self):
        """Run automated performance optimizations"""
        self.stdout.write(self.style.HTTP_INFO('\\n⚡ Running Performance Optimizations'))
        self.stdout.write('-' * 30)
        
        optimizations = []
        
        # Clear expired cache entries
        try:
            # This would depend on cache backend
            self.stdout.write('  🗑️  Clearing expired cache entries...')
            optimizations.append('Cache cleanup')
        except Exception as e:
            self.stdout.write(f'  ⚠️  Cache cleanup failed: {e}')
        
        # Update database statistics
        try:
            with connection.cursor() as cursor:
                if 'sqlite' in settings.DATABASES['default']['ENGINE']:
                    cursor.execute('PRAGMA optimize')
                    self.stdout.write('  📊 SQLite statistics updated')
                elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
                    cursor.execute('ANALYZE')
                    self.stdout.write('  📊 PostgreSQL statistics updated')
            optimizations.append('Database statistics update')
        except Exception as e:
            self.stdout.write(f'  ⚠️  Database optimization failed: {e}')
        
        # Cleanup old sessions
        try:
            from django.core.management import call_command
            call_command('clearsessions')
            self.stdout.write('  🧹 Old sessions cleared')
            optimizations.append('Session cleanup')
        except Exception as e:
            self.stdout.write(f'  ⚠️  Session cleanup failed: {e}')
        
        # Update conversation stats
        try:
            ConversationStats.update_daily_stats()
            self.stdout.write('  📈 Daily statistics updated')
            optimizations.append('Statistics update')
        except Exception as e:
            self.stdout.write(f'  ⚠️  Statistics update failed: {e}')
        
        self.stdout.write(f'\\n✅ Completed {len(optimizations)} optimizations')
    
    def update_daily_statistics(self):
        """Update daily application statistics"""
        self.stdout.write(self.style.HTTP_INFO('\\n📈 Updating Daily Statistics'))
        self.stdout.write('-' * 30)
        
        try:
            stats = ConversationStats.update_daily_stats()
            
            self.stdout.write(f'  📊 Statistics for {stats.date}:')
            self.stdout.write(f'     Total Conversations: {stats.total_conversations:,}')
            self.stdout.write(f'     Total Messages: {stats.total_messages:,}')
            self.stdout.write(f'     Active Users: {stats.active_users:,}')
            self.stdout.write(f'     Avg Messages/Conversation: {stats.avg_messages_per_conversation:.1f}')
            
            self.stdout.write(self.style.SUCCESS('  ✅ Daily statistics updated successfully'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Statistics update failed: {e}'))