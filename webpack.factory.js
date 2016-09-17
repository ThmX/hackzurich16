'use strict';

var path = require('path');
var webpack = require('webpack');

var webpackCommon = {
    devtool: 'source-map',
    progress: false,
    stats: {
        colors: true,
        modules: false,
        reasons: true
    },
    node: {
        fs: 'empty' // https://github.com/webpack/jade-loader/issues/8#issuecomment-55568520
    },
    resolve: {
        extensions: ['', '.ts', '.js'],
        alias: {
            spin: 'spin.js'
        }
    },
    plugins: [],
    module: {
        preLoaders: [],
        loaders: [{
            test: /\.js$/,
            loaders: ['babel', 'angular2-template'],
            exclude: [path.resolve('node_modules/')]
        },{
            test: /\.ts$/,
            loaders: ['awesome-typescript', 'angular2-template']
        },{
            test: /\.(html|css)$/,
            loader: 'raw'
        },{
            test: /\.scss$/,
            loaders: ['raw', 'sass']
        }],
        postLoaders: []
    }
};

function webpackConfigFactory(src, prod, options) {
    var wpConfig = Object.assign({}, webpackCommon);

    // https://github.com/AngularClass/angular2-webpack-starter/issues/993
    wpConfig.plugins.push(
        new webpack.ContextReplacementPlugin(
            /angular(\\|\/)core(\\|\/)(esm(\\|\/)src|src)(\\|\/)linker/,
            src
        )
    );

    if (prod) {
        wpConfig.plugins.push(
            new webpack.optimize.UglifyJsPlugin({
                compress: {
                    warnings: false
                },
                mangle: {
                    except: ['$super', '$', 'exports', 'require']
                }
            })
        );
    }

    return Object.assign({}, webpackCommon, options ? options : {});
}

module.exports = webpackConfigFactory;