document.addEventListener('DOMContentLoaded', function() {
    const switches = document.querySelectorAll('input[type="checkbox"]');

    switches.forEach(function(switchEl) {
        switchEl.addEventListener('change', function() {
            console.log(`Switch ${switchEl.id} is now ${switchEl.checked ? 'ON' : 'OFF'}`);

        });
    });
});