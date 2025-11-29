import {
  OAUTH_STORAGE_KEY,
  retrieveEncryptedOAuthResult,
} from "@karrio/lib";
import { useCarrierConnections } from "./user-connection";
import { useSystemConnections } from "./system-connection";
import { useKarrio } from "./karrio";
import React, { useCallback, useEffect, useRef, useState } from "react";

export function useConnections() {
  const [carrierOptions, setCarrierOptions] = React.useState<
    Record<string, string[]>
  >({});
  const {
    query: { isFetched: isUserFetched },
    user_connections,
  } = useCarrierConnections();
  const {
    query: { isFetched: isSystemFetched },
    system_connections,
  } = useSystemConnections();

  const memoizedUserConnections = React.useMemo(() => user_connections, [JSON.stringify(user_connections)]);
  const memoizedSystemConnections = React.useMemo(() => system_connections, [JSON.stringify(system_connections)]);

  React.useEffect(() => {
    if (!isUserFetched || !isSystemFetched) {
      return;
    }

    const newCarrierOptions = [...memoizedUserConnections, ...memoizedSystemConnections]
      .filter((_) => _.active && (_.config?.shipping_options || []).length > 0)
      .reduce(
        (acc, _) => ({
          ...acc,
          [_.carrier_name]: [
            ...(new Set<string>([
              ...((acc[_.carrier_name] as string[]) || []),
              ...(_.config?.shipping_options || []),
            ]) as any),
          ],
        }),
        {} as Record<string, string[]>
      );

    setCarrierOptions(newCarrierOptions);
  }, [isUserFetched, isSystemFetched, memoizedUserConnections, memoizedSystemConnections]);

  return {
    carrierOptions,
  };
}


// =============================================================================
// OAuth Connection Management
// =============================================================================

export interface OAuthCallbackResult {
  type: "oauth_callback";
  success: boolean;
  carrier_name: string;
  credentials: Record<string, any> | null;
  messages: Array<{ code: string; message: string }>;
  state: string | null;
}

export interface OAuthAuthorizeResponse {
  operation: string;
  request: {
    carrier_name: string;
    authorization_url: string;
    state?: string;
    meta?: Record<string, any>;
  };
  messages: Array<{ code: string; message: string }>;
}

export interface UseOAuthConnectionOptions {
  onSuccess?: (result: OAuthCallbackResult) => void;
  onError?: (error: Error | OAuthCallbackResult) => void;
}


/**
 * Hook for managing OAuth connection flows with carrier integrations.
 *
 * Handles:
 * - Initiating OAuth authorization requests
 * - Opening OAuth popup windows
 * - Receiving credentials from OAuth callbacks via sessionStorage polling
 */
export function useOAuthConnection(options: UseOAuthConnectionOptions = {}) {
  const karrio = useKarrio();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const popupRef = useRef<Window | null>(null);
  const pollTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Use refs for callbacks to avoid stale closures in polling intervals
  const onSuccessRef = useRef(options.onSuccess);
  const onErrorRef = useRef(options.onError);

  // Keep refs updated with latest callbacks
  useEffect(() => {
    onSuccessRef.current = options.onSuccess;
    onErrorRef.current = options.onError;
  }, [options.onSuccess, options.onError]);

  /**
   * Clears the OAuth result from localStorage
   */
  const clearOAuthResult = useCallback(() => {
    try {
      localStorage.removeItem(OAUTH_STORAGE_KEY);
    } catch (e) {
      console.error("Failed to clear OAuth result from localStorage:", e);
    }
  }, []);

  /**
   * Checks localStorage for encrypted OAuth result, decrypts it, and returns the data.
   * Uses localStorage (not sessionStorage) because popup windows have separate
   * sessionStorage contexts from their opener window.
   * Data is encrypted with AES-GCM for security.
   */
  const checkForOAuthResult = useCallback(async (): Promise<OAuthCallbackResult | null> => {
    try {
      const result = await retrieveEncryptedOAuthResult<OAuthCallbackResult>();
      if (result?.type === "oauth_callback") {
        console.log("[OAuth] Retrieved credentials:", result.credentials ? "present" : "missing");
        return result;
      }
      return null;
    } catch (e) {
      console.error("[OAuth] Failed to check for result:", e);
      return null;
    }
  }, []);

  /**
   * Cleanup function to stop polling and close popup
   */
  const cleanup = useCallback(() => {
    if (pollTimerRef.current) {
      clearInterval(pollTimerRef.current);
      pollTimerRef.current = null;
    }
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
    if (popupRef.current && !popupRef.current.closed) {
      popupRef.current.close();
    }
    popupRef.current = null;
  }, []);

  /**
   * Gets the frontend callback URL for OAuth redirects
   */
  const getFrontendCallbackUrl = useCallback(() => {
    // Return the current origin + /oauth/callback path
    return `${window.location.origin}/oauth/callback`;
  }, []);

  /**
   * Initiates the OAuth authorization flow for a carrier.
   *
   * @param carrierName - The carrier to authorize (e.g., "teleship")
   * @param state - Optional state parameter for CSRF protection
   * @returns Promise that resolves with OAuth callback result
   */
  const initiateOAuth = useCallback(
    async (
      carrierName: string,
      state?: string,
    ): Promise<OAuthCallbackResult> => {
      setIsLoading(true);
      setError(null);

      // Clear any previous OAuth result
      clearOAuthResult();

      try {
        // Generate state with frontend_url for callback redirect
        const oauthState =
          state ||
          btoa(
            JSON.stringify({
              carrier: carrierName,
              timestamp: Date.now(),
              nonce: Math.random().toString(36).substring(2),
              frontend_url: getFrontendCallbackUrl(),
            }),
          );

        // Request authorization URL from backend
        const response = await karrio.axios.post<OAuthAuthorizeResponse>(
          `/v1/connections/oauth/${carrierName}/authorize`,
          { state: oauthState },
        );

        const { request: authRequest, messages } = response.data;

        // Check for errors in the response
        if (messages?.length > 0) {
          const errorMessages = messages.filter(
            (m) => m.code?.includes("ERROR") || m.code?.includes("error"),
          );
          if (errorMessages.length > 0) {
            throw new Error(errorMessages.map((m) => m.message).join("; "));
          }
        }

        if (!authRequest?.authorization_url) {
          throw new Error("No authorization URL received from server");
        }

        // Open OAuth popup
        const popup = openOAuthPopup(authRequest.authorization_url);
        popupRef.current = popup;

        // Create promise that will be resolved by localStorage polling
        return new Promise<OAuthCallbackResult>((resolve, reject) => {
          // Set a timeout for the OAuth flow (5 minutes)
          timeoutRef.current = setTimeout(() => {
            cleanup();
            clearOAuthResult();
            setIsLoading(false);
            reject(new Error("OAuth authorization timed out"));
          }, 5 * 60 * 1000);

          // Process OAuth result and resolve/reject promise
          const handleResult = (result: OAuthCallbackResult) => {
            cleanup();
            setIsLoading(false);

            if (result.success && result.credentials) {
              onSuccessRef.current?.(result);
              resolve(result);
            } else {
              const errorMessage = result.messages?.[0]?.message || "OAuth authorization failed";
              onErrorRef.current?.(result);
              reject(new Error(errorMessage));
            }
          };

          // Poll sessionStorage for the OAuth result (async due to decryption)
          const pollForResult = async () => {
            const result = await checkForOAuthResult();

            if (result) {
              handleResult(result);
              return true;
            }

            // Popup closed manually - give grace period then check one more time
            if (popupRef.current?.closed) {
              if (pollTimerRef.current) {
                clearInterval(pollTimerRef.current);
                pollTimerRef.current = null;
              }

              setTimeout(async () => {
                const delayedResult = await checkForOAuthResult();
                delayedResult
                  ? handleResult(delayedResult)
                  : (cleanup(), setIsLoading(false), reject(new Error(
                      "Authorization was cancelled or failed. This may occur if the OAuth credentials are invalid or misconfigured."
                    )));
              }, 200);

              return true;
            }

            return false;
          };

          pollTimerRef.current = setInterval(async () => {
            await pollForResult();
          }, 500);
        });
      } catch (err: any) {
        cleanup();
        const error =
          err instanceof Error
            ? err
            : new Error(
                err?.response?.data?.message || "OAuth initiation failed",
              );
        setError(error);
        setIsLoading(false);
        throw error;
      }
    },
    [
      karrio.axios,
      cleanup,
      clearOAuthResult,
      checkForOAuthResult,
      getFrontendCallbackUrl,
    ],
  );

  /**
   * Cancels any ongoing OAuth flow.
   */
  const cancelOAuth = useCallback(() => {
    cleanup();
    clearOAuthResult();
    setIsLoading(false);
  }, [cleanup, clearOAuthResult]);

  return {
    initiateOAuth,
    cancelOAuth,
    isLoading,
    error,
  };
}

/**
 * Opens a centered popup window for OAuth authorization.
 */
function openOAuthPopup(url: string, name = "oauth_popup"): Window {
  const width = 600;
  const height = 700;
  const left = window.screenX + (window.outerWidth - width) / 2;
  const top = window.screenY + (window.outerHeight - height) / 2;

  const features = [
    `width=${width}`,
    `height=${height}`,
    `left=${left}`,
    `top=${top}`,
    "toolbar=no",
    "menubar=no",
    "scrollbars=yes",
    "resizable=yes",
  ].join(",");

  const popup = window.open(url, name, features);

  if (!popup) {
    throw new Error(
      "Failed to open OAuth popup. Please check your popup blocker settings.",
    );
  }

  popup.focus();
  return popup;
}

/**
 * Checks if a carrier supports OAuth authentication.
 */
export function supportsOAuth(
  carrierName: string,
  capabilities?: Record<string, string[]>,
): boolean {
  if (!capabilities || !carrierName) return false;
  const carrierCapabilities = capabilities[carrierName] || [];
  return carrierCapabilities.includes("oauth");
}


// =============================================================================
// Carrier Webhook Management
// =============================================================================

export interface CarrierWebhookRegistrationResult {
  operation: string;
  success: boolean;
  carrier_name: string;
  carrier_id: string;
  webhook_id: string | null;
  webhook_url: string | null;
  messages: Array<{ code?: string; message: string }>;
}

export interface CarrierWebhookDeregistrationResult {
  operation: string;
  success: boolean;
  carrier_name: string;
  carrier_id: string;
  messages: Array<{ code?: string; message: string }>;
}

export interface UseCarrierWebhookOptions {
  onSuccess?: (result: CarrierWebhookRegistrationResult | CarrierWebhookDeregistrationResult) => void;
  onError?: (error: Error) => void;
}

/**
 * Hook for managing webhook registration/deregistration for carrier connections.
 *
 * Handles:
 * - Registering webhooks with carriers (e.g., Teleship)
 * - Deregistering webhooks from carriers
 * - Loading states and error handling
 */
export function useCarrierWebhook(options: UseCarrierWebhookOptions = {}) {
  const karrio = useKarrio();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  /**
   * Register a webhook for a carrier connection.
   *
   * @param connectionId - The connection ID (pk) to register webhook for
   * @param enabledEvents - Optional array of events to subscribe to (defaults to ["*"])
   * @param description - Optional description for the webhook
   * @returns Promise with webhook registration result
   */
  const registerWebhook = useCallback(
    async (
      connectionId: string,
      enabledEvents?: string[],
      description?: string,
    ): Promise<CarrierWebhookRegistrationResult> => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await karrio.axios.post<CarrierWebhookRegistrationResult>(
          `/v1/connections/webhook/${connectionId}/register`,
          {
            enabled_events: enabledEvents || ["*"],
            description,
          },
        );

        const result = response.data;

        if (result.success) {
          options.onSuccess?.(result);
        } else {
          const errorMessage =
            result.messages?.[0]?.message || "Webhook registration failed";
          const error = new Error(errorMessage);
          options.onError?.(error);
          throw error;
        }

        return result;
      } catch (err: any) {
        const error =
          err instanceof Error
            ? err
            : new Error(
                err?.response?.data?.message || "Webhook registration failed",
              );
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [karrio.axios, options],
  );

  /**
   * Deregister a webhook for a carrier connection.
   *
   * @param connectionId - The connection ID (pk) to deregister webhook for
   * @returns Promise with webhook deregistration result
   */
  const deregisterWebhook = useCallback(
    async (connectionId: string): Promise<CarrierWebhookDeregistrationResult> => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await karrio.axios.post<CarrierWebhookDeregistrationResult>(
          `/v1/connections/webhook/${connectionId}/deregister`,
        );

        const result = response.data;

        if (result.success) {
          options.onSuccess?.(result);
        } else {
          const errorMessage =
            result.messages?.[0]?.message || "Webhook deregistration failed";
          const error = new Error(errorMessage);
          options.onError?.(error);
          throw error;
        }

        return result;
      } catch (err: any) {
        const error =
          err instanceof Error
            ? err
            : new Error(
                err?.response?.data?.message || "Webhook deregistration failed",
              );
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [karrio.axios, options],
  );

  /**
   * Force disconnect a webhook for a carrier connection (local only).
   *
   * This clears the local webhook configuration without calling the carrier's API.
   * Use this when the carrier's API is unavailable or when cleaning up stale config.
   *
   * @param connectionId - The connection ID (pk) to disconnect webhook for
   * @returns Promise with webhook disconnect result
   */
  const disconnectWebhook = useCallback(
    async (connectionId: string): Promise<CarrierWebhookDeregistrationResult> => {
      setIsLoading(true);
      setError(null);

      try {
        const response = await karrio.axios.post<CarrierWebhookDeregistrationResult>(
          `/v1/connections/webhook/${connectionId}/disconnect`,
        );

        const result = response.data;

        if (result.success) {
          options.onSuccess?.(result);
        } else {
          const errorMessage =
            result.messages?.[0]?.message || "Webhook disconnect failed";
          const error = new Error(errorMessage);
          options.onError?.(error);
          throw error;
        }

        return result;
      } catch (err: any) {
        const error =
          err instanceof Error
            ? err
            : new Error(
                err?.response?.data?.message || "Webhook disconnect failed",
              );
        setError(error);
        throw error;
      } finally {
        setIsLoading(false);
      }
    },
    [karrio.axios, options],
  );

  return {
    registerWebhook,
    deregisterWebhook,
    disconnectWebhook,
    isLoading,
    error,
  };
}

/**
 * Checks if a carrier supports webhook registration.
 */
export function supportsWebhook(
  carrierName: string,
  capabilities?: Record<string, string[]>,
): boolean {
  if (!capabilities || !carrierName) return false;
  const carrierCapabilities = capabilities[carrierName] || [];
  return carrierCapabilities.includes("webhook");
}
