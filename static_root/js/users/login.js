document.getElementById('national_id').oninvalid = e => {
    e.target.setCustomValidity('خطأ في الرقم القومي')
}
document.getElementById('national_id').onchange = e => {
    try { e.target.setCustomValidity('') } catch (e) { }
}