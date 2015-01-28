$(document).ready(function () {
	$("#render.OfxImageEffectContextGenerator").click(function(){
		var pluginId = $(this)[0].getAttribute("pluginId");
		console.log('internet');
		$.ajax({
			type: "POST",
			url: "/render/",
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify({
				nodes: [{
					id: 0,
					plugin: pluginId
				},{
					id: 1,
					plugin: "tuttle.jpegwriter"
				}],
				connections: [{
						src : 0,
						dst: 1
				}],
				renderNode: 1
			})
		}).done(function(data){
			$("#viewer img").attr("src", data.resources[0]).fadeIn();
		})
	});


	// $("#render.OfxImageEffectContextGenerator").click(function(){
	// 	var pluginId = $(this)[0].getAttribute("pluginId");
	// 	$.ajax({
	// 		type: "POST",
	// 		url: "/render/",
	// 		contentType: 'application/json; charset=utf-8',
	// 		data: JSON.stringify({
	// 			nodes: [{
	// 				id: 0,
	// 				plugin: pluginId
	// 			},{
	// 				id: 1,
	// 				plugin: "tuttle.jpegwriter"
	// 			}],
	// 			connections: [{
	// 					src : 0,
	// 					dst: 1
	// 			}],
	// 			renderNode: 1
	// 		})
	// 	}).done(function(data){
	// 		$("#viewer img").attr("src", data.resources[0]).fadeIn();
	// 	})
	// });

});