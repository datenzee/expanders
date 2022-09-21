const path = require('path')

const CopyPlugin = require("copy-webpack-plugin")
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
    entry: [
        './src/main.js',
        './src/assets/main.css'
    ],
    output: {
        path: path.resolve(__dirname, './dist'),
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
            {
                test: /\.css$/,
                use: [
                    // 'vue-style-loader',
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                ]
            }
        ]
    },
    plugins: [
        new VueLoaderPlugin(),
        new CopyPlugin({
            patterns: [
                { from: 'public', to: '' }
            ]
        }), 
        new MiniCssExtractPlugin({
            filename: '[name].css'
        }),
    ],
    resolve: {
        fallback: {
            buffer: require.resolve('buffer/')
        },
        alias: {
            '@': path.resolve(__dirname, './src')
        },
        extensions: ['.js', '.vue', '.json']
    },
    devServer: {
        static: {
            directory: path.join(__dirname, 'public'),
        },
        liveReload: true,
        hot: true,
        port: 8081
    }
}
