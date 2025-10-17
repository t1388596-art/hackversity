"""
Comprehensive Application Optimization Task
Run all optimizations and generate a complete optimization report
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
import time
import io
import sys

class Command(BaseCommand):
    help = 'Run comprehensive application optimization and generate report'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--quick',
            action='store_true',
            help='Run quick optimization (skip time-intensive operations)',
        )
        parser.add_argument(
            '--full',
            action='store_true',
            help='Run full optimization including all operations',
        )
    
    def handle(self, *args, **options):
        """Main optimization handler"""
        start_time = time.time()
        
        self.stdout.write(self.style.HTTP_INFO('🚀 Hackversity Application Optimization Suite'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'Started at: {time.strftime("%Y-%m-%d %H:%M:%S")}')
        
        is_quick = options.get('quick', False)
        is_full = options.get('full', False)
        
        if not is_quick and not is_full:
            # Default to quick optimization
            is_quick = True
        
        optimization_results = []
        
        # 1. Database Optimization
        self.stdout.write(self.style.HTTP_INFO('\\n1️⃣ Database Optimization'))
        self.stdout.write('-' * 30)
        
        try:
            if is_full:
                call_command('optimize_db', '--analyze', '--create-indexes', '--maintenance')
            else:
                call_command('optimize_db', '--analyze', '--create-indexes')
            optimization_results.append(('Database Optimization', '✅ Success'))
        except Exception as e:
            optimization_results.append(('Database Optimization', f'❌ Failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Database optimization failed: {e}'))
        
        # 2. Static Files Optimization
        self.stdout.write(self.style.HTTP_INFO('\\n2️⃣ Static Files Optimization'))
        self.stdout.write('-' * 30)
        
        try:
            if is_full:
                call_command('optimize_static', '--analyze', '--compress', '--minify')
            else:
                call_command('optimize_static', '--analyze', '--compress')
            optimization_results.append(('Static Files Optimization', '✅ Success'))
        except Exception as e:
            optimization_results.append(('Static Files Optimization', f'❌ Failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Static files optimization failed: {e}'))
        
        # 3. Performance Monitoring
        self.stdout.write(self.style.HTTP_INFO('\\n3️⃣ Performance Analysis'))
        self.stdout.write('-' * 30)
        
        try:
            call_command('monitor_performance', '--report', '--stats')
            optimization_results.append(('Performance Analysis', '✅ Success'))
        except Exception as e:
            optimization_results.append(('Performance Analysis', f'❌ Failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Performance analysis failed: {e}'))
        
        # 4. Django System Optimizations
        self.stdout.write(self.style.HTTP_INFO('\\n4️⃣ Django System Optimizations'))
        self.stdout.write('-' * 30)
        
        try:
            # Clear expired sessions
            call_command('clearsessions')
            self.stdout.write('  ✅ Expired sessions cleared')
            
            # Run Django system checks
            call_command('check', '--deploy')
            self.stdout.write('  ✅ Django system checks passed')
            
            optimization_results.append(('Django System Optimizations', '✅ Success'))
        except Exception as e:
            optimization_results.append(('Django System Optimizations', f'⚠️ Partial: {e}'))
            self.stdout.write(self.style.WARNING(f'Django optimizations partial: {e}'))
        
        # 5. Security and Configuration Review
        self.stdout.write(self.style.HTTP_INFO('\\n5️⃣ Security & Configuration Review'))
        self.stdout.write('-' * 30)
        
        try:
            self.review_security_settings()
            optimization_results.append(('Security Review', '✅ Success'))
        except Exception as e:
            optimization_results.append(('Security Review', f'❌ Failed: {e}'))
            self.stdout.write(self.style.ERROR(f'Security review failed: {e}'))
        
        # 6. Performance Recommendations
        self.stdout.write(self.style.HTTP_INFO('\\n6️⃣ Performance Recommendations'))
        self.stdout.write('-' * 30)
        
        self.generate_performance_recommendations(is_full)
        
        # 7. Generate Final Report
        end_time = time.time()
        duration = end_time - start_time
        
        self.generate_final_report(optimization_results, duration, is_quick, is_full)
    
    def review_security_settings(self):
        """Review and report on security settings"""
        security_checks = []
        
        # Debug mode check
        if settings.DEBUG:
            security_checks.append('⚠️  DEBUG=True (OK for development, disable in production)')
        else:
            security_checks.append('✅ DEBUG=False (production ready)')
        
        # Secret key check
        if len(settings.SECRET_KEY) > 30:
            security_checks.append('✅ SECRET_KEY is strong')
        else:
            security_checks.append('⚠️  SECRET_KEY should be longer and more random')
        
        # Allowed hosts check
        if settings.ALLOWED_HOSTS:
            security_checks.append(f'✅ ALLOWED_HOSTS configured ({len(settings.ALLOWED_HOSTS)} hosts)')
        else:
            security_checks.append('⚠️  ALLOWED_HOSTS not configured')
        
        # HTTPS settings check
        if hasattr(settings, 'SECURE_SSL_REDIRECT'):
            if settings.SECURE_SSL_REDIRECT:
                security_checks.append('✅ SSL redirect enabled')
            else:
                security_checks.append('⚠️  SSL redirect disabled')
        
        # Security middleware check
        security_middleware = 'django.middleware.security.SecurityMiddleware'
        if security_middleware in settings.MIDDLEWARE:
            security_checks.append('✅ Security middleware enabled')
        else:
            security_checks.append('⚠️  Security middleware not found')
        
        for check in security_checks:
            self.stdout.write(f'  {check}')
    
    def generate_performance_recommendations(self, is_full):
        """Generate performance recommendations based on current setup"""
        recommendations = []
        
        # Database recommendations
        db_engine = settings.DATABASES['default']['ENGINE']
        if 'sqlite' in db_engine:
            recommendations.append('📊 Database: Consider PostgreSQL for production')
            recommendations.append('📊 Database: Enable WAL mode for SQLite (PRAGMA journal_mode=WAL)')
        elif 'postgresql' in db_engine:
            recommendations.append('📊 Database: Excellent choice for production')
            recommendations.append('📊 Database: Consider connection pooling (pgbouncer)')
        
        # Cache recommendations
        cache_backend = settings.CACHES['default']['BACKEND']
        if 'dummy' in cache_backend.lower():
            recommendations.append('🗄️  Cache: Enable Redis or Memcached for production')
        elif 'locmem' in cache_backend.lower():
            recommendations.append('🗄️  Cache: Local memory cache OK for single server')
        else:
            recommendations.append('🗄️  Cache: External cache backend configured ✅')
        
        # Static files recommendations
        if hasattr(settings, 'STATICFILES_STORAGE'):
            if 'whitenoise' in settings.STATICFILES_STORAGE.lower():
                recommendations.append('📁 Static Files: WhiteNoise configured ✅')
            else:
                recommendations.append('📁 Static Files: Consider WhiteNoise for static file serving')
        
        # Monitoring recommendations
        recommendations.append('📊 Monitoring: Set up application performance monitoring (APM)')
        recommendations.append('📊 Monitoring: Configure error tracking (Sentry, Rollbar)')
        recommendations.append('📊 Monitoring: Set up uptime monitoring')
        
        # Performance recommendations
        recommendations.append('⚡ Performance: Use select_related() and prefetch_related() in queries')
        recommendations.append('⚡ Performance: Implement pagination for large datasets')
        recommendations.append('⚡ Performance: Add database indexes for frequently queried fields')
        recommendations.append('⚡ Performance: Use async views for I/O-bound operations')
        
        # Deployment recommendations
        recommendations.append('🚀 Deployment: Use Gunicorn with multiple workers')
        recommendations.append('🚀 Deployment: Set up reverse proxy (Nginx)')
        recommendations.append('🚀 Deployment: Enable gzip compression')
        recommendations.append('🚀 Deployment: Use CDN for static files')
        
        self.stdout.write('\\n💡 Recommended Optimizations:')
        for i, rec in enumerate(recommendations[:15], 1):  # Show top 15 recommendations
            self.stdout.write(f'  {i:2d}. {rec}')
        
        if len(recommendations) > 15:
            self.stdout.write(f'     ... and {len(recommendations) - 15} more recommendations')
    
    def generate_final_report(self, optimization_results, duration, is_quick, is_full):
        """Generate final optimization report"""
        self.stdout.write(self.style.HTTP_INFO('\\n📋 Optimization Summary Report'))
        self.stdout.write('=' * 60)
        
        # Optimization mode
        mode = 'Quick' if is_quick else 'Full' if is_full else 'Default'
        self.stdout.write(f'Optimization Mode: {mode}')
        self.stdout.write(f'Total Duration: {duration:.1f} seconds')
        self.stdout.write(f'Completed at: {time.strftime("%Y-%m-%d %H:%M:%S")}')
        
        # Results summary
        success_count = sum(1 for _, result in optimization_results if '✅' in result)
        warning_count = sum(1 for _, result in optimization_results if '⚠️' in result)
        error_count = sum(1 for _, result in optimization_results if '❌' in result)
        
        self.stdout.write(f'\\n📊 Results Summary:')
        self.stdout.write(f'  ✅ Successful: {success_count}')
        self.stdout.write(f'  ⚠️  Warnings: {warning_count}')
        self.stdout.write(f'  ❌ Errors: {error_count}')
        
        # Detailed results
        self.stdout.write(f'\\n📝 Detailed Results:')
        for operation, result in optimization_results:
            self.stdout.write(f'  {operation}: {result}')
        
        # Success rate
        total_operations = len(optimization_results)
        if total_operations > 0:
            success_rate = (success_count / total_operations) * 100
            self.stdout.write(f'\\n🎯 Success Rate: {success_rate:.1f}%')
            
            if success_rate >= 90:
                self.stdout.write(self.style.SUCCESS('🎉 Excellent! Your application is highly optimized.'))
            elif success_rate >= 70:
                self.stdout.write(self.style.SUCCESS('👍 Good! Your application is well optimized.'))
            elif success_rate >= 50:
                self.stdout.write(self.style.WARNING('⚠️  Fair. Consider addressing the issues for better performance.'))
            else:
                self.stdout.write(self.style.ERROR('❌ Poor. Multiple issues need attention for optimal performance.'))
        
        # Next steps
        self.stdout.write(f'\\n🔄 Next Steps:')
        next_steps = [
            'Monitor application performance regularly',
            'Set up automated performance testing',
            'Review and update dependencies regularly',
            'Implement continuous optimization practices',
            'Set up alerts for performance degradation',
        ]
        
        for i, step in enumerate(next_steps, 1):
            self.stdout.write(f'  {i}. {step}')
        
        # Command suggestions
        self.stdout.write(f'\\n💻 Useful Commands:')
        commands = [
            'python manage.py optimize_db --maintenance  # Database maintenance',
            'python manage.py optimize_static --compress  # Compress static files',
            'python manage.py monitor_performance --report  # Performance report',
            'python manage.py check --deploy  # Django deployment check',
            'python manage.py optimize_application --full  # Full optimization',
        ]
        
        for cmd in commands:
            self.stdout.write(f'  {cmd}')
        
        self.stdout.write('\\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('🚀 Application optimization completed!'))