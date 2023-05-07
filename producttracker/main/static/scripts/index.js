"use strict";
function update_site_location(target) {
    location.href = target;
}
;
document.addEventListener("DOMContentLoaded", function () {
    const menu_btn = document.getElementById('menuButton');
    menu_btn.addEventListener('change', function () {
        (menu_btn.checked) ? (document.querySelector('.the-bass').classList.add('dropped')) : (document.querySelector('.the-bass').classList.remove('dropped'));
    });
});
