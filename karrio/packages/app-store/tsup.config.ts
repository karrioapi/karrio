import { defineConfig } from 'tsup';

export default defineConfig({
  entry: ['index.ts'],
  format: ['cjs', 'esm'],
  dts: {
    compilerOptions: {
      incremental: false
    }
  },
  clean: true,
  sourcemap: true,
  external: ['react', 'react-dom'],
  esbuildOptions(options) {
    options.alias = {
      '@karrio/app-store': './'
    };
  }
});
