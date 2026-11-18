// Registered with `node --import` (see the "test" script in package.json).
import { register } from "node:module";

register("./loader.mjs", import.meta.url);
