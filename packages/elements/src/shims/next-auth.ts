// Shim for next-auth/react - all auth is handled by KarrioEmbedProvider
export function useSession() {
  return { data: null, status: "unauthenticated" as const };
}

export function getSession() {
  return Promise.resolve(null);
}

export function signOut() {
  return Promise.resolve();
}

export function signIn() {
  return Promise.resolve();
}

export default {};
