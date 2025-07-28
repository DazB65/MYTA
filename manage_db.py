#!/usr/bin/env python3
"""
CreatorMate Database Management CLI
Comprehensive tool for managing database migrations, backups, and maintenance
"""

import sys
import os
import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path
import logging

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from migration_manager import get_migration_manager, BackupInfo
from backup_service import get_backup_service, BackupSchedule, BackupAlert, BackupFrequency, BackupHealthChecker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseCLI:
    """Command-line interface for database management"""
    
    def __init__(self, db_path: str = "backend/creatormate.db"):
        self.db_path = db_path
        self.migration_manager = get_migration_manager(db_path)
        self.backup_service = None
    
    def init_backup_service(self):
        """Initialize backup service if needed"""
        if self.backup_service is None:
            self.backup_service = get_backup_service(self.db_path)
    
    # Migration Commands
    def migration_status(self):
        """Show migration status"""
        print("🗃️  Database Migration Status")
        print("=" * 50)
        
        current_version = self.migration_manager.get_current_version()
        pending_migrations = self.migration_manager.get_pending_migrations()
        
        print(f"Current Version: {current_version}")
        print(f"Pending Migrations: {len(pending_migrations)}")
        
        if pending_migrations:
            print("\nPending Migrations:")
            for migration in pending_migrations:
                print(f"  • {migration.version}: {migration.name}")
                print(f"    {migration.description}")
        else:
            print("\n✅ Database is up to date!")
    
    def migration_history(self):
        """Show migration history"""
        print("📜 Migration History")
        print("=" * 50)
        
        history = self.migration_manager.get_migration_history()
        
        if not history:
            print("No migrations have been applied yet.")
            return
        
        for migration in history:
            status = "✅" if migration.applied else "❌"
            print(f"{status} {migration.version}: {migration.name}")
            print(f"   Applied: {migration.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            if migration.execution_time:
                print(f"   Execution time: {migration.execution_time:.2f}s")
            if migration.rollback_available:
                print(f"   Rollback: Available")
            print()
    
    def migrate(self, target_version: str = None, no_backup: bool = False):
        """Run database migrations"""
        print("🚀 Running Database Migrations")
        print("=" * 50)
        
        if not no_backup:
            print("Creating pre-migration backup...")
        
        success = self.migration_manager.migrate(
            target_version=target_version,
            create_backup=not no_backup
        )
        
        if success:
            print("✅ Migrations completed successfully!")
        else:
            print("❌ Migration failed! Check logs for details.")
            sys.exit(1)
    
    def rollback(self, target_version: str, no_backup: bool = False):
        """Rollback database to specific version"""
        print(f"⏪ Rolling back to version {target_version}")
        print("=" * 50)
        
        current_version = self.migration_manager.get_current_version()
        
        if target_version >= current_version:
            print("❌ Target version must be older than current version")
            sys.exit(1)
        
        confirm = input(f"This will rollback from {current_version} to {target_version}. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Rollback cancelled.")
            return
        
        success = self.migration_manager.rollback(
            target_version=target_version,
            create_backup=not no_backup
        )
        
        if success:
            print("✅ Rollback completed successfully!")
        else:
            print("❌ Rollback failed! Check logs for details.")
            sys.exit(1)
    
    # Backup Commands
    def backup_create(self, backup_type: str = "manual", compression: bool = True):
        """Create a database backup"""
        print("💾 Creating Database Backup")
        print("=" * 50)
        
        backup_id = self.migration_manager.create_backup(
            backup_type=backup_type,
            compression=compression
        )
        
        if backup_id:
            backup_info = self.migration_manager.get_backup_info(backup_id)
            print(f"✅ Backup created successfully!")
            print(f"   Backup ID: {backup_id}")
            print(f"   Size: {backup_info.size_bytes / (1024*1024):.2f} MB")
            print(f"   Location: {backup_info.file_path}")
            print(f"   Compression: {'Yes' if backup_info.compression else 'No'}")
        else:
            print("❌ Backup creation failed!")
            sys.exit(1)
    
    def backup_list(self, limit: int = 10):
        """List available backups"""
        print("📋 Available Backups")
        print("=" * 50)
        
        backups = self.migration_manager.list_backups()
        
        if not backups:
            print("No backups found.")
            return
        
        # Show limited number of backups
        displayed_backups = backups[:limit]
        
        for backup in displayed_backups:
            status = "✅" if os.path.exists(backup.file_path) else "❌"
            size_mb = backup.size_bytes / (1024 * 1024)
            
            print(f"{status} {backup.backup_id}")
            print(f"   Type: {backup.backup_type}")
            print(f"   Created: {backup.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Size: {size_mb:.2f} MB")
            print(f"   Version: {backup.database_version}")
            print(f"   Compression: {'Yes' if backup.compression else 'No'}")
            print()
        
        if len(backups) > limit:
            print(f"... and {len(backups) - limit} more backups")
    
    def backup_restore(self, backup_id: str, verify: bool = True):
        """Restore database from backup"""
        print(f"🔄 Restoring from backup: {backup_id}")
        print("=" * 50)
        
        backup_info = self.migration_manager.get_backup_info(backup_id)
        if not backup_info:
            print(f"❌ Backup {backup_id} not found!")
            sys.exit(1)
        
        print(f"Backup Details:")
        print(f"   Type: {backup_info.backup_type}")
        print(f"   Created: {backup_info.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Database Version: {backup_info.database_version}")
        print(f"   Size: {backup_info.size_bytes / (1024*1024):.2f} MB")
        print()
        
        confirm = input("This will replace the current database. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Restore cancelled.")
            return
        
        success = self.migration_manager.restore_backup(backup_id, verify_integrity=verify)
        
        if success:
            print("✅ Database restored successfully!")
        else:
            print("❌ Restore failed! Check logs for details.")
            sys.exit(1)
    
    def backup_delete(self, backup_id: str):
        """Delete a specific backup"""
        print(f"🗑️  Deleting backup: {backup_id}")
        print("=" * 50)
        
        backup_info = self.migration_manager.get_backup_info(backup_id)
        if not backup_info:
            print(f"❌ Backup {backup_id} not found!")
            sys.exit(1)
        
        confirm = input(f"Delete backup {backup_id}? (y/N): ")
        if confirm.lower() != 'y':
            print("Deletion cancelled.")
            return
        
        success = self.migration_manager.delete_backup(backup_id)
        
        if success:
            print("✅ Backup deleted successfully!")
        else:
            print("❌ Backup deletion failed!")
            sys.exit(1)
    
    def backup_verify(self, backup_id: str = None):
        """Verify backup integrity"""
        if backup_id:
            print(f"🔍 Verifying backup: {backup_id}")
            print("=" * 50)
            
            is_valid = self.migration_manager.verify_backup_integrity(backup_id)
            
            if is_valid:
                print("✅ Backup integrity verified!")
            else:
                print("❌ Backup integrity check failed!")
                sys.exit(1)
        else:
            print("🔍 Verifying all backups")
            print("=" * 50)
            
            backups = self.migration_manager.list_backups()
            failed_backups = []
            
            for backup in backups:
                is_valid = self.migration_manager.verify_backup_integrity(backup.backup_id)
                status = "✅" if is_valid else "❌"
                print(f"{status} {backup.backup_id}")
                
                if not is_valid:
                    failed_backups.append(backup.backup_id)
            
            if failed_backups:
                print(f"\n❌ {len(failed_backups)} backups failed integrity check:")
                for backup_id in failed_backups:
                    print(f"   • {backup_id}")
                sys.exit(1)
            else:
                print(f"\n✅ All {len(backups)} backups passed integrity check!")
    
    def backup_cleanup(self, days: int = 30, keep: int = 10):
        """Clean up old backups"""
        print(f"🧹 Cleaning up backups older than {days} days (keeping {keep} most recent)")
        print("=" * 50)
        
        deleted_count = self.migration_manager.cleanup_old_backups(
            keep_days=days,
            keep_count=keep
        )
        
        print(f"✅ Cleaned up {deleted_count} old backups")
    
    # Service Commands
    def service_start(self):
        """Start backup service"""
        print("🚀 Starting Backup Service")
        print("=" * 50)
        
        self.init_backup_service()
        self.backup_service.start()
        
        status = self.backup_service.get_service_status()
        print("✅ Backup service started!")
        print(f"   Schedule: {status['schedule']['frequency']} at {status['schedule']['time']}")
        print(f"   Compression: {'Enabled' if status['schedule']['compression'] else 'Disabled'}")
        print(f"   Max backups: {status['schedule']['max_backups']}")
    
    def service_stop(self):
        """Stop backup service"""
        print("🛑 Stopping Backup Service")
        print("=" * 50)
        
        self.init_backup_service()
        self.backup_service.stop()
        print("✅ Backup service stopped!")
    
    def service_status(self):
        """Show backup service status"""
        print("📊 Backup Service Status")
        print("=" * 50)
        
        self.init_backup_service()
        status = self.backup_service.get_service_status()
        
        print(f"Running: {'Yes' if status['running'] else 'No'}")
        print(f"Schedule: {status['schedule']['frequency']} at {status['schedule']['time']}")
        print(f"Enabled: {'Yes' if status['schedule']['enabled'] else 'No'}")
        print(f"Compression: {'Enabled' if status['schedule']['compression'] else 'Disabled'}")
        print(f"Max backups: {status['schedule']['max_backups']}")
        print(f"Cleanup: {'Enabled' if status['schedule']['cleanup_enabled'] else 'Disabled'}")
        print()
        print("Alert Configuration:")
        print(f"   Email alerts: {'Enabled' if status['alerts']['email_enabled'] else 'Disabled'}")
        print(f"   Webhook alerts: {'Enabled' if status['alerts']['webhook_enabled'] else 'Disabled'}")
        print(f"   Alert on failure: {'Yes' if status['alerts']['alert_on_failure'] else 'No'}")
        print(f"   Alert on success: {'Yes' if status['alerts']['alert_on_success'] else 'No'}")
        print()
        print(f"Last check: {status['last_check']}")
    
    # Health Commands
    def health_check(self):
        """Run comprehensive health check"""
        print("🏥 Database Health Check")
        print("=" * 50)
        
        health_checker = BackupHealthChecker(self.db_path)
        report = health_checker.run_health_check()
        
        status_emoji = {
            "healthy": "✅",
            "degraded": "⚠️",
            "unhealthy": "❌",
            "error": "💥"
        }
        
        print(f"Overall Status: {status_emoji.get(report['overall_status'], '❓')} {report['overall_status'].upper()}")
        print(f"Check Time: {report['timestamp']}")
        print()
        
        for check_name, result in report.get('checks', {}).items():
            status = "✅" if result.get('status', False) else "❌"
            print(f"{status} {check_name.replace('_', ' ').title()}")
            print(f"   {result.get('message', 'No message')}")
            
            details = result.get('details', {})
            if details:
                for key, value in details.items():
                    print(f"   {key}: {value}")
            print()
        
        if report['overall_status'] in ['unhealthy', 'error']:
            sys.exit(1)
    
    def stats(self):
        """Show database statistics"""
        print("📊 Database Statistics")
        print("=" * 50)
        
        stats = self.migration_manager.get_database_stats()
        
        print(f"Database Path: {stats.get('database_path', 'Unknown')}")
        print(f"Database Size: {stats.get('database_size_mb', 0):.2f} MB")
        print(f"Current Version: {stats.get('current_version', 'Unknown')}")
        print(f"Pending Migrations: {stats.get('pending_migrations', 0)}")
        print(f"Total Tables: {stats.get('total_tables', 0)}")
        print()
        
        print("Table Record Counts:")
        table_counts = stats.get('table_counts', {})
        for table, count in table_counts.items():
            print(f"   {table}: {count}")
        print()
        
        print(f"Total Backups: {stats.get('total_backups', 0)}")
        print(f"Backup Storage: {stats.get('total_backup_size_mb', 0):.2f} MB")
        
        last_backup = stats.get('last_backup')
        if last_backup:
            print(f"Last Backup: {last_backup}")
        else:
            print("Last Backup: Never")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CreatorMate Database Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s migration status                    # Show migration status
  %(prog)s migrate                            # Run all pending migrations
  %(prog)s migrate --target 003               # Migrate to specific version
  %(prog)s rollback 002                       # Rollback to version 002
  
  %(prog)s backup create                      # Create manual backup
  %(prog)s backup list                        # List available backups
  %(prog)s backup restore backup_20240101_120000_manual  # Restore from backup
  %(prog)s backup cleanup --days 30 --keep 10  # Clean old backups
  
  %(prog)s service start                      # Start backup service
  %(prog)s service status                     # Show service status
  
  %(prog)s health                            # Run health check
  %(prog)s stats                             # Show database stats
        """
    )
    
    parser.add_argument('--db', default='backend/creatormate.db', help='Database path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Migration commands
    migration_parser = subparsers.add_parser('migration', help='Migration commands')
    migration_subparsers = migration_parser.add_subparsers(dest='migration_command')
    
    migration_subparsers.add_parser('status', help='Show migration status')
    migration_subparsers.add_parser('history', help='Show migration history')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Run database migrations')
    migrate_parser.add_argument('--target', help='Target version')
    migrate_parser.add_argument('--no-backup', action='store_true', help='Skip pre-migration backup')
    
    # Rollback command
    rollback_parser = subparsers.add_parser('rollback', help='Rollback database')
    rollback_parser.add_argument('target_version', help='Target version to rollback to')
    rollback_parser.add_argument('--no-backup', action='store_true', help='Skip pre-rollback backup')
    
    # Backup commands
    backup_parser = subparsers.add_parser('backup', help='Backup commands')
    backup_subparsers = backup_parser.add_subparsers(dest='backup_command')
    
    create_parser = backup_subparsers.add_parser('create', help='Create backup')
    create_parser.add_argument('--type', default='manual', help='Backup type')
    create_parser.add_argument('--no-compression', action='store_true', help='Disable compression')
    
    list_parser = backup_subparsers.add_parser('list', help='List backups')
    list_parser.add_argument('--limit', type=int, default=10, help='Limit number of backups shown')
    
    restore_parser = backup_subparsers.add_parser('restore', help='Restore backup')
    restore_parser.add_argument('backup_id', help='Backup ID to restore')
    restore_parser.add_argument('--no-verify', action='store_true', help='Skip integrity verification')
    
    delete_parser = backup_subparsers.add_parser('delete', help='Delete backup')
    delete_parser.add_argument('backup_id', help='Backup ID to delete')
    
    verify_parser = backup_subparsers.add_parser('verify', help='Verify backup integrity')
    verify_parser.add_argument('backup_id', nargs='?', help='Specific backup ID (optional)')
    
    cleanup_parser = backup_subparsers.add_parser('cleanup', help='Clean up old backups')
    cleanup_parser.add_argument('--days', type=int, default=30, help='Keep backups newer than N days')
    cleanup_parser.add_argument('--keep', type=int, default=10, help='Keep N most recent backups')
    
    # Service commands
    service_parser = subparsers.add_parser('service', help='Backup service commands')
    service_subparsers = service_parser.add_subparsers(dest='service_command')
    
    service_subparsers.add_parser('start', help='Start backup service')
    service_subparsers.add_parser('stop', help='Stop backup service')
    service_subparsers.add_parser('status', help='Show service status')
    
    # Health commands
    subparsers.add_parser('health', help='Run health check')
    subparsers.add_parser('stats', help='Show database statistics')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize CLI
    cli = DatabaseCLI(args.db)
    
    try:
        # Route commands
        if args.command == 'migration':
            if args.migration_command == 'status':
                cli.migration_status()
            elif args.migration_command == 'history':
                cli.migration_history()
        
        elif args.command == 'migrate':
            cli.migrate(args.target, args.no_backup)
        
        elif args.command == 'rollback':
            cli.rollback(args.target_version, args.no_backup)
        
        elif args.command == 'backup':
            if args.backup_command == 'create':
                cli.backup_create(args.type, not args.no_compression)
            elif args.backup_command == 'list':
                cli.backup_list(args.limit)
            elif args.backup_command == 'restore':
                cli.backup_restore(args.backup_id, not args.no_verify)
            elif args.backup_command == 'delete':
                cli.backup_delete(args.backup_id)
            elif args.backup_command == 'verify':
                cli.backup_verify(args.backup_id)
            elif args.backup_command == 'cleanup':
                cli.backup_cleanup(args.days, args.keep)
        
        elif args.command == 'service':
            if args.service_command == 'start':
                cli.service_start()
            elif args.service_command == 'stop':
                cli.service_stop()
            elif args.service_command == 'status':
                cli.service_status()
        
        elif args.command == 'health':
            cli.health_check()
        
        elif args.command == 'stats':
            cli.stats()
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Command failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()