function getBaseLog(x, y) {
	return Math.log(y) / Math.log(x);
}

$(document).ready(function() {

	var styleCache = {};
	var styleFunction1 = function(feature) {
		var total = feature.get('TotalCases');

		if (feature.getId() == "TOTAL") {
			total = 1;
		}
		var radius = Math.pow(getBaseLog(10, total), 2);
		var style = styleCache[radius];
		if (!style) {
			style = new ol.style.Style({
				image : new ol.style.Circle({
					radius : radius,
					fill : new ol.style.Fill({
						color : 'rgb(237, 107, 117, 0.3)'
					}),
					stroke : new ol.style.Stroke({
						color : 'rgb(255, 0, 0, 0.9)',
						width : 1
					})
				})
				/*text : new ol.style.Text({
					text:feature.get('bnName'),
					font : '11px Calibri,sans-serif',
					fill : new ol.style.Fill({
						color : '#000'
					}),
					stroke : new ol.style.Stroke({
						color : '#fff',
						width : 1
					})
				})*/
			});
			styleCache[radius] = style;
		}
		return style;
	};

	
	var bubbleSource = new ol.source.Vector({
		url : "api/points",
		format : new ol.format.GeoJSON()
	});

	var bubbleLayer = new ol.layer.Vector({
		source : bubbleSource,
		name : "bubble",
		title : "পৃথিবীর  বৃত্ত ভিত্তিক মানচিত্র ",
		type : 'children',
		style : styleFunction1
	});

	map.addLayer(bubbleLayer)
	console.log("layer size: "+ map.getLayers().getLength());
	populateTableData(bubbleLayer);
	
	var bListenerKey=bubbleSource.on('change', function(e) {
	    if (bubbleSource.getState() == 'ready') {
	        ol.Observable.unByKey(bListenerKey);
	        console.log('bubbleLayer is loaded');
	        populateTableData(bubbleLayer);
	    }
	});
	 
})