// Module resolution hooks so route handlers can be imported by the Node.js
// built-in test runner without a bundler:
//  - `next/server` has no "exports" map, so Node needs the explicit file name;
//  - `@karrio/lib` is a TypeScript workspace package with extension-less
//    imports, so a tiny stub (./karrio-lib-stub.mjs) stands in for it;
//  - `@karrio/core/context/auth` (NextAuth) is replaced by a session stub.
export async function resolve(specifier, context, nextResolve) {
  if (specifier === "next/server") {
    return nextResolve("next/server.js", context);
  }
  if (specifier === "@karrio/lib") {
    return {
      url: new URL("./karrio-lib-stub.mjs", import.meta.url).href,
      shortCircuit: true,
    };
  }
  if (specifier === "@karrio/core/context/auth") {
    return {
      url: new URL("./karrio-core-auth-stub.mjs", import.meta.url).href,
      shortCircuit: true,
    };
  }
  return nextResolve(specifier, context);
}
