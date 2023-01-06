
// for(let i=1;i <= document.querySelectorAll("tr").length;i++){
// 	if((i%2) != 1){
// 		document.querySelectorAll("tr")[i-1].className += ' bkg';
// 	}
// }

function span_clicked(trgt){
	num = trgt.id.slice(-1)
	rst = trgt.id.slice(0, -6)
	i = -1
	while (!isNaN(Number(trgt.id.slice(i)))) {
		num = trgt.id.slice(i)
		rst = trgt.id.slice(0, i-5)
		i -= 1;
	}        
	document.getElementById(`${rst}${num}`).click();
}
var submitted = false;
document.getElementById('correcting_form').onsubmit = () => {
	submitted = true;
}
window.addEventListener('onbeforeunload', function (e) {
	var e = e || window.event;
	var element = document.activeElement;
		//IE & Firefox
		if (e) {
			e.returnValue = null;
		}
		// For Safari
		return null;
});

function num_changed(e){
	const [t, num] = e.target.name.split("_"),
		   evaluation_values = [
			   Number(document.querySelector(`[name="references_${num}"][type="number"]`).value), 
			   Number(document.querySelector(`[name="conclusions_${num}"][type="number"]`).value),
			   Number(document.querySelector(`[name="content_${num}"][type="number"]`).value), 
			   Number(document.querySelector(`[name="axes_${num}"][type="number"]`).value), 
			   Number(document.querySelector(`[name="intro_${num}"][type="number"]`).value)],
			total = evaluation_values.reduce((last, value)=>last+value);

	$(`#total_${num}`).text(total)
	$(`#pon_${num}`).text((total>=50) ? "مستوفي" : "غير مستوفي")
	$(`#pon_${num}`).attr("class", (total>=50) ? "passed" : "not-passed")

}

$.each($('input[type="number"]'), (i, v)=>{v.oninput=num_changed})


