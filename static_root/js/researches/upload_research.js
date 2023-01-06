/*
	By Osvaldas Valutis, www.osvaldas.info
	Available for use under the MIT License
*/
'use strict';

; (function (document, window, index) {
    var inputs = document.querySelectorAll('.inputfile');
    Array.prototype.forEach.call(inputs, function (input) {
        var label = input.nextElementSibling,
            labelVal = label.innerHTML;

        input.addEventListener('change', function (e) {
            var fileName = '';
            if (this.files && this.files.length > 1)
                fileName = (this.getAttribute('data-multiple-caption') || '').replace('{count}', this.files.length);
            else
                fileName = e.target.value.split('\\').pop();

            if (fileName)
                document.getElementById('sr').innerHTML = fileName;
            else
                label.innerHTML = labelVal;
        });

        // Firefox bug fix
        input.addEventListener('focus', function () { input.classList.add('has-focus'); });
        input.addEventListener('blur', function () { input.classList.remove('has-focus'); });
    });
}(document, window, 0));



try{
	$('#colleagues_list').hide()
	$('#add_colleagues').css('cursor', 'pointer')
	$('#add_colleagues').click(()=>{
	    $('#colleagues_list').slideToggle()
	})
	var limit = 5;
	$('input[type="checkbox"]').on('change', function(evt) {
	   if($('input[type="checkbox"]:checked').length >= limit) {
	       this.checked = false;
	   }
	});

	document.getElementById("sent").onclick = function (target) {
	    if (document.getElementById("file-7").value) {
		$('.alert').show('fade')
		this.classList.add("file-sent");
	    }
	}
} catch{}

