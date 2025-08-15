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

const shadcnNotify = (notification: Notification) => {
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

export const Notify = React.createContext<LoadingNotifier>({
  notify: shadcnNotify,
});

export const Notifier = ({ children }: { children?: React.ReactNode }): JSX.Element => (
  <Notify.Provider value={{ notify: shadcnNotify }}>
    {children}
  </Notify.Provider>
);

export function formatMessage(msg: Notification["message"]) {
  try {
    // Process plain text message
    if (typeof msg === "string") {
      return msg;
    }

    // Process GraphQL errors
    if (Array.isArray(msg) && msg.length > 0 && msg[0] instanceof ErrorType) {
      return msg.map((error: any, index) => {
        return (
          <p key={`error-${index}-${error.field}`}>
            <strong>{error.field}:</strong> {error.messages.join(" | ")}
          </p>
        );
      });
    }

    // Process Rest Request errors
    if (Array.isArray(msg) && msg.length > 0) {
      return renderError(msg, 0);
    }

    // Process API errors
    if (msg instanceof RequestError) {
      return renderError(msg, 0);
    }

    return (msg as any).message;
  } catch (e) {
    console.log("Failed to parse error");
    console.error(e);
    return "Uh Oh! An uncaught error occured...";
  }
}

// Parse GraphQL-style errors into toast payloads
function parseMessage(msg: any):
  | string
  | Array<{ title?: string; description?: string; variant?: "default" | "destructive" }>
{
  try {
    if (!msg) return "";
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

function mapVariant(type?: NotificationType | string): "default" | "destructive" {
  const t = String(type || "").toLowerCase();
  if (t.includes("danger") || t.includes("error") || t.includes("warning")) return "destructive";
  return "default";
}

function renderError(msg: any, _: number): any {
  const error = msg.data?.errors || msg.data?.messages || msg;
  if (error?.message !== undefined) {
    return error.message;
  } else if (error?.details?.messages !== undefined) {
    return (error.details.messages || []).map((msg: any, index: number) => {
      const carrier_name =
        msg.carrier_name !== undefined ? `${msg.carrier_id} :` : "";
      return (
        <p key={`msg-${index}-${msg.carrier_id || 'unknown'}`}>
          {carrier_name} {msg.message}
        </p>
      );
    });
  } else if (Array.isArray(error) && error.length > 0) {
    return (error || []).map((msg: any, index: number) => {
      if (msg.carrier_name) {
        return (
          <p key={`carrier-${index}-${msg.carrier_name || msg.carrier_id}`}>
            {msg.carrier_name || msg.carrier_id || JSON.stringify(msg)}{" "}
            {msg.details?.carrier} {msg.message}
          </p>
        );
      }
      if (msg.details) {
        return <React.Fragment key={`details-${index}`}>{renderError(msg, 0)}</React.Fragment>;
      }
      if (msg.validation) {
        return <React.Fragment key={`validation-${index}`}>{renderError({ details: msg.validation }, 0)}</React.Fragment>;
      }
      if (msg.message) {
        return (
          <p key={`message-${index}-${msg.code || 'unknown'}`}>
            <strong>{JSON.stringify(msg.code)}:</strong> {msg.message}
          </p>
        );
      }
      return <p key={`json-${index}`}>{JSON.stringify(msg)}</p>;
    });
  } else if (typeof error?.details == "object") {
    const render = (
      [field, msg]: [string, string | FieldError],
      index: number,
    ) => {
      let text = formatMessageObject(msg);
      return (
        <React.Fragment key={index}>
          <span className="is-size-7">
            {field} {formatMessageObject(msg).length > 0 && ` - ${text}`}
          </span>
          {!(msg as any).message && (
            <ul className="pl-1">
              <li className="is-size-7">
                {!Array.isArray(msg) &&
                  typeof msg === "object" &&
                  !msg.message &&
                  Object.entries(msg).map(render as any)}
              </li>
            </ul>
          )}
          <br />
        </React.Fragment>
      );
    };
    return Object.entries(error?.details as FieldError).map(render as any);
  }

  return formatMessageObject(error);
}

function formatMessageObject(msg: any) {
  if (msg.message) return msg.message;
  if (typeof msg === "string") return msg;
  if (Array.isArray(msg) && typeof msg[0] === "string") return msg.join(" ");
  if (typeof msg === "object") return "";
}

export function useNotifier() {
  return React.useContext(Notify);
}
