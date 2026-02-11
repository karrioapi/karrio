// Shim: provides a minimal `require` for the lodash CJS calls in @karrio/lib/helper.ts
// Vite's ESM build cannot handle bare `require()` calls, so we polyfill just the four
// lodash micro-packages used by helper.ts.
import _isEqual from "lodash.isequal";
import _snakeCase from "lodash.snakecase";
import _groupBy from "lodash.groupby";
import _toNumber from "lodash.tonumber";

const modules: Record<string, any> = {
  "lodash.isequal": _isEqual,
  "lodash.snakecase": _snakeCase,
  "lodash.groupby": _groupBy,
  "lodash.tonumber": _toNumber,
};

(globalThis as any).require = (id: string) => {
  if (id in modules) return modules[id];
  throw new Error(`[karrio-elements] require("${id}") is not shimmed`);
};
