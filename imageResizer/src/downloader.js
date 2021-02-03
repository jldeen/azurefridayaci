const fs = require("fs");
const imageDownload = require('image-download');
// const imageDownload = require('image-downloader');
const util = require('util');

const writeToFile = util.promisify(fs.writeFile);

async function download(url, fileName) {

    let buffer = await imageDownload(url);

    const filePath = './tmp/' + fileName;

    try {
        await writeToFile(filePath, buffer);
        return Promise.resolve(fileName);
    } catch (e) {
        return Promise.reject(err);
    }

}


module.exports = {
     download
}