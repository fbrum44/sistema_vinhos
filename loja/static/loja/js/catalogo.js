document.addEventListener('DOMContentLoaded', function () {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const form = document.getElementById('filtro-form');

    checkboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            form.submit();
        });
    });
});
