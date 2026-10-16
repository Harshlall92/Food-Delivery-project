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

        }
    } catch (error) {
        console.error('Error creating restaurant:', error);
    }
});