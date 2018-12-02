const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');


module.exports = (env, argv) => {
  const config = {
    entry: {'wagtail-react-streamfield': './wagtail_react_streamfield/static_src/js/entry.js'},
    output: {
      path: path.resolve('wagtail_react_streamfield/static'),
      filename: 'js/[name].js',
      publicPath: '/static/'
    },
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          loader: 'babel-loader',
          options: {
            presets: [
              '@babel/preset-env',
              '@babel/preset-react'
            ],
            'plugins': [
              '@babel/plugin-proposal-class-properties',
              [
                '@babel/plugin-proposal-decorators',
                {
                  'legacy': true
                }
              ],
              '@babel/plugin-proposal-object-rest-spread'
            ]
          }
        },
        {
          test: /\.scss$/,
          use: [
            MiniCssExtractPlugin.loader,
            'css-loader',
            'sass-loader',
          ]
        },
      ],
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: 'css/[name].css',
        chunkFilename: 'css/[id].css',
      }),
    ],
  };

  if (argv.mode === 'production') {
    config.optimization = {
      minimizer: [
        new UglifyJsPlugin({
          cache: true,
          parallel: true,
          uglifyOptions: {
            output: {
              comments: false,
              beautify: false
            },
            compress: {
              drop_console: true,
              hoist_funs: true,
              passes: 2,
              toplevel: true,
              warnings: true
            }
          }
        })
      ]
    }
  }
  return config;
};
