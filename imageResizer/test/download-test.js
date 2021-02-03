const assert = require('assert');
const downloader = require('../src/downloader');
const config = require('../config');
const paramHelper = require('../src/param-helper');

describe('Test image file download',  ()=> {

    it('should save file in the "tmp" folder', async function(done) {

        this.timeout(30000);

        const params = {url: config.DefaultImageUrl, height: 100, width: 150};
        const fileName = paramHelper.getFileName(params);

        try {
            const downloadedFileName = await downloader.download(params.url, fileName)
            assert(downloadedFileName.length > 0);
        }
        catch (e) {
            assert.throws(e);
        }
    });

});
