/**
 * Auth utility functions for Karrio
 */

/**
 * Check if a user is authenticated by looking for required auth tokens in localStorage
 * @returns boolean indicating if user is authenticated
 */
export function isAuthenticated(): boolean {
  if (typeof window === 'undefined') {
    return false;
  }

  const accessToken = localStorage.getItem('karrio_access_token');
  const userId = localStorage.getItem('karrio_user_id');
  const tokenExpiry = localStorage.getItem('karrio_token_expiry');

  if (!accessToken || !userId || !tokenExpiry) {
    return false;
  }

  // Check if the token is expired
  const expiryDate = new Date(tokenExpiry);
  const now = new Date();

  return expiryDate > now;
}

/**
 * Get the current user ID if authenticated
 * @returns user ID or null if not authenticated
 */
export function getUserId(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }

  return localStorage.getItem('karrio_user_id');
}

/**
 * Get the current access token if authenticated
 * @returns access token or null if not authenticated
 */
export function getAccessToken(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }

  const tokenExpiry = localStorage.getItem('karrio_token_expiry');
  if (!tokenExpiry) {
    return null;
  }

  // Check if the token is expired
  const expiryDate = new Date(tokenExpiry);
  const now = new Date();

  if (expiryDate <= now) {
    return null;
  }

  return localStorage.getItem('karrio_access_token');
}

/**
 * Clear all authentication data
 */
export function clearAuthData(): void {
  if (typeof window === 'undefined') {
    return;
  }

  localStorage.removeItem('karrio_access_token');
  localStorage.removeItem('karrio_refresh_token');
  localStorage.removeItem('karrio_token_expiry');
  localStorage.removeItem('karrio_user_id');
}
