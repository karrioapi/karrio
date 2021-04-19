const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const WebpackShellPluginNext = require('webpack-shell-plugin-next');

const build_path = '../apps/client/purpleserver/client/static/client/';

module.exports = {
  entry: {
    vendor: ['rxjs', 'react', 'react-dom', 'libphonenumber-js', '@reach/router', 'graphql', '@apollo/client'],
    graph: {
      dependOn: 'vendor',
      import: ['./src/library/graphql.ts', './src/graphql/index.ts']
    },
    rest: {
      dependOn: 'vendor',
      import: './src/library/rest.ts'
    },
    dashboard: {
      dependOn: ['vendor', 'rest', 'graph'],
      import: './src/dashboard.tsx'
    },
  },
  mode: 'production',
  devtool: "source-map",
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
      {
        // For pure CSS - /\.css$/i,
        // For Sass/SCSS - /\.((c|sa|sc)ss)$/i,
        // For Less - /\.((c|le)ss)$/i,
        test: /\.((c|sa|sc)ss)$/i,
        exclude: /node_modules/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'sass-loader'
        ],
      },
      {
        test: /\.(png|jpe?g|gif|svg|eot|ttf|woff|woff2)$/i,
        loader: 'url-loader',
        options: {
          limit: 8192,
        },
      },
    ],
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
    alias: {
      "@": path.resolve(__dirname, 'src'),
    }
  },
  output: {
    filename: `purplship.[name].min.js`,
    path: path.resolve(__dirname, build_path),
  },
  optimization: {
    runtimeChunk: 'single',
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: `purplship.dashboard.min.css`
    }),
    new WebpackShellPluginNext({
      onAfterDone: { scripts: ['purplship collectstatic --noinput'], blocking: false, parallel: true },
    }),
  ],
};