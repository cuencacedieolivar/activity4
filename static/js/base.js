document.querySelector('.hamburger').addEventListener('click', function() {
    const links = document.querySelector('.navbar-links');
    links.classList.toggle('active');
});


document.querySelectorAll('.add-to-cart-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        });

        if (response.ok) {
            const countElement = document.querySelector('.cart-count');
            countElement.textContent = parseInt(countElement.textContent) + 1;
            alert("Added to cart!");
        }
    });
});