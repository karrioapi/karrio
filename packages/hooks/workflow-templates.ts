import {
  WorkflowFilter,
  WorkflowActionFilter,
  WorkflowConnectionFilter,
  GetWorkflowTemplates,
  GetWorkflowActionTemplates,
  GetWorkflowConnectionTemplates,
  GET_WORKFLOW_TEMPLATES,
  GET_WORKFLOW_ACTION_TEMPLATES,
  GET_WORKFLOW_CONNECTION_TEMPLATES
} from "@karrio/types/graphql/ee";
import { useQuery } from "@tanstack/react-query";
import { gqlstr, onError } from "@karrio/lib";
import { useKarrio } from "./karrio";
import React from "react";

const PAGE_SIZE = 50;
const PAGINATION = { offset: 0, first: PAGE_SIZE };

export type WorkflowTemplateType = GetWorkflowTemplates["workflow_templates"]["edges"][0]["node"];
export type WorkflowActionTemplateType = GetWorkflowActionTemplates["workflow_action_templates"]["edges"][0]["node"];
export type WorkflowConnectionTemplateType = GetWorkflowConnectionTemplates["workflow_connection_templates"]["edges"][0]["node"];

export function useWorkflowTemplates(filter: WorkflowFilter = {}) {
  const karrio = useKarrio();
  const fetch = (variables: { filter: WorkflowFilter }) =>
    karrio.graphql.request<GetWorkflowTemplates>(gqlstr(GET_WORKFLOW_TEMPLATES), { variables });

  return useQuery(
    ['workflow-templates', filter],
    () => fetch({ filter: { ...PAGINATION, ...filter } }),
    { keepPreviousData: true, staleTime: 10000, onError },
  );
}

export function useWorkflowActionTemplates(filter: WorkflowActionFilter = {}) {
  const karrio = useKarrio();
  const fetch = (variables: { filter: WorkflowActionFilter }) =>
    karrio.graphql.request<GetWorkflowActionTemplates>(gqlstr(GET_WORKFLOW_ACTION_TEMPLATES), { variables });

  return useQuery(
    ['workflow-action-templates', filter],
    () => fetch({ filter: { ...PAGINATION, ...filter } }),
    { keepPreviousData: true, staleTime: 10000, onError },
  );
}

export function useWorkflowConnectionTemplates(filter: WorkflowConnectionFilter = {}) {
  const karrio = useKarrio();
  const fetch = (variables: { filter: WorkflowConnectionFilter }) =>
    karrio.graphql.request<GetWorkflowConnectionTemplates>(gqlstr(GET_WORKFLOW_CONNECTION_TEMPLATES), { variables });

  return useQuery(
    ['workflow-connection-templates', filter],
    () => fetch({ filter: { ...PAGINATION, ...filter } }),
    { keepPreviousData: true, staleTime: 10000, onError },
  );
}

// Predefined workflow templates for common use cases
export const PREDEFINED_WORKFLOW_TEMPLATES: any[] = [
  {
    name: "Order Fulfillment Notification",
    slug: "order-fulfillment-notification",
    description: "Automatically notify customers when their orders are fulfilled",
    trigger: {
      slug: "order-fulfilled-trigger",
      trigger_type: "webhook" as any,
      schedule: null
    },
    actions: [
      {
        slug: "send-email-notification",
        name: "Send Email Notification",
        action_type: "http_request" as any,
        description: "Send notification email to customer",
        method: "post" as any,
        content_type: "json" as any,
        parameters_type: "data" as any,
        parameters_template: `{
  "to": "{{ customer_email }}",
  "subject": "Your order {{ order_number }} has been fulfilled!",
  "template": "order_fulfilled",
  "data": {
    "customer_name": "{{ customer_name }}",
    "order_number": "{{ order_number }}",
    "tracking_number": "{{ tracking_number }}",
    "carrier": "{{ carrier_name }}"
  }
}`,
        header_template: `{
  "Content-Type": "application/json",
  "Authorization": "Bearer {{ email_service_token }}"
}`,
        template_slug: "email-notification-action"
      }
    ]
  },
  {
    name: "ERP Order Sync",
    slug: "erp-order-sync",
    description: "Synchronize new orders with your ERP system",
    trigger: {
      slug: "order-created-trigger",
      trigger_type: "webhook" as any,
      schedule: null
    },
    actions: [
      {
        slug: "sync-to-erp",
        name: "Sync to ERP",
        action_type: "http_request" as any,
        description: "Send order data to ERP system",
        method: "post" as any,
        content_type: "json" as any,
        parameters_type: "data" as any,
        parameters_template: `{
  "order_id": "{{ order_id }}",
  "customer": {
    "name": "{{ customer_name }}",
    "email": "{{ customer_email }}",
    "phone": "{{ customer_phone }}"
  },
  "items": {{ order_items }},
  "shipping_address": {{ shipping_address }},
  "total": "{{ order_total }}"
}`,
        header_template: `{
  "Content-Type": "application/json",
  "X-API-Key": "{{ erp_api_key }}"
}`,
        template_slug: "erp-sync-action"
      }
    ]
  },
  {
    name: "Inventory Level Alert",
    slug: "inventory-level-alert",
    description: "Get notified when inventory levels are low",
    trigger: {
      slug: "low-inventory-trigger",
      trigger_type: "scheduled" as any,
      schedule: "0 9 * * *" // Daily at 9 AM
    },
    actions: [
      {
        slug: "check-inventory",
        name: "Check Inventory Levels",
        action_type: "http_request" as any,
        description: "Check current inventory levels",
        method: "get" as any,
        content_type: "json" as any,
        parameters_type: "data" as any,
        parameters_template: `{
  "threshold": 10,
  "include_variants": true
}`,
        header_template: `{
  "Authorization": "Bearer {{ inventory_api_token }}"
}`,
        template_slug: "inventory-check-action"
      },
      {
        slug: "send-alert",
        name: "Send Low Stock Alert",
        action_type: "http_request" as any,
        description: "Send alert for low stock items",
        method: "post" as any,
        content_type: "json" as any,
        parameters_type: "data" as any,
        parameters_template: `{
  "channel": "#inventory",
  "message": "⚠️ Low inventory alert: {{ low_stock_items }}",
  "urgency": "high"
}`,
        header_template: `{
  "Content-Type": "application/json",
  "Authorization": "Bearer {{ slack_bot_token }}"
}`,
        template_slug: "slack-alert-action"
      }
    ]
  },
  {
    name: "Shipping Rate Sync",
    slug: "shipping-rate-sync",
    description: "Daily sync of shipping rates from carriers",
    trigger: {
      slug: "daily-rate-sync",
      trigger_type: "scheduled" as any,
      schedule: "0 6 * * *" // Daily at 6 AM
    },
    actions: [
      {
        slug: "fetch-fedex-rates",
        name: "Fetch FedEx Rates",
        action_type: "http_request" as any,
        description: "Get latest rates from FedEx API",
        method: "get" as any,
        content_type: "json" as any,
        parameters_type: "data" as any,
        parameters_template: `{
  "service_types": ["FEDEX_GROUND", "FEDEX_EXPRESS_SAVER", "FEDEX_2_DAY"],
  "zones": "all"
}`,
        header_template: `{
  "Authorization": "Bearer {{ fedex_api_token }}"
}`,
        template_slug: "fedex-rates-action"
      }
    ]
  }
];

// Predefined action templates
export const PREDEFINED_ACTION_TEMPLATES: any[] = [
  {
    slug: "slack-notification",
    name: "Slack Notification",
    action_type: "http_request" as any,
    description: "Send a message to Slack channel",
    method: "post" as any,
    content_type: "json" as any,
    parameters_type: "data" as any,
    parameters_template: `{
  "channel": "#general",
  "text": "{{ message }}",
  "username": "Karrio Bot"
}`,
    header_template: `{
  "Content-Type": "application/json",
  "Authorization": "Bearer {{ slack_bot_token }}"
}`,
    template_slug: "slack-notification"
  },
  {
    slug: "email-notification",
    name: "Email Notification",
    action_type: "http_request" as any,
    description: "Send email notification",
    method: "post" as any,
    content_type: "json" as any,
    parameters_type: "data" as any,
    parameters_template: `{
  "to": "{{ recipient_email }}",
  "subject": "{{ email_subject }}",
  "html": "{{ email_body }}",
  "from": "{{ sender_email }}"
}`,
    header_template: `{
  "Content-Type": "application/json",
  "Authorization": "Bearer {{ email_service_token }}"
}`,
    template_slug: "email-notification"
  },
  {
    slug: "webhook-call",
    name: "Webhook Call",
    action_type: "http_request" as any,
    description: "Make a webhook call to external service",
    method: "post" as any,
    content_type: "json" as any,
    parameters_type: "data" as any,
    parameters_template: `{
  "event": "{{ event_type }}",
  "data": {{ event_data }},
  "timestamp": "{{ current_timestamp }}"
}`,
    header_template: `{
  "Content-Type": "application/json",
  "X-Webhook-Secret": "{{ webhook_secret }}"
}`,
    template_slug: "webhook-call"
  },
  {
    slug: "database-insert",
    name: "Database Insert",
    action_type: "http_request" as any,
    description: "Insert data into database via API",
    method: "post" as any,
    content_type: "json" as any,
    parameters_type: "data" as any,
    parameters_template: `{
  "table": "{{ table_name }}",
  "data": {{ record_data }}
}`,
    header_template: `{
  "Content-Type": "application/json",
  "Authorization": "Bearer {{ database_api_token }}"
}`,
    template_slug: "database-insert"
  }
];

// Predefined connection templates
export const PREDEFINED_CONNECTION_TEMPLATES: any[] = [
  {
    name: "Slack Bot Connection",
    slug: "slack-bot",
    auth_type: "bearer" as any,
    description: "Connect to Slack using Bot Token",
    host: "slack.com",
    endpoint: "/api",
    auth_template: `{
  "Authorization": "Bearer {{ slack_bot_token }}"
}`,
    parameters_template: `{
  "slack_bot_token": "xoxb-your-bot-token"
}`,
    template_slug: "slack-bot"
  },
  {
    name: "Email Service (SendGrid)",
    slug: "sendgrid-email",
    auth_type: "bearer" as any,
    description: "Send emails via SendGrid API",
    host: "api.sendgrid.com",
    endpoint: "/v3/mail/send",
    auth_template: `{
  "Authorization": "Bearer {{ sendgrid_api_key }}"
}`,
    parameters_template: `{
  "sendgrid_api_key": "SG.your-api-key"
}`,
    template_slug: "sendgrid-email"
  },
  {
    name: "Generic Webhook",
    slug: "generic-webhook",
    auth_type: "basic" as any,
    description: "Generic webhook connection with custom auth",
    host: "example.com",
    endpoint: "/webhook",
    auth_template: `{
  "Authorization": "{{ auth_header }}",
  "X-API-Key": "{{ api_key }}"
}`,
    parameters_template: `{
  "auth_header": "Bearer your-token",
  "api_key": "your-api-key"
}`,
    template_slug: "generic-webhook"
  },
  {
    name: "Database API",
    slug: "database-api",
    auth_type: "bearer" as any,
    description: "Connect to database via REST API",
    host: "api.database.com",
    endpoint: "/v1",
    auth_template: `{
  "Authorization": "Bearer {{ db_token }}"
}`,
    parameters_template: `{
  "db_token": "your-database-token"
}`,
    template_slug: "database-api"
  }
];
