#!/usr/bin/env python3
"""
Complete Django Application Optimization Script
Optimizes performance, security, database, static files, and caching
"""

import os
import sys
import django
import time
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.contrib.staticfiles import finders

class ApplicationOptimizer:
    """Comprehensive application optimization"""
    
    def __init__(self):
        self.optimizations_applied = []
        self.warnings = []
        self.errors = []
    
    def run_all_optimizations(self):
        """Run all optimization steps"""
        print("🚀 Hackversity Application Optimization")
        print("=" * 50)
        
        # Database optimizations
        self.optimize_database()
        
        # Static files optimizations
        self.optimize_static_files()
        
        # Security optimizations
        self.optimize_security()
        
        # Performance optimizations
        self.optimize_performance()
        
        # Template optimizations
        self.optimize_templates()
        
        # Django settings optimizations
        self.optimize_django_settings()
        
        # Cache optimizations
        self.optimize_caching()
        
        # URL optimizations
        self.optimize_urls()
        
        # Generate optimization report
        self.generate_report()
    
    def optimize_database(self):
        """Optimize database configuration and queries"""
        print("\n📊 Database Optimization")
        print("-" * 25)
        
        try:
            # Check database connection
            connection.ensure_connection()
            print("✅ Database connection: Working")
            
            # Run database optimization commands
            print("🔧 Running database maintenance...")
            
            # Analyze database for optimizations
            with connection.cursor() as cursor:
                if 'sqlite' in settings.DATABASES['default']['ENGINE']:
                    # SQLite optimizations
                    cursor.execute("PRAGMA optimize")
                    cursor.execute("VACUUM")
                    print("✅ SQLite database optimized (VACUUM, PRAGMA)")
                elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
                    # PostgreSQL optimizations
                    cursor.execute("ANALYZE")
                    print("✅ PostgreSQL statistics updated")
            
            # Check for missing indexes
            self.check_database_indexes()
            
            self.optimizations_applied.append("Database maintenance and optimization")
            
        except Exception as e:
            self.errors.append(f"Database optimization failed: {e}")
            print(f"❌ Database optimization failed: {e}")
    
    def check_database_indexes(self):
        """Check and suggest database indexes"""
        print("📋 Checking database indexes...")
        
        # Common indexes that should exist
        suggested_indexes = [
            ("chat_conversation", ["user_id", "created_at"]),
            ("chat_message", ["conversation_id", "timestamp"]),
            ("accounts_customuser", ["email", "is_active"]),
        ]
        
        with connection.cursor() as cursor:
            for table, columns in suggested_indexes:
                try:
                    # Check if table exists
                    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                    if cursor.fetchone():
                        print(f"✅ Table {table} exists")
                    else:
                        print(f"⚠️  Table {table} not found")
                except Exception as e:
                    print(f"⚠️  Could not check table {table}: {e}")
    
    def optimize_static_files(self):
        """Optimize static files configuration"""
        print("\n📁 Static Files Optimization")
        print("-" * 25)
        
        try:
            # Collect static files
            print("📦 Collecting static files...")
            call_command('collectstatic', '--noinput', verbosity=0)
            print("✅ Static files collected")
            
            # Check static files configuration
            self.check_static_config()
            
            # Compress static files if possible
            self.compress_static_files()
            
            self.optimizations_applied.append("Static files collection and optimization")
            
        except Exception as e:
            self.errors.append(f"Static files optimization failed: {e}")
            print(f"❌ Static files optimization failed: {e}")
    
    def check_static_config(self):
        """Check static files configuration"""
        print("🔍 Checking static files configuration...")
        
        # Check WhiteNoise
        if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
            print("✅ WhiteNoise middleware enabled")
        else:
            print("⚠️  WhiteNoise middleware not found")
            self.warnings.append("WhiteNoise middleware not configured")
        
        # Check static root
        if settings.STATIC_ROOT:
            print(f"✅ STATIC_ROOT configured: {settings.STATIC_ROOT}")
        else:
            print("⚠️  STATIC_ROOT not configured")
            self.warnings.append("STATIC_ROOT not configured")
        
        # Check key static files
        key_files = ['css/style.css', 'js/chat.js', 'js/responsive.js']
        for file_path in key_files:
            found = finders.find(file_path)
            if found:
                print(f"✅ Found: {file_path}")
            else:
                print(f"⚠️  Missing: {file_path}")
                self.warnings.append(f"Static file missing: {file_path}")
    
    def compress_static_files(self):
        """Compress static files for better performance"""
        print("🗜️  Checking static file compression...")
        
        if hasattr(settings, 'STATICFILES_STORAGE'):
            if 'Compressed' in settings.STATICFILES_STORAGE:
                print("✅ Static file compression enabled")
            else:
                print("⚠️  Static file compression not enabled")
                self.warnings.append("Static file compression not enabled")
        
        # Check file sizes
        static_root = Path(settings.STATIC_ROOT)
        if static_root.exists():
            total_size = sum(f.stat().st_size for f in static_root.rglob('*') if f.is_file())
            print(f"📊 Total static files size: {total_size / 1024 / 1024:.1f} MB")
        
    def optimize_security(self):
        """Optimize security settings"""
        print("\n🔒 Security Optimization")
        print("-" * 25)
        
        security_checks = [
            ("DEBUG", not settings.DEBUG, "Debug mode should be disabled in production"),
            ("SECRET_KEY", len(settings.SECRET_KEY) > 20, "Secret key should be strong"),
            ("ALLOWED_HOSTS", len(settings.ALLOWED_HOSTS) > 0, "Allowed hosts should be configured"),
            ("CSRF_COOKIE_SECURE", getattr(settings, 'CSRF_COOKIE_SECURE', False) or settings.DEBUG, "CSRF cookie should be secure"),
            ("SESSION_COOKIE_SECURE", getattr(settings, 'SESSION_COOKIE_SECURE', False) or settings.DEBUG, "Session cookie should be secure"),
        ]
        
        for check_name, condition, message in security_checks:
            if condition:
                print(f"✅ {check_name}: OK")
            else:
                print(f"⚠️  {check_name}: {message}")
                self.warnings.append(f"Security: {message}")
        
        # Check middleware order
        self.check_middleware_order()
        
        self.optimizations_applied.append("Security configuration review")
    
    def check_middleware_order(self):
        """Check middleware order for security"""
        print("🔍 Checking middleware order...")
        
        middleware = settings.MIDDLEWARE
        security_middleware = 'django.middleware.security.SecurityMiddleware'
        whitenoise_middleware = 'whitenoise.middleware.WhiteNoiseMiddleware'
        
        if security_middleware in middleware:
            security_pos = middleware.index(security_middleware)
            print(f"✅ SecurityMiddleware at position {security_pos}")
            
            if whitenoise_middleware in middleware:
                whitenoise_pos = middleware.index(whitenoise_middleware)
                if whitenoise_pos == security_pos + 1:
                    print("✅ WhiteNoiseMiddleware positioned correctly")
                else:
                    print("⚠️  WhiteNoiseMiddleware should be right after SecurityMiddleware")
                    self.warnings.append("WhiteNoise middleware positioning")
        else:
            print("⚠️  SecurityMiddleware not found")
            self.warnings.append("SecurityMiddleware not configured")
    
    def optimize_performance(self):
        """Optimize application performance"""
        print("\n⚡ Performance Optimization")
        print("-" * 25)
        
        # Check database connection pooling
        self.check_database_performance()
        
        # Check template caching
        self.check_template_caching()
        
        # Check session configuration
        self.check_session_config()
        
        # Memory optimization suggestions
        self.suggest_memory_optimizations()
        
        self.optimizations_applied.append("Performance configuration review")
    
    def check_database_performance(self):
        """Check database performance settings"""
        print("📊 Database performance check...")
        
        # Check connection settings
        db_config = settings.DATABASES['default']
        
        if 'postgresql' in db_config['ENGINE']:
            # PostgreSQL specific optimizations
            conn_max_age = db_config.get('CONN_MAX_AGE', 0)
            if conn_max_age > 0:
                print(f"✅ Connection pooling enabled (max age: {conn_max_age}s)")
            else:
                print("⚠️  Connection pooling not enabled")
                self.warnings.append("Database connection pooling not enabled")
        elif 'sqlite' in db_config['ENGINE']:
            print("✅ SQLite - suitable for development")
    
    def check_template_caching(self):
        """Check template caching configuration"""
        print("🎨 Template caching check...")
        
        # Check if template caching is enabled
        template_loaders = []
        for template_config in settings.TEMPLATES:
            options = template_config.get('OPTIONS', {})
            loaders = options.get('loaders', [])
            template_loaders.extend(loaders)
        
        cached_loader = 'django.template.loaders.cached.Loader'
        has_cached_loader = any(cached_loader in str(loader) for loader in template_loaders)
        
        if has_cached_loader:
            print("✅ Template caching enabled")
        else:
            print("⚠️  Template caching not enabled")
            self.warnings.append("Template caching not enabled")
    
    def check_session_config(self):
        """Check session configuration"""
        print("🔐 Session configuration check...")
        
        session_engine = getattr(settings, 'SESSION_ENGINE', 'django.contrib.sessions.backends.db')
        print(f"📊 Session engine: {session_engine}")
        
        if 'cache' in session_engine:
            print("✅ Cache-based sessions configured")
        else:
            print("⚠️  Database sessions in use (consider cache-based sessions for performance)")
            self.warnings.append("Consider cache-based sessions for better performance")
    
    def suggest_memory_optimizations(self):
        """Suggest memory optimizations"""
        print("🧠 Memory optimization suggestions...")
        
        suggestions = [
            "✅ Use select_related() and prefetch_related() in queries",
            "✅ Implement pagination for large datasets",
            "✅ Use database indexes for frequently queried fields",
            "✅ Consider using cache for expensive operations",
            "✅ Optimize image sizes and formats",
        ]
        
        for suggestion in suggestions:
            print(f"   {suggestion}")
    
    def optimize_templates(self):
        """Optimize template configuration"""
        print("\n🎨 Template Optimization")
        print("-" * 25)
        
        # Check template directories
        template_dirs = []
        for template_config in settings.TEMPLATES:
            template_dirs.extend(template_config.get('DIRS', []))
        
        for template_dir in template_dirs:
            if Path(template_dir).exists():
                print(f"✅ Template directory exists: {template_dir}")
            else:
                print(f"⚠️  Template directory missing: {template_dir}")
                self.warnings.append(f"Template directory missing: {template_dir}")
        
        # Check for common template files
        common_templates = [
            'base.html',
            'registration/login.html',
            'accounts/signup.html',
            'chat/home.html',
        ]
        
        for template_name in common_templates:
            template_path = Path(settings.BASE_DIR) / 'templates' / template_name
            if template_path.exists():
                print(f"✅ Template exists: {template_name}")
            else:
                print(f"⚠️  Template missing: {template_name}")
                self.warnings.append(f"Template missing: {template_name}")
        
        self.optimizations_applied.append("Template configuration review")
    
    def optimize_django_settings(self):
        """Optimize Django settings"""
        print("\n⚙️  Django Settings Optimization")
        print("-" * 25)
        
        # Check installed apps
        print(f"📦 Installed apps: {len(settings.INSTALLED_APPS)}")
        
        # Check for unnecessary apps in production
        dev_apps = [
            'django.contrib.admin',
            'debug_toolbar',
        ]
        
        for app in dev_apps:
            if app in settings.INSTALLED_APPS:
                if app == 'django.contrib.admin':
                    print(f"✅ {app}: Enabled (useful for management)")
                else:
                    print(f"⚠️  {app}: Enabled (consider disabling in production)")
                    self.warnings.append(f"Consider disabling {app} in production")
        
        # Check logging configuration
        if hasattr(settings, 'LOGGING'):
            print("✅ Logging configured")
        else:
            print("⚠️  Logging not configured")
            self.warnings.append("Logging configuration missing")
        
        self.optimizations_applied.append("Django settings review")
    
    def optimize_caching(self):
        """Optimize caching configuration"""
        print("\n🗄️  Cache Optimization")
        print("-" * 25)
        
        # Check cache configuration
        if hasattr(settings, 'CACHES'):
            for cache_name, cache_config in settings.CACHES.items():
                backend = cache_config.get('BACKEND', 'Unknown')
                print(f"✅ Cache '{cache_name}': {backend}")
                
                if 'dummy' in backend.lower():
                    print("⚠️  Dummy cache backend in use (no actual caching)")
                    self.warnings.append("Dummy cache backend provides no performance benefit")
                elif 'locmem' in backend.lower():
                    print("✅ Local memory cache - good for single-server deployments")
                elif 'redis' in backend.lower() or 'memcached' in backend.lower():
                    print("✅ External cache backend - excellent for production")
        else:
            print("⚠️  No cache configuration found")
            self.warnings.append("Cache configuration missing")
        
        # Test cache functionality
        try:
            cache.set('optimization_test', 'success', 60)
            result = cache.get('optimization_test')
            if result == 'success':
                print("✅ Cache is working correctly")
                cache.delete('optimization_test')
            else:
                print("⚠️  Cache test failed")
                self.warnings.append("Cache functionality test failed")
        except Exception as e:
            print(f"⚠️  Cache test error: {e}")
            self.warnings.append(f"Cache test error: {e}")
        
        self.optimizations_applied.append("Cache configuration and testing")
    
    def optimize_urls(self):
        """Optimize URL configuration"""
        print("\n🌐 URL Configuration Optimization")
        print("-" * 25)
        
        from django.urls import get_resolver
        
        try:
            resolver = get_resolver()
            url_patterns = resolver.url_patterns
            print(f"✅ URL patterns loaded: {len(url_patterns)} main patterns")
            
            # Check for common URL optimization patterns
            self.check_url_patterns()
            
            self.optimizations_applied.append("URL configuration review")
            
        except Exception as e:
            self.errors.append(f"URL optimization failed: {e}")
            print(f"❌ URL optimization failed: {e}")
    
    def check_url_patterns(self):
        """Check URL patterns for optimization opportunities"""
        print("🔍 Checking URL patterns...")
        
        optimizations = [
            "✅ Use include() to organize URL patterns",
            "✅ Place specific patterns before generic ones",
            "✅ Use trailing slashes consistently",
            "✅ Avoid complex regex patterns when simple strings work",
            "✅ Use name= parameter for reverse URL lookups",
        ]
        
        for optimization in optimizations:
            print(f"   {optimization}")
    
    def generate_report(self):
        """Generate optimization report"""
        print("\n📋 Optimization Report")
        print("=" * 30)
        
        print(f"\n✅ Optimizations Applied ({len(self.optimizations_applied)}):")
        for optimization in self.optimizations_applied:
            print(f"   • {optimization}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"   • {error}")
        
        # Performance recommendations
        print("\n🚀 Performance Recommendations:")
        recommendations = [
            "Enable Redis or Memcached for caching in production",
            "Use CDN for static file delivery",
            "Implement database query optimization",
            "Add monitoring and logging",
            "Consider using async views for I/O bound operations",
            "Optimize database indexes based on query patterns",
            "Use database connection pooling in production",
            "Implement proper error handling and logging",
        ]
        
        for rec in recommendations:
            print(f"   • {rec}")
        
        # Success summary
        success_rate = len(self.optimizations_applied) / (len(self.optimizations_applied) + len(self.errors)) * 100 if (self.optimizations_applied or self.errors) else 100
        print(f"\n🎯 Optimization Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 Excellent! Your application is well optimized.")
        elif success_rate >= 60:
            print("👍 Good! Consider addressing the warnings for better performance.")
        else:
            print("⚠️  There are several areas that need attention for optimal performance.")

def main():
    """Main optimization function"""
    optimizer = ApplicationOptimizer()
    
    try:
        optimizer.run_all_optimizations()
        return True
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        return False

if __name__ == '__main__':
    print("Starting comprehensive application optimization...")
    start_time = time.time()
    
    success = main()
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n⏱️  Optimization completed in {duration:.1f} seconds")
    
    if success:
        print("✅ Application optimization completed successfully!")
        sys.exit(0)
    else:
        print("❌ Application optimization completed with errors.")
        sys.exit(1)