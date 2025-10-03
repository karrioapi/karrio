const argv = require('yargs').argv;
const gulp = require('gulp');
const rollup = require('rollup');
const rollupTypescript = require('@rollup/plugin-typescript');

const output = argv.output === undefined ? './dist/karrio.js' : argv.output;

gulp.task('build', async function () {
  const bundle = await rollup.rollup({
    input: './api/karrio.ts',
    plugins: [
      rollupTypescript()
    ]
  });

  await bundle.write({
    file: output,
    format: 'iife',
    name: 'Karrio',
    sourcemap: true,
  });
});
