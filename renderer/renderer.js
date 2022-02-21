const katex = require('katex');
const readline = require('readline')

var rl = readline.createInterface({
	input: process.stdin,
	output: process.stdout,
	terminal: false
});


rl.on('line', function(line){
	const data = JSON.parse(line);

	const html = katex.renderToString(data.equation, {
		throwOnError: false,
		output: "html",
		displayMode: data.is_display
	});
	const obj = new Object();
	obj.html = html;
	console.log(JSON.stringify(obj));
})