"""
Database Optimization Management Command
Optimizes database performance with proper indexes and maintenance
"""

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.core.management import call_command
import time

class Command(BaseCommand):
    help = 'Optimize database performance with indexes and maintenance'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--analyze',
            action='store_true',
            help='Analyze database and suggest optimizations',
        )
        parser.add_argument(
            '--create-indexes',
            action='store_true',
            help='Create recommended database indexes',
        )
        parser.add_argument(
            '--maintenance',
            action='store_true',
            help='Run database maintenance operations',
        )
    
    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(self.style.HTTP_INFO('🔧 Database Optimization'))
        self.stdout.write('=' * 50)
        
        if options['analyze']:
            self.analyze_database()
        
        if options['create_indexes']:
            self.create_indexes()
        
        if options['maintenance']:
            self.run_maintenance()
        
        if not any([options['analyze'], options['create_indexes'], options['maintenance']]):
            # Run all optimizations by default
            self.analyze_database()
            self.create_indexes()
            self.run_maintenance()
    
    def analyze_database(self):
        """Analyze database for optimization opportunities"""
        self.stdout.write(self.style.HTTP_INFO('\n📊 Database Analysis'))
        self.stdout.write('-' * 25)
        
        with connection.cursor() as cursor:
            # Check database engine
            db_engine = connection.settings_dict['ENGINE']
            self.stdout.write(f"Database Engine: {db_engine}")
            
            if 'sqlite' in db_engine:
                self.analyze_sqlite(cursor)
            elif 'postgresql' in db_engine:
                self.analyze_postgresql(cursor)
    
    def analyze_sqlite(self, cursor):
        """SQLite specific analysis"""
        self.stdout.write("🔍 SQLite Analysis")
        
        # Check database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        size = cursor.fetchone()[0]
        self.stdout.write(f"Database size: {size / 1024 / 1024:.1f} MB")
        
        # Check table statistics
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for (table_name,) in tables:
            if not table_name.startswith('sqlite_'):
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                self.stdout.write(f"  {table_name}: {count:,} rows")
        
        # Check indexes
        cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index'")
        indexes = cursor.fetchall()
        self.stdout.write(f"Total indexes: {len(indexes)}")
    
    def analyze_postgresql(self, cursor):
        """PostgreSQL specific analysis"""
        self.stdout.write("🐘 PostgreSQL Analysis")
        
        # Check database size
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as size
        """)
        size = cursor.fetchone()[0]
        self.stdout.write(f"Database size: {size}")
        
        # Check table statistics
        cursor.execute("""
            SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del, n_live_tup
            FROM pg_stat_user_tables
            ORDER BY n_live_tup DESC
        """)
        
        tables = cursor.fetchall()
        for schema, table, inserts, updates, deletes, live_tuples in tables:
            self.stdout.write(f"  {table}: {live_tuples:,} rows (I:{inserts}, U:{updates}, D:{deletes})")
    
    def create_indexes(self):
        """Create recommended database indexes"""
        self.stdout.write(self.style.HTTP_INFO('\\n🔨 Creating Database Indexes'))
        self.stdout.write('-' * 25)
        
        indexes = [
            {
                'name': 'chat_conversation_user_created_idx',
                'table': 'chat_conversation',
                'columns': ['user_id', 'created_at'],
                'description': 'Optimize conversation lookup by user and date'
            },
            {
                'name': 'chat_conversation_created_idx',
                'table': 'chat_conversation',
                'columns': ['created_at'],
                'description': 'Optimize conversation ordering by date'
            },
            {
                'name': 'chat_message_conversation_timestamp_idx',
                'table': 'chat_message',
                'columns': ['conversation_id', 'timestamp'],
                'description': 'Optimize message lookup within conversations'
            },
            {
                'name': 'chat_message_timestamp_idx',
                'table': 'chat_message',
                'columns': ['timestamp'],
                'description': 'Optimize message ordering by timestamp'
            },
            {
                'name': 'accounts_customuser_email_idx',
                'table': 'accounts_customuser',
                'columns': ['email'],
                'description': 'Optimize user lookup by email'
            },
            {
                'name': 'accounts_customuser_active_idx',
                'table': 'accounts_customuser',
                'columns': ['is_active'],
                'description': 'Optimize active user queries'
            },
        ]
        
        with connection.cursor() as cursor:
            for index in indexes:
                try:
                    self.create_index(cursor, index)
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠️  Could not create {index['name']}: {e}")
                    )
    
    def create_index(self, cursor, index_info):
        """Create a single database index"""
        name = index_info['name']
        table = index_info['table']
        columns = index_info['columns']
        description = index_info['description']
        
        # Check if table exists
        db_engine = connection.settings_dict['ENGINE']
        
        if 'sqlite' in db_engine:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [table])
        elif 'postgresql' in db_engine:
            cursor.execute("SELECT tablename FROM pg_tables WHERE tablename=%s", [table])
        
        if not cursor.fetchone():
            self.stdout.write(self.style.WARNING(f"  ⚠️  Table {table} does not exist"))
            return
        
        # Check if index already exists
        if 'sqlite' in db_engine:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name=?", [name])
        elif 'postgresql' in db_engine:
            cursor.execute("SELECT indexname FROM pg_indexes WHERE indexname=%s", [name])
        
        if cursor.fetchone():
            self.stdout.write(f"  ✅ Index {name} already exists")
            return
        
        # Create the index
        columns_str = ', '.join(columns)
        sql = f"CREATE INDEX {name} ON {table} ({columns_str})"
        
        try:
            cursor.execute(sql)
            self.stdout.write(
                self.style.SUCCESS(f"  ✅ Created {name}: {description}")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"  ❌ Failed to create {name}: {e}")
            )
    
    def run_maintenance(self):
        """Run database maintenance operations"""
        self.stdout.write(self.style.HTTP_INFO('\\n🧹 Database Maintenance'))
        self.stdout.write('-' * 25)
        
        with connection.cursor() as cursor:
            db_engine = connection.settings_dict['ENGINE']
            
            if 'sqlite' in db_engine:
                self.sqlite_maintenance(cursor)
            elif 'postgresql' in db_engine:
                self.postgresql_maintenance(cursor)
    
    def sqlite_maintenance(self, cursor):
        """SQLite maintenance operations"""
        self.stdout.write("🔧 SQLite Maintenance")
        
        try:
            # Analyze database for query optimization
            self.stdout.write("  Running ANALYZE...")
            cursor.execute("ANALYZE")
            
            # Optimize database
            self.stdout.write("  Running PRAGMA optimize...")
            cursor.execute("PRAGMA optimize")
            
            # Vacuum database to reclaim space
            self.stdout.write("  Running VACUUM...")
            start_time = time.time()
            cursor.execute("VACUUM")
            end_time = time.time()
            self.stdout.write(f"  VACUUM completed in {end_time - start_time:.1f}s")
            
            # Check integrity
            self.stdout.write("  Checking integrity...")
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()[0]
            if result == 'ok':
                self.stdout.write(self.style.SUCCESS("  ✅ Database integrity: OK"))
            else:
                self.stdout.write(self.style.ERROR(f"  ❌ Database integrity: {result}"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ SQLite maintenance failed: {e}"))
    
    def postgresql_maintenance(self, cursor):
        """PostgreSQL maintenance operations"""
        self.stdout.write("🐘 PostgreSQL Maintenance")
        
        try:
            # Update table statistics
            self.stdout.write("  Running ANALYZE...")
            cursor.execute("ANALYZE")
            
            # Get table list for VACUUM operations
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cursor.fetchall()
            
            # VACUUM each table (non-blocking)
            for (table_name,) in tables:
                try:
                    self.stdout.write(f"  Vacuuming {table_name}...")
                    cursor.execute(f"VACUUM ANALYZE {table_name}")
                except Exception as e:
                    self.stdout.write(f"    ⚠️  Could not vacuum {table_name}: {e}")
            
            self.stdout.write(self.style.SUCCESS("  ✅ PostgreSQL maintenance completed"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ❌ PostgreSQL maintenance failed: {e}"))