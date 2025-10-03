# Generated diagnostic migration for workflow-trigger table issue

from django.db import migrations, connection
import logging

logger = logging.getLogger(__name__)


def diagnose_workflow_trigger_table(apps, schema_editor):
    """
    Diagnostic function to check workflow-trigger table existence and relationships.
    This is a backward-compatible migration that only performs diagnostics.
    """
    try:
        with connection.cursor() as cursor:
            # Check if workflow-trigger table exists
            if schema_editor.connection.vendor == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = 'workflow-trigger'
                    );
                """)
                table_exists = cursor.fetchone()[0]
                
                if table_exists:
                    # Check table structure
                    cursor.execute("""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns 
                        WHERE table_schema = 'public' 
                        AND table_name = 'workflow-trigger'
                        ORDER BY ordinal_position;
                    """)
                    columns = cursor.fetchall()
                    logger.info(f"workflow-trigger table exists with {len(columns)} columns")
                    
                    # Test a simple query
                    cursor.execute("SELECT COUNT(*) FROM \"workflow-trigger\"")
                    count = cursor.fetchone()[0]
                    logger.info(f"workflow-trigger table has {count} records")
                    
                    # Test the problematic join query
                    try:
                        cursor.execute("""
                            SELECT w."id", w."created_by_id", w."template_id"
                            FROM "workflow-trigger" wt
                            INNER JOIN "workflow" w ON wt.workflow_id = w.id
                            LIMIT 1
                        """)
                        logger.info("✅ Join query between workflow-trigger and workflow works")
                    except Exception as join_error:
                        logger.error(f"❌ Join query failed: {join_error}")
                        
                else:
                    logger.error("❌ workflow-trigger table does not exist")
                    
            elif schema_editor.connection.vendor == 'sqlite':
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name='workflow-trigger'
                """)
                table_exists = cursor.fetchone() is not None
                
                if table_exists:
                    cursor.execute("SELECT COUNT(*) FROM \"workflow-trigger\"")
                    count = cursor.fetchone()[0]
                    logger.info(f"workflow-trigger table exists with {count} records")
                else:
                    logger.error("❌ workflow-trigger table does not exist")
            
    except Exception as e:
        logger.error(f"Diagnostic failed: {e}")


def reverse_diagnostics(apps, schema_editor):
    """Reverse operation - this is safe as we only did diagnostics."""
    logger.info("Reversing workflow-trigger diagnostics (no-op)")


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0006_workflowtrigger_last_run_at_and_more'),
    ]

    operations = [
        migrations.RunPython(
            diagnose_workflow_trigger_table,
            reverse_diagnostics,
        ),
    ]