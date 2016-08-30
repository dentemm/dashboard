function initDateChooser(id, opts) {
	$('#' + id).datetimepicker($.extend({
		timepicker: false,
		scrollInput: false,
		format: 'Y-m-d',
		//onGenerate: hideCurrent
	}, opts || {}));
}

function initDateTimeChooser(id, opts) {
	$('#' + id).datetimepicker($.extend({
		format: 'Y-m-d H:i',
		//onGenerate: hideCurrent
	}, opts || {}));
}