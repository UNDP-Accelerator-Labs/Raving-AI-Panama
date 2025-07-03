import { d3_extended as d3 } from './d3.extensions.mjs';
import * as messages from './messages.mjs';
import { capitalize } from './helpers.mjs';

export function render(data) {
	// Treemap design inspired by https://observablehq.com/@d3/treemap/2
	const canvas = d3.select('#canvas');

	const { clientWidth: cw, clientHeight: ch, offsetWidth: ow, offsetHeight: oh } = canvas.node()
	const width = cw ?? ow ?? 1000
	const height = ch ?? oh ?? 500

	const root = d3.treemap()
	.size([width, height])
	.tile(d3.treemapBinary)
	.padding(1)
	.round(true);

	const hierarchy = d3.hierarchy(data)
	.sum(d => d.value)
	.sort((a, b) => b.value - a.value || b.avg_sentiment - a.avg_sentiment);

	const color = d3.scaleOrdinal(data.children.map(d => d.id), d3.schemeTableau10);
	const saturation = d3.scaleLinear([-1, 1], [.25, 1])

	const svg = canvas.addElem('svg')
	.attr('viewBox', [0, 0, width, height])
	.attr('width', width)
	.attr('height', height);

	const leaf = svg.addElems('g', 'leaf', root(hierarchy).leaves())
	.attr('transform', d => `translate(${[ d.x0, d.y0 ]})`)
	.on('mouseover', function (evt, d) {
		d3.select(this).select('rect')
		.style('stroke', _ => {
			const c = d3.color(color(d.parent.data.id)).darker(.25);
			return `rgb(${c.r}, ${c.g}, ${c.b})`;
		});
	}).on('mouseout', function (evt, d) {
		d3.select(this).select('rect')
		.style('stroke', null);
	}).on('click', async (evt, d) => {
		const grievances = await fetch(`/get_grievances/${d.data.id}`)
		.then(res => res.json())
		.catch(err => console.log(err));

		console.log(d.parent)
		console.log(color.domain())
		console.log(color.range())

		messages.render(d.data.name, grievances, { color });
	});

	// Add the rectangles
	const rects = leaf.addElems('rect')
	.attr('id', d => d.data.id)
	.attr('width', d => d.x1 - d.x0)
	.attr('height', d => d.y1 - d.y0)
	.style('fill-opacity', d => saturation(d.data.avg_sentiment))
	.style('fill', d => { 
		while (d.depth > 1) d = d.parent; 
		return color(d.data.id); 
	}).style('stroke-width', 10);

	// Add a clip path so the text and the rect borders do not overflow
	leaf.addElems('clipPath')
	.attr('id', d => d.clipUid = `clip-${d.data.id}`)
	.each(function (d) {
		const clone = d3.select(this).findAncestor('leaf').select('rect').node().cloneNode();
		const rect = d3.select(this).node().appendChild(clone);
		d3.select(rect).attr('id', null);
	});

	// Add the clip path to the rect
	rects.attr('clip-path', d => `url(#${d.clipUid})`)

	// Add text
	const format = d3.format(',d');
	leaf.addElems('text')
	.attr('clip-path', d => `url(#${d.clipUid})`)
	.addElems('tspan', null, d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g).concat(format(d.value)))
	.attr('x', 3)
	.attr('y', (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
	.attr('fill-opacity', (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
	.text(d => capitalize(d));
}