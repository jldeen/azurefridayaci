const assert = require('assert');
const downloader = require('../src/downloader');
const config = require('../config');
const paramHelper = require('../src/param-helper');
const resizer = require('../src/resizer');


describe('Test image file download and resize', function() {

    it('should save downloaded file and resized file in the "tmp" folder', async function() {

        this.timeout(30000);

        const params = {url: config.DefaultImageUrl, height: 100, width: 150, format : 'webp'};

        const fileName = paramHelper.getFileName(params);

        const downloadedFileName = await downloader.download(params.url, fileName);

        const downloadedFilePath = "./images/originals/" + downloadedFileName;

        const resizedFileName = await resizer.resize(downloadedFilePath, params);
        assert(resizedFileName.length > 0);

    });

});
