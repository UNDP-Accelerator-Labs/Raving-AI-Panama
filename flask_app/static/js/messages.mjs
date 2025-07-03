import { d3_extended as d3 } from './d3.extensions.mjs';
import { capitalize } from './helpers.mjs';

export function render(keyword, data, kwargs) {
	const { color } = kwargs || {};

	const messagebox = d3.select('#messages')
	.classed('show', true);

	console.log(color.domain())
	console.log(color.range())

	messagebox.addElems('h1')
	.html(capitalize(keyword))

	const messages = messagebox.addElems('section', 'message', data)
	messages.addElems('div', 'text')
	.addElems('p', null, d => d.message.split(/\n+/g))
	.html(d => d);
	messages.addElems('div', 'chips')
	.addElems('div', 'chip', d => d.keywords)
	.style('background-color', d => {
		const c = d3.color(color(d.tree.split('.')[0]));
		return `rgba(${c.r}, ${c.g}, ${c.b}, .5)`;
	})
	.html(d => capitalize(d.keyword));
}