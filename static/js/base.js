document.querySelector('.hamburger').addEventListener('click', function() {
    const links = document.querySelector('.navbar-links');
    links.classList.toggle('active');
});


 document.addEventListener('DOMContentLoaded', function () {
    flatpickr("#id_last_watered", {
      dateFormat: "Y-m-d",
    });
    flatpickr("#id_next_watering", {
      dateFormat: "Y-m-d",
    });
  });