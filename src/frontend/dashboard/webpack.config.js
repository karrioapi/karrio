const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const WebpackShellPlugin = require('webpack-shell-plugin');

const build_path = '../../apps/client/purpleserver/client/static/purpleserver/client';

module.exports = {
  entry: './src/dashboard.tsx',
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
        use: ['style-loader', 'css-loader'],
      },
      {
        // For pure CSS - /\.css$/i,
        // For Sass/SCSS - /\.((c|sa|sc)ss)$/i,
        // For Less - /\.((c|le)ss)$/i,
        test: /\.((c|sa|sc)ss)$/i,
        exclude: /node_modules/,
        use: [
          'style-loader',
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
            options: {
              importLoaders: 1,
              modules: { auto: true },
            },
          },
          {
            loader: 'sass-loader',
          },
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
    extensions: [ '.ts', '.tsx', '.js' ],
    alias: {
      "@": path.resolve(__dirname, 'src'),
    }
  },
  output: {
    filename: 'purpleboard.min.js',
    path: path.resolve(__dirname, build_path),
  },
  plugins: [
    new MiniCssExtractPlugin({ filename: 'purpleboard.min.css' }),
    new WebpackShellPlugin({ onBuildEnd:['purplship collectstatic --noinput'] }),
  ],
};