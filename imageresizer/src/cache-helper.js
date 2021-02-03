const fs = require("fs");
const util = require('util');
const config = require('../config');

const getFileStatus = util.promisify(fs.stat);
const deleteFile = util.promisify(fs.unlink);
const getFiles = util.promisify(fs.readdir);

const MaxDeleteItemsAtATime = 500;
const folderPath = './tmp/';


async function runCacheCleanupTask(){

    const files = await getFiles(folderPath);
    let counter = 0;

    for (var file of files) {

        if (file == ".gitkeep"){
            continue;
        }

        let stat = await getFileStatus( folderPath + file);

        let hoursSinceLastModified = (new Date().getTime() - stat.mtime) / 1000 / 60 / 60;

        if (hoursSinceLastModified > config.CacheDuration) {

            // Cached image too old. Delete from cache folder

            await deleteFile(file);

            counter++;
        }

        if (counter > MaxDeleteItemsAtATime) {

            // We have deleted many files.
            // Lets take a break and let others do some work
            break;
        }
    }

    return Promise.resolve(counter);
}


module.exports = {
    runCacheCleanupTask
}