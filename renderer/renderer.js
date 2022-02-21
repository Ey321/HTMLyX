const katex = require('katex');
function render_katex(){
	var html = katex.renderToString(process.argv[2], {
	    throwOnError: false,
	    output: "html",
	    displayMode: (process.argv[3]=="True")
	});
	return html;
}
 
console.log(render_katex());
