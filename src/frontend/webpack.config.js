const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const build_path = '../apps/client/purpleserver/client/static/purpleserver/client';

module.exports = {
  entry: './src/index.tsx',
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          'css-loader',
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
    extensions: [ '.tsx', '.ts', '.js' ],
  },
  output: {
    filename: 'purpleboard.min.js',
    path: path.resolve(__dirname, build_path),
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'purpleboard.min.css',
    }),
  ],
};