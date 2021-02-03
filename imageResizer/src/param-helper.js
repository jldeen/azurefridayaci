const md5 = require('md5');
const config = require('../config');

function getFileName(params){
    var urlHash = md5(params.url);

    return urlHash;
}

function getResizedFileName(params){
    var urlHash = md5(params.url);
    var fileName = urlHash + '_' + params.height + '_' + params.width + "." + params.format;

    return fileName;
}

function getParams(req){

    /*
     * Get values from URL Params
     */
    let url = req.query.url;
    let width = req.query.w ? req.query.w : req.query.width;
    let height = req.query.h ? req.query.h : req.query.height;
    let format = req.query.f ? req.query.f : req.query.format;
    let fit = (req.query.fit ? req.query.fit : config.DefaultImageFitPolicy).toLowerCase();

    if( !(fit == 'cover' || fit == 'contain') ){
        // Fall back to default
        fit = config.DefaultImageFitPolicy.toLocaleString();
    }

    try{
        width = parseInt(width);
    }
    catch{
        width = config.DefaultWidth;
    }

    try{
        height = parseInt(height);
    }
    catch  {
        height = config.DefaultHeight;
    }

    if(format === undefined){
        format = "png";
    }
    else{
        format = format.toLowerCase();

        // check if its one of the supported format
        if( format === "png" ||
            format === "jpeg" ||
            format === "jpg" ||
            format === "webp" ||
            format === "tiff"
        )
        {
            // OK, its one of the supported format
        }
        else {
            format = config.DefaultOutputImageFormat;
        }
    }

    /*
     * Set default settings as needed
     */
    if(url === undefined){
        url = config.DefaultImageUrl;
    }

    if(width === undefined || isNaN(width)){
        width = config.DefaultWidth;
    }

    if(height === undefined || isNaN(height)){
        height = config.DefaultHeight;
    }

    return {
        height : height,
        width: width,
        url : url,
        format : format,
        fit : fit
    }
}


module.exports = {
    getFileName, getParams , getResizedFileName
}