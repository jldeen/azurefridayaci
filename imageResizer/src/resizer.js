const paramHelper = require('./param-helper');
const sharp = require('sharp');
const config = require('../config');

async function resize(filePath, params) {

    try {

        const resizedImageName = paramHelper.getResizedFileName(params);
        const resizedImagePath = './tmp/' + resizedImageName;

            await sharp(filePath)
                .resize(params.width, params.height, {
                    kernel: sharp.kernel.nearest,
                    fit: params.fit,
                    background: config.ImageBackground
                })
                .toFormat(params.format)
                .toFile(resizedImagePath);


        return Promise.resolve(resizedImageName);
    }
    catch (e) {
        return Promise.reject(e);
    }
}



module.exports = {
    resize
}