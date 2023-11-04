const fs = require('fs')

const YAPLParser = require('./yaplparser');

// Make sure we got a filename on the command line.
if (process.argv.length < 3) {
    console.log('Usage: node ' + process.argv[1] + ' FILENAME');
    process.exit(1);
}

// Read the file and print its contents.
var filename = process.argv[2];
fs.readFile(filename, 'utf8', function(err, data) {
    if (err) throw err;
    let unparsed = String(data)
    // console.log('filename: ' + filename);
    // console.log('contents: ' + unparsed);
    // TODO: fix locations in parsed output, based on this preprocessing step.
    // I haven't gotten the Syntax to jive with empty lines, so I'm just filtering them out here.
    unparsed = unparsed.replace(/\n( )*\n/g, "\n") + "\n@@EOF@@"
    // console.log('filtered: ' + unparsed);
    try {
        let parsed = YAPLParser.parse(unparsed);
        console.log('parsed: ' + JSON.stringify(parsed));
    } catch (error) {
        console.log('error: ' + String(error));
    }
});
