onloads.push(() => {
	const linesElement = document.getElementById("cloc");
	let htmlFormat = "1";

	for(let numberOfLines = 2; numberOfLines <= code.split('\n').length; numberOfLines++)
		htmlFormat += `<br>${numberOfLines}`;

	linesElement.innerHTML = htmlFormat;
});
