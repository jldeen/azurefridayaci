const restify = require('restify');
const httpHandler = require('./http-handler');
const cacheHelper = require('./cache-helper');


// Initialize server
const server = restify.createServer();


// Enable plugins
server.use(restify.plugins.queryParser());


// Register handlers
server.get('/resize/', httpHandler.resizeImage);
server.get('/resize', httpHandler.resizeImage);
server.get('/', httpHandler.landingPage);


// Start server
server.listen(80, function() {
  console.log('%s listening at %s', server.name, server.url);
});


// Run Cache cleanup task in the background (every 10 minutes)
setInterval(async function(){
  try {
    await cacheHelper.runCacheCleanupTask();
  }
  catch (e) {
    //TODO: Log error
  }
}, 1000 * 60 * 10);
