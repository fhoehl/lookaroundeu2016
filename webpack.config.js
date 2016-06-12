var webpack = require('webpack');
var HtmlWebpackPlugin = require('html-webpack-plugin');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var path = require('path');

module.exports = {
  entry: './src',
  output: {
    path: path.join(__dirname, 'dist'),
    filename: '[hash].bundle.js',
    publicPath: 'http://139.59.173.245/',
  },
  module: {
    loaders: [{
      test: /\.css$/,
      loader: ExtractTextPlugin.extract('style-loader', 'css-loader!postcss-loader'),
    }, {
      test: /\.(jpg|png|ico)$/, loader: 'file-loader',
    }, {
      test: /\.ttf$/, loader: 'file-loader',
    }, {
      test: /\.svg$/, loader: 'file-loader',
    }, {
      test: /\.html$/, loader: 'html?interpolate',
    }, {
      test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'
    }]
  },
  postcss: function () {
    return [
      require('postcss-partial-import')(),
      require('postcss-import')({ path: ['src'], addDependencyTo: webpack }),
      require('stylelint')({ "rules": { "max-empty-lines": 2 }}),
      require('postcss-url')(),
      require('postcss-cssnext')(),
      require('postcss-custom-properties')(),
      require('postcss-color-function')(),
      require('postcss-browser-reporter')(),
      require('postcss-reporter')(),
    ];
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './index.html'
    }),
    new ExtractTextPlugin('[hash].main.css', {
      allChunks: false
    }),
  ]
};

