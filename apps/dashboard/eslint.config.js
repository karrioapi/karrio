//  @ts-check

import { tanstackConfig } from '@tanstack/eslint-config'

export default [
  ...tanstackConfig,
  {
    ignores: [
      '.output/**',
      '.nitro/**',
      'dist/**',
      'build/**',
      'node_modules/**',
      'src/routeTree.gen.ts',
      'eslint.config.js',
      'prettier.config.js',
      'postcss.config.ts',
      'vite.config.ts',
    ],
  },
]
