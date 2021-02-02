const fs = require("fs");
const imageDownload = require('image-download');
const util = require('util');

const writeToFile = util.promisify(fs.writeFile);

async function download(url, fileName) {

    let buffer = await imageDownload(url);
    console.log("Provided image URL: " + url)
    console.log("Downloading image now...")

    const filePath = './images/originals/' + fileName;

    try {
        await writeToFile(filePath, buffer);
        console.log("Original image succesfully downloaded! Saved in: " + filePath)
        return Promise.resolve(fileName);
    } catch (e) {
        console.log("Error!" + e)
        return Promise.reject(err);
    }

}


module.exports = {
     download
}