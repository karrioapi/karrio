// Stand-in for `auth` from @karrio/core/context/auth (NextAuth). Tests choose the
// session the route sees with setSession(); null means "not signed in".
let current = null;

export async function auth() {
  return current;
}

export function setSession(session) {
  current = session;
}
