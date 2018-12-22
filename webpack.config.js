const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');


module.exports = (env, argv) => {
  const config = {
    entry: {'wagtail-react-streamfield': [
        './wagtail_react_streamfield/static_src/js/entry.js',
        './wagtail_react_streamfield/static_src/scss/entry.scss',
      ]},
    output: {
      path: path.resolve('wagtail_react_streamfield/static'),
      filename: 'js/[name].js',
      publicPath: '/static/'
    },
    module: {
      rules: [
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
