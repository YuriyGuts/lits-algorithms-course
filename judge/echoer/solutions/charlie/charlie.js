var fs = require('fs');

var input_file = 'echoer.in';
var output_file = 'echoer.out';

var message = fs.readFileSync(input_file, 'utf8');
fs.writeFileSync(output_file, 'Solution: ' + message);
