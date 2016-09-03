// MATCHHEIGHT: Init
  	$(function() {
  		$.fn.matchHeight._maintainScroll = true;
    	$('.equal-height').matchHeight();
  	});
// FULLCALENDAR: Init
		$(function() { // dom ready
      $('#calendar').fullCalendar({
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
        resourceAreaWidth: 140,
        defaultDate: '2016-08-08',
        defaultDate: moment().startOf('day'),	// Today in Moment.js
        editable: true,
        //aspectRatio: 4.35,
        contentHeight: 30 * {{ page.task_count_distinct_owner }} + 28,  /* aantal resources bepaalt hoogte van kalender */
        eventOverlap: false,
        //scrollTime: '00:00',
        minTime: '05:00',
        maxTime: '23:00',
        header: {
          left: 'promptResource today prev,next',
          //left: null,
          center: 'title',
          //right: 'timelineDay,timelineThreeDays,timelineTenDays,month',
          //right: null 
          right: 'timelineDay,timelineWW,timeline2WW'
        },
        customButtons: {
        },
        defaultView: 'timelineDay',
        views: {
          timelineDay: {
            buttonText: 'Today',
            slotDuration: '01:00',
            duration: {days: 7 }
          },
          timelineWW: {
            type: 'timeline',
            slotDuration: '04:00',
            duration: { days: 7 }
          },
          timeline2WW: {
            type: 'timeline',
            slotDuration: '08:00',
            duration: { days: 14 }
          }
        },
        resourceLabelText: 'Owner',
        resources: "{% url 'event-resources' event_id=page.pk %}",
        events: "{% url 'event-events' event_id=page.pk %}",
        //eventClick: function(event) {
        	/* This callback gets executed when an event is being clicked by a user */

          //$('#calendartaskmodal').modal();
 
       // },
        eventAfterRender: function(event, element, view) {
        	/* This callback get executed when an event is added to the calendar */

        	// Add Bootstrap modal data attributes
        	$(element).attr('data-taskid', event.id);
        	$(element).attr('data-target', '#calendartaskmodal');
        	$(element).attr('data-toggle', 'modal');
        }
      });
    });
// Fetch data for task modal through ajax call
	$(function() {
		$('#calendartaskmodal').on('show.bs.modal', function(e){

			//console.log(e.relatedTarget);
			var id = $(e.relatedTarget).data("taskid");

			$.ajax({
				url:"/tasks/update/" + id,	// Impossible to solve through {- url -} template tag?
				//url: "{- url 'update-task-modal' pk=page.page.page -}",
				type: "GET",
				success: task_handler,

				error: function(xhr, ajaxOptions, thrownError) {
					console.log(xhr.status);
					alert(thrownError);
				}
			});
			function task_handler(data) {
				console.log('success');
				$('#calendartaskmodal').html(data);
			};
		})
	})
// Add task modal
	$(function() {
		$('#addtaskmodal').on('show.bs.modal', function(e){

			var id = $(e.relatedTarget).data("eventid");

			console.log(id);

			$.ajax({
				url: "{% url 'add-task-for-event' event_id=page.pk %}",
				type: "GET",
				success: task_handler,

				error: function(xhr, ajaxOptions, thrownError) {
					console.log(xhr.status);
					alert(thrownError);
				}
			});
			function task_handler(data) {
				console.log('success');
				$('#addtaskmodal').html(data);
			};
		})
	})
// DRAGULA: Init
	$(function() {
	    options = {
	      revertOnSpill: true
	    }
	  	// initieer Dragula 
	  	drake = dragula([todo, inprogress, done], options);
	  	// Use jQuery matchHeight om kolommen van dezelfde hoogte te verzekeren na elk drop event
	  	drake.on('drop', function(el, target, source, sibling) {
	  		$('.equal-height').matchHeight();
	  		//console.log('drop');
	  	});
	  	drake.on('dragend', function(el, target, source, sibling) {
	  		//console.log('drag end');
	  	});
	})
