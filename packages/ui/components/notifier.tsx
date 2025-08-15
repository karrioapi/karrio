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
    const variant = mapVariant(notification?.type);
    const parsed = parseMessage(notification?.message);
    if (Array.isArray(parsed)) {
      parsed.forEach(({ title, description, variant: v }) =>
        shadcnToast({ title, description, variant: v || variant }),
      );
    } else {
      shadcnToast({ variant, description: parsed as any });
    }
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
    if (!msg) return "";
    // GraphQL top-level shape
    if (msg?.errors && Array.isArray(msg.errors)) {
      return msg.errors.map((err: any) => {
        const validation = err.validation || {};
        const details = Object.entries(validation)
          .map(([field, messages]) => `${field}: ${(messages as string[]).join(" ")}`)
          .join("\n");
        return { title: err.message || "Error", description: details || undefined, variant: "destructive" };
      });
    }
    if (msg?.message && msg?.validation) {
      const details = Object.entries(msg.validation)
        .map(([field, messages]) => `${field}: ${(messages as string[]).join(" ")}`)
        .join("\n");
      return [{ title: msg.message, description: details, variant: "destructive" }];
    }
    if (msg?.message) return [{ title: "Error", description: msg.message, variant: "destructive" }];
    return formatMessage(msg);
  } catch {
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
