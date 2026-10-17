document.getElementById('create-restaurant-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const form = event.target;

    const formData = new FormData(form);

    const restaurantData = Object.fromEntries(formData.entries());

    try {
        const response = await fetch("/api/restaurants", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(restaurantData)
        });

        if (response.ok){
            const restaurant = await response.json();
            result.textContent = `Restaurant ${restaurant.name} was created`;
            result.className = 'success';
            form.reset();
        }
    } catch (error) {
        console.error('Error creating restaurant:', error);
        result.textContent = `Error creating restaurant`;
    }
});