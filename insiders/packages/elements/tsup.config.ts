import { defineConfig } from 'tsup';

export default defineConfig({
    entry: ['src/index.tsx'],
    format: ['cjs', 'esm'],
    dts: true,
    clean: true,
    sourcemap: true,
    external: ['react', 'react-dom'],
    esbuildOptions(options) {
        options.alias = {
            '@karrio/elements': './src'
        };
    }
});
