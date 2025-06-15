import type { AppManifest } from "../../types";

const manifest: AppManifest = {
    id: "karrio.app.shipping-tasks",
    name: "Shipping Tasks",
    slug: "shipping-tasks",
    version: "1.0.0",
    description: "Manage your shipping-related tasks and workflows with a simple TODO list integrated into your Karrio workspace",
    developer: {
        name: "Karrio",
        email: "hello@karrio.io",
        website: "https://karrio.io",
    },
    category: "utility",
    type: "builtin",
    logo: "icon.svg",
    features: ["shipments", "automation"],
    ui: {
        viewports: ["dashboard", "shipments"],
        settings: true,
    },
    requirements: {
        karrio_version: ">=2024.1.0",
    },
    metadata: {
        tags: ["shipping", "tasks", "todo", "productivity", "workflow"],
        difficulty: "beginner",
        setup_time: "2 minutes",
    },
    // Metafields schema for app configuration
    metafields: [
        {
            key: "default_priority",
            label: "Default Task Priority",
            type: "text",
            description: "Choose the default priority level for new tasks",
            is_required: true,
            default_value: "medium",
            options: [
                { value: "low", label: "Low Priority" },
                { value: "medium", label: "Medium Priority" },
                { value: "high", label: "High Priority" },
                { value: "urgent", label: "Urgent" }
            ],
            validation: {
                enum: ["low", "medium", "high", "urgent"]
            }
        },
        {
            key: "task_categories",
            label: "Task Categories",
            type: "text",
            description: "Define custom task categories (comma-separated)",
            is_required: false,
            default_value: "Pickup, Delivery, Documentation, Customer Service",
            placeholder: "Pickup, Delivery, Documentation, Customer Service"
        },
        {
            key: "auto_archive_days",
            label: "Auto-Archive Completed Tasks (days)",
            type: "number",
            description: "Automatically archive completed tasks after this many days (0 to disable)",
            is_required: false,
            default_value: 30,
            validation: {
                min: 0,
                max: 365
            }
        },
        {
            key: "enable_notifications",
            label: "Enable Task Notifications",
            type: "boolean",
            description: "Show browser notifications for task reminders and updates",
            is_required: false,
            default_value: true
        },
        {
            key: "daily_task_limit",
            label: "Daily Task Limit",
            type: "number",
            description: "Maximum number of tasks to show per day (helps focus)",
            is_required: false,
            default_value: 10,
            validation: {
                min: 1,
                max: 50
            }
        },
        {
            key: "workspace_name",
            label: "Workspace Display Name",
            type: "text",
            description: "Custom name to display in the task list header",
            is_required: false,
            placeholder: "My Shipping Workspace"
        }
    ]
};

export default manifest;
