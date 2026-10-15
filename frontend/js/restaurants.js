async function fetchAllRestaurants() {
    const restaurantContainer = document.getElementById('restaurant-list');

    try {
        const response = await fetch("/api/restaurants");

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);

        }
        const restaurants = await response.json();

        if (restaurants.length === 0) {
            restaurantContainer.innerHTML = "<p>No restaurants available at the moment.</p>";
            return;
        }

        restaurantContainer.innerHTML = '';

        for (const restaurant of restaurants) {
            const restaurantCard = document.createElement("button");
            restaurantCard.className = "restaurant-card";
            restaurantCard.type = "button";

            const restaurantName = document.createElement("h4");
            restaurantName.textContent = restaurant.name;

            restaurantCard.appendChild(restaurantName);

            const restaurantDescription = document.createElement("p");
            restaurantDescription.textContent = restaurant.cuisine + " | " + restaurant.address

            restaurantCard.appendChild(restaurantDescription);

            restaurantCard.addEventListener("click", () => {
                window.location.href = `/restaurants/${restaurant.id}`;
            });

            restaurantContainer.appendChild(restaurantCard);
        }

    }
    catch (error) {
        console.error("Error fetching restaurants:", error);
        restaurantContainer.innerHTML = "<p>Failed to load restaurants. Please try again later.</p>";
    }
}

document.addEventListener('DOMContentLoaded', fetchAllRestaurants);