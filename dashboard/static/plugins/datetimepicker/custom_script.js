function initDateTimeChooser(id, opts) {
	$('#' + id).datetimepicker($.extend({
		format: 'Y-m-d - H:i',
		//onGenerate: hideCurrent
	}, opts || {}));
}