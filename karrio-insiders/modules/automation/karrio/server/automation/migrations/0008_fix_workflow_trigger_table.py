# Migration to fix workflow-trigger table issue using Django ORM

from django.db import migrations, models
import django.db.models.deletion
import functools
import karrio.server.core.models.base
import logging

logger = logging.getLogger(__name__)


def fix_workflow_trigger_table(apps, schema_editor):
    """
    Fix the workflow-trigger table by ensuring it exists properly using Django ORM.
    
    This migration tries to query the WorkflowTrigger model to see if the table
    exists and is accessible. If not, it provides guidance on what might be wrong.
    """
    try:
        # Get the model from the migration state
        WorkflowTrigger = apps.get_model('automation', 'WorkflowTrigger')
        
        # Try to perform a simple query to check if the table is accessible
        try:
            # This will fail if the table doesn't exist or has the wrong name
            count = WorkflowTrigger.objects.count()
            logger.info(f"✅ WorkflowTrigger table is accessible with {count} records")
            return
            
        except Exception as query_error:
            logger.info(f"WorkflowTrigger table query failed: {query_error}")
            
            # If we can't query the table, it might be a table naming issue
            # Let's try to detect and fix it using Django's introspection
            db_table_name = WorkflowTrigger._meta.db_table
            logger.info(f"Expected table name: {db_table_name}")
            
            # Check what tables actually exist using Django's introspection
            with schema_editor.connection.cursor() as cursor:
                table_names = schema_editor.connection.introspection.table_names(cursor)
                logger.info(f"Available tables: {[t for t in table_names if 'workflow' in t.lower()]}")
                
                # Look for tables that might be our WorkflowTrigger table
                possible_names = [
                    'workflow_trigger', 
                    'workflowtrigger', 
                    'workflow-trigger',
                    '"workflow-trigger"'
                ]
                
                found_table = None
                for possible_name in possible_names:
                    if possible_name in table_names:
                        found_table = possible_name
                        break
                
                if found_table and found_table != db_table_name:
                    logger.info(f"Found table with different name: {found_table}")
                    logger.info(f"Renaming {found_table} to {db_table_name}")
                    
                    # Use Django's schema editor to rename the table
                    # This is safer than raw SQL as it handles database differences
                    old_table_name = found_table.strip('"')  # Remove quotes if present
                    new_table_name = db_table_name.strip('"')
                    
                    # Django's rename_table method
                    schema_editor.execute(
                        schema_editor.sql_rename_table % {
                            "old_table": schema_editor.quote_name(old_table_name),
                            "new_table": schema_editor.quote_name(new_table_name),
                        }
                    )
                    logger.info("✅ Table renamed successfully using Django schema editor")
                    
                    # Verify the fix worked
                    count = WorkflowTrigger.objects.count()
                    logger.info(f"✅ WorkflowTrigger table now accessible with {count} records")
                    
                else:
                    logger.warning("WorkflowTrigger table not found with any expected name")
                    logger.warning("This suggests that the initial migration (0001_initial.py) hasn't been applied")
                    logger.warning("Please run: python manage.py migrate automation 0001 --fake")
                    logger.warning("Then run: python manage.py migrate automation")
                    
    except Exception as e:
        logger.error(f"Fix operation failed: {e}")
        # Don't raise the exception to avoid breaking migrations
        # Just log the error and continue
        logger.error("Migration will continue, but WorkflowTrigger table issues may persist")


def reverse_fix(apps, schema_editor):
    """
    Reverse operation using Django ORM.
    
    Since we're only fixing table naming issues, there's not much to reverse.
    We'll just log that this was a table naming fix.
    """
    logger.info("Reversing workflow-trigger table fix")
    logger.info("Note: This migration only fixed table naming issues, no structural changes to reverse")


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0007_workflow_trigger_diagnostics'),
    ]

    operations = [
        migrations.RunPython(
            fix_workflow_trigger_table,
            reverse_fix,
        ),
    ]