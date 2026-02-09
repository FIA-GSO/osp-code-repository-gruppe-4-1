document.addEventListener("DOMContentLoaded", function() {

    const form = document.querySelector('.event-form');
    const submitBtn = document.querySelector('.btn-submit');
    const first = document.querySelector('[name="first_day"][value="no"]');
    const second = document.querySelector('[name="second_day"][value="no"]');

    function checkFormValidity() {
        if (form.checkValidity() && !(first.checked && second.checked)) {
            submitBtn.removeAttribute('disabled');
        } else {
            submitBtn.setAttribute('disabled', 'true');
        }
    }

    form.addEventListener('input', checkFormValidity);
    form.addEventListener('change', checkFormValidity);
});
