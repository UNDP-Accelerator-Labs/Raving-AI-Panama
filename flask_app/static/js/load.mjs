import * as treemap from './treemap.mjs';

async function onLoad() {
	const data = await fetch('/get_clusters', { method: 'GET' })
		.then(res => res.json())
		.catch(err => console.log(err));

	treemap.render(data);
}

if (document.readyState === 'loading') {
	document.addEventListener('DOMContentLoaded', onLoad);
} else {
	await onLoad();
}