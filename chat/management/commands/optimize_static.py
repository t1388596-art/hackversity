"""
Static Files Optimization Script
Compresses and optimizes static files for better performance
"""

import os
import gzip
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.management.commands.collectstatic import Command as CollectstaticCommand

class Command(BaseCommand):
    help = 'Optimize static files for production performance'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Compress CSS and JS files with gzip',
        )
        parser.add_argument(
            '--minify',
            action='store_true',
            help='Minify CSS and JS files',
        )
        parser.add_argument(
            '--analyze',
            action='store_true',
            help='Analyze static files for optimization opportunities',
        )
    
    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(self.style.HTTP_INFO('📁 Static Files Optimization'))
        self.stdout.write('=' * 50)
        
        # Ensure static files are collected first
        self.collect_static_files()
        
        if options['analyze']:
            self.analyze_static_files()
        
        if options['compress']:
            self.compress_static_files()
        
        if options['minify']:
            self.minify_static_files()
        
        if not any([options['analyze'], options['compress'], options['minify']]):
            # Run all optimizations by default
            self.analyze_static_files()
            self.compress_static_files()
            self.minify_static_files()
    
    def collect_static_files(self):
        """Collect static files first"""
        self.stdout.write('📦 Collecting static files...')
        
        try:
            from django.core.management import call_command
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS('✅ Static files collected'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to collect static files: {e}'))
    
    def analyze_static_files(self):
        """Analyze static files for optimization opportunities"""
        self.stdout.write(self.style.HTTP_INFO('\\n🔍 Static Files Analysis'))
        self.stdout.write('-' * 25)
        
        static_root = Path(settings.STATIC_ROOT)
        if not static_root.exists():
            self.stdout.write(self.style.ERROR('❌ STATIC_ROOT directory does not exist'))
            return
        
        # Analyze file types and sizes
        file_stats = {}
        total_size = 0
        
        for file_path in static_root.rglob('*'):
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                size = file_path.stat().st_size
                total_size += size
                
                if suffix in file_stats:
                    file_stats[suffix]['count'] += 1
                    file_stats[suffix]['size'] += size
                else:
                    file_stats[suffix] = {'count': 1, 'size': size}
        
        self.stdout.write(f'Total static files: {sum(stats["count"] for stats in file_stats.values()):,}')
        self.stdout.write(f'Total size: {total_size / 1024 / 1024:.1f} MB')
        
        # Show breakdown by file type
        self.stdout.write('\\nFile type breakdown:')
        for suffix, stats in sorted(file_stats.items(), key=lambda x: x[1]['size'], reverse=True):
            size_mb = stats['size'] / 1024 / 1024
            self.stdout.write(f'  {suffix or "no extension"}: {stats["count"]:,} files, {size_mb:.1f} MB')
        
        # Find large files
        large_files = []
        for file_path in static_root.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size > 100 * 1024:  # Files larger than 100KB
                    large_files.append((file_path, size))
        
        if large_files:
            self.stdout.write('\\n📊 Large files (>100KB):')
            for file_path, size in sorted(large_files, key=lambda x: x[1], reverse=True)[:10]:
                relative_path = file_path.relative_to(static_root)
                size_kb = size / 1024
                self.stdout.write(f'  {relative_path}: {size_kb:.1f} KB')
        
        # Check for optimization opportunities
        self.check_optimization_opportunities(static_root)
    
    def check_optimization_opportunities(self, static_root):
        """Check for specific optimization opportunities"""
        self.stdout.write('\\n💡 Optimization Opportunities:')
        
        # Check for uncompressed CSS/JS files
        css_files = list(static_root.glob('**/*.css'))
        js_files = list(static_root.glob('**/*.js'))
        
        compressible_size = 0
        for file_path in css_files + js_files:
            if not file_path.with_suffix(file_path.suffix + '.gz').exists():
                compressible_size += file_path.stat().st_size
        
        if compressible_size > 0:
            self.stdout.write(f'  • {compressible_size / 1024:.1f} KB of CSS/JS files can be compressed')
        
        # Check for unoptimized images
        image_files = []
        for pattern in ['**/*.jpg', '**/*.jpeg', '**/*.png', '**/*.gif']:
            image_files.extend(static_root.glob(pattern))
        
        if image_files:
            large_images = [f for f in image_files if f.stat().st_size > 50 * 1024]
            if large_images:
                self.stdout.write(f'  • {len(large_images)} image files >50KB could be optimized')
        
        # Check for duplicate files
        self.check_duplicate_files(static_root)
    
    def check_duplicate_files(self, static_root):
        """Check for potential duplicate files"""
        file_sizes = {}
        for file_path in static_root.rglob('*'):
            if file_path.is_file():
                size = file_path.stat().st_size
                if size in file_sizes:
                    file_sizes[size].append(file_path)
                else:
                    file_sizes[size] = [file_path]
        
        duplicates = {size: files for size, files in file_sizes.items() if len(files) > 1}
        if duplicates:
            self.stdout.write(f'  • Found {len(duplicates)} potential duplicate file groups')
    
    def compress_static_files(self):
        """Compress CSS and JS files with gzip"""
        self.stdout.write(self.style.HTTP_INFO('\\n🗜️  Compressing Static Files'))
        self.stdout.write('-' * 25)
        
        static_root = Path(settings.STATIC_ROOT)
        if not static_root.exists():
            self.stdout.write(self.style.ERROR('❌ STATIC_ROOT directory does not exist'))
            return
        
        # Files to compress
        patterns = ['**/*.css', '**/*.js', '**/*.html', '**/*.svg', '**/*.txt']
        files_to_compress = []
        
        for pattern in patterns:
            files_to_compress.extend(static_root.glob(pattern))
        
        compressed_count = 0
        total_original_size = 0
        total_compressed_size = 0
        
        for file_path in files_to_compress:
            if file_path.is_file():
                original_size = file_path.stat().st_size
                
                # Skip very small files (less than 1KB)
                if original_size < 1024:
                    continue
                
                compressed_path = file_path.with_suffix(file_path.suffix + '.gz')
                
                # Skip if already compressed and up to date
                if compressed_path.exists() and compressed_path.stat().st_mtime > file_path.stat().st_mtime:
                    continue
                
                try:
                    with open(file_path, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    compressed_size = compressed_path.stat().st_size
                    compression_ratio = (1 - compressed_size / original_size) * 100
                    
                    if compression_ratio > 10:  # Only keep if >10% reduction
                        compressed_count += 1
                        total_original_size += original_size
                        total_compressed_size += compressed_size
                        
                        relative_path = file_path.relative_to(static_root)
                        self.stdout.write(
                            f'  ✅ {relative_path}: {original_size:,} → {compressed_size:,} bytes '
                            f'({compression_ratio:.1f}% reduction)'
                        )
                    else:
                        # Remove compressed file if savings are minimal
                        compressed_path.unlink()
                
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠️  Could not compress {file_path}: {e}')
                    )
        
        if compressed_count > 0:
            total_savings = total_original_size - total_compressed_size
            overall_ratio = (total_savings / total_original_size) * 100
            self.stdout.write(
                self.style.SUCCESS(
                    f'\\n✅ Compressed {compressed_count} files '
                    f'({total_savings / 1024:.1f} KB saved, {overall_ratio:.1f}% reduction)'
                )
            )
        else:
            self.stdout.write('  ℹ️  No files needed compression')
    
    def minify_static_files(self):
        """Minify CSS and JS files (basic implementation)"""
        self.stdout.write(self.style.HTTP_INFO('\\n✂️  Minifying Static Files'))
        self.stdout.write('-' * 25)
        
        static_root = Path(settings.STATIC_ROOT)
        if not static_root.exists():
            self.stdout.write(self.style.ERROR('❌ STATIC_ROOT directory does not exist'))
            return
        
        # Basic CSS minification
        css_files = static_root.glob('**/*.css')
        minified_count = 0
        
        for css_file in css_files:
            if css_file.name.endswith('.min.css'):
                continue  # Skip already minified files
            
            try:
                content = css_file.read_text(encoding='utf-8')
                
                # Basic CSS minification
                minified_content = self.minify_css(content)
                
                if len(minified_content) < len(content):
                    minified_path = css_file.with_name(
                        css_file.stem + '.min' + css_file.suffix
                    )
                    minified_path.write_text(minified_content, encoding='utf-8')
                    
                    original_size = len(content)
                    minified_size = len(minified_content)
                    savings = (1 - minified_size / original_size) * 100
                    
                    relative_path = css_file.relative_to(static_root)
                    self.stdout.write(
                        f'  ✅ {relative_path}: {original_size:,} → {minified_size:,} chars '
                        f'({savings:.1f}% reduction)'
                    )
                    minified_count += 1
            
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️  Could not minify {css_file}: {e}')
                )
        
        if minified_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\\n✅ Minified {minified_count} CSS files')
            )
        else:
            self.stdout.write('  ℹ️  No CSS files needed minification')
    
    def minify_css(self, css_content):
        """Basic CSS minification"""
        import re
        
        # Remove comments
        css_content = re.sub(r'/\\*.*?\\*/', '', css_content, flags=re.DOTALL)
        
        # Remove extra whitespace
        css_content = re.sub(r'\\s+', ' ', css_content)
        
        # Remove whitespace around specific characters
        css_content = re.sub(r'\\s*([{}:;,>+~])\\s*', r'\\1', css_content)
        
        # Remove trailing semicolons
        css_content = re.sub(r';\\s*}', '}', css_content)
        
        return css_content.strip()
    
    def create_cache_manifest(self):
        """Create a cache manifest for static files"""
        self.stdout.write('📝 Creating cache manifest...')
        
        static_root = Path(settings.STATIC_ROOT)
        manifest = {
            'files': {},
            'version': int(time.time()),
        }
        
        for file_path in static_root.rglob('*'):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(static_root))
                manifest['files'][relative_path] = {
                    'size': file_path.stat().st_size,
                    'modified': file_path.stat().st_mtime,
                }
        
        manifest_path = static_root / 'manifest.json'
        import json
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        self.stdout.write(f'✅ Cache manifest created with {len(manifest["files"])} files')