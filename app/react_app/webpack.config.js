const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
    entry: {
        jobsList: "./src/JobsList.tsx",
        jobDetails: "./src/JobDetails.tsx",
        form: "./src/Form.tsx",
        configplan: "./src/ConfigPlan.tsx",
    },
    output: {
        path: path.resolve("./../static/react_components/"),
        filename: "[name].js",
        publicPath: "/static/react_components/",
    },
    plugins: [
        new CleanWebpackPlugin(),
        new BundleTracker({
            path: __dirname,
            filename: "webpack-stats.json",
        }),
    ],
    module: {
        rules: [
            {
                test: /\.tsx$/,
                exclude: /node_modules/,
                use: ["ts-loader"],
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"],
            },
        ],
    },
    resolve: {
        extensions: [".tsx", ".ts", ".js"],
    },
};
