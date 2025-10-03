"use client";
import {
  FieldError,
  NotificationType,
  Notification,
  RequestError,
  ErrorType,
} from "@karrio/types";
import React from "react";
import { toast as shadcnToast } from "@karrio/ui/hooks/use-toast";

interface LoadingNotifier {
  notify: (notification: Notification) => void;
}

export const Notify = React.createContext<LoadingNotifier>({} as LoadingNotifier);

export const Notifier = ({ children }: { children?: React.ReactNode }): JSX.Element => {
  const notify = (notification: Notification) => {
    console.log("=== NOTIFY FUNCTION DEBUG ===");
    console.log("Notification:", notification);
    console.log("Notification type:", notification?.type);
    console.log("Notification message:", notification?.message);
    
    const variant = mapVariant(notification?.type);
    console.log("Mapped variant:", variant);
    
    const parsed = parseMessage(notification?.message);
    console.log("Parsed result:", parsed);
    console.log("Is parsed array:", Array.isArray(parsed));
    
    if (Array.isArray(parsed)) {
      console.log("Calling shadcnToast for each parsed item");
      parsed.forEach(({ title, description, variant: v }, index) => {
        console.log(`Toast ${index}:`, { title, description, variant: v || variant });
        shadcnToast({ title, description, variant: v || variant });
      });
    } else {
      console.log("Calling shadcnToast with single item:", { variant, description: parsed });
      shadcnToast({ variant, description: parsed as any });
    }
    console.log("=== END NOTIFY DEBUG ===");
  };

  return <Notify.Provider value={{ notify }}>{children}</Notify.Provider>;
};

export function useNotifier() {
  return React.useContext(Notify);
}

function mapVariant(type?: NotificationType | string): "default" | "destructive" {
  const t = String(type || "").toLowerCase();
  if (t.includes("danger") || t.includes("error") || t.includes("warning")) return "destructive";
  return "default";
}

export function formatMessage(msg: Notification["message"]) {
  try {
    if (typeof msg === "string") return msg;
    if (Array.isArray(msg) && msg.length > 0 && msg[0] instanceof ErrorType) {
      return msg.map((error: any, index) => (
        <p key={`error-${index}-${error.field}`}>
          <strong>{error.field}:</strong> {error.messages.join(" | ")}
        </p>
      ));
    }
    if (Array.isArray(msg) && msg.length > 0) return renderError(msg, 0);
    if (msg instanceof RequestError) return renderError(msg, 0);
    return (msg as any).message;
  } catch (e) {
    return "Uh Oh! An uncaught error occured...";
  }
}

function parseMessage(msg: any):
  | string
  | Array<{ title?: string; description?: string; variant?: "default" | "destructive" }>
{
  try {
    console.log("=== PARSE MESSAGE DEBUG ===");
    console.log("Input message:", msg);
    console.log("Type:", typeof msg);
    console.log("Is array:", Array.isArray(msg));
    console.log("Has errors:", !!msg?.errors);
    console.log("Has messages:", !!msg?.messages);
    console.log("Has message:", !!msg?.message);
    
    if (!msg) {
      console.log("Message is empty, returning empty string");
      return "";
    }
    // GraphQL top-level shape
    if (msg?.errors && Array.isArray(msg.errors)) {
      console.log("Processing GraphQL errors");
      return msg.errors.map((err: any) => {
        const validation = err.validation || {};
        const details = Object.entries(validation)
          .map(([field, messages]) => `${field}: ${(messages as string[]).join(" ")}`)
          .join("\n");
        return { title: err.message || "Error", description: details || undefined, variant: "destructive" };
      });
    }
    // REST API messages array (like tracker creation errors)
    if (msg?.messages && Array.isArray(msg.messages)) {
      console.log("Processing REST API messages array:", msg.messages);
      const result = msg.messages.map((err: any) => {
        const title = err.carrier_name ? `${err.carrier_name} (${err.code || "Error"})` : (err.code || "Error");
        console.log("Creating toast with title:", title, "description:", err.message);
        return { title, description: err.message, variant: "destructive" };
      });
      console.log("Final REST API result:", result);
      return result;
    }
    if (msg?.message && msg?.validation) {
      console.log("Processing message with validation");
      const details = Object.entries(msg.validation)
        .map(([field, messages]) => `${field}: ${(messages as string[]).join(" ")}`)
        .join("\n");
      return [{ title: msg.message, description: details, variant: "destructive" }];
    }
    if (msg?.message) {
      console.log("Processing simple message:", msg.message);
      return [{ title: "Error", description: msg.message, variant: "destructive" }];
    }
    console.log("Falling back to formatMessage");
    const result = formatMessage(msg);
    console.log("formatMessage result:", result);
    console.log("=== END PARSE MESSAGE DEBUG ===");
    return result;
  } catch (e) {
    console.log("Error in parseMessage:", e);
    console.log("=== END PARSE MESSAGE DEBUG ===");
    return formatMessage(msg);
  }
}

function renderError(msg: any, _: number): any {
  const error = msg.data?.errors || msg.data?.messages || msg;
  if (error?.message !== undefined) return error.message;
  if (error?.details?.messages !== undefined) {
    return (error.details.messages || []).map((m: any, i: number) => (
      <p key={`msg-${i}-${m.code || "unknown"}`}>{m.message}</p>
    ));
  }
  if (Array.isArray(error) && error.length > 0) {
    return (error || []).map((m: any, i: number) => (
      <p key={`message-${i}-${m.code || "unknown"}`}>{m.message || JSON.stringify(m)}</p>
    ));
  }
  if (typeof error?.details == "object") {
    return Object.entries(error?.details as FieldError).map(([field, val], i) => (
      <span className="is-size-7" key={`details-${i}`}>{field}: {formatMessageObject(val)}</span>
    ));
  }
  return formatMessageObject(error);
}

function formatMessageObject(msg: any) {
  if (msg?.message) return msg.message;
  if (typeof msg === "string") return msg;
  if (Array.isArray(msg) && typeof msg[0] === "string") return msg.join(" ");
  if (typeof msg === "object") return "";
}
