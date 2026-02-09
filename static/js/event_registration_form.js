document.addEventListener("DOMContentLoaded", function() {

    const form = document.querySelector('.event-form');
    const submitBtn = document.querySelector('.btn-submit');

    function checkFormValidity() {
        if (form.checkValidity()) {
            submitBtn.removeAttribute('disabled');
        } else {
            submitBtn.setAttribute('disabled', 'true');
        }
    }

    form.addEventListener('input', checkFormValidity);
    form.addEventListener('change', checkFormValidity);
});
