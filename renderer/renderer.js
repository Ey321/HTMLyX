const katex = require('katex');
function render_katex(){
	var html = katex.renderToString(process.argv[2], {
	    throwOnError: false,
	    output: "html"
	});
	return html;
}
 
console.log(render_katex());
