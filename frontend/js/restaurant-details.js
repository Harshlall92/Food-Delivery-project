const path = window.location.pathname;
const restaurantId = path.split("/").pop();

async function fetchRestaurant(restaurantId) {
    const restaurantDetailsContainer = document.getElementById('restaurant-details');


    try {
        const response = await fetch(`/api/restaurants/${restaurantId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const restaurant = await response.json();
        
        restaurantDetailsContainer.innerHTML = ``

        const restaurantName = document.createElement("h2");
        restaurantName.textContent = restaurant.name;
        restaurantDetailsContainer.appendChild(restaurantName);

        const restaurantDetails = document.createElement("p");
        restaurantDetails.textContent = `${restaurant.address} | ${restaurant.cuisine}`;
        restaurantDetailsContainer.appendChild(restaurantDetails);

        const menuItemsContainer = document.createElement("div");
        menuItemsContainer.id = "menu-items-container";
        restaurantDetailsContainer.appendChild(menuItemsContainer);

        for (const menuItem of restaurant.menu_items) {
            const menuItemCard = document.createElement("div");
            menuItemCard.className = "menu-item-card";

            const menuItemName = document.createElement("h4");
            menuItemName.textContent = menuItem.name;
            menuItemCard.appendChild(menuItemName);

            const menuItemDetails = document.createElement("div");
            menuItemDetails.className = "menu-item-details";
            menuItemCard.appendChild(menuItemDetails);

            const menuItemDescription = document.createElement("p");
            menuItemDescription.textContent = menuItem.description;
            menuItemDetails.appendChild(menuItemDescription);

            const menuItemPrice = document.createElement("p");
            menuItemPrice.textContent = `Price: $${menuItem.price.toFixed(2)}`;
            menuItemDetails.appendChild(menuItemPrice);

            menuItemsContainer.appendChild(menuItemCard);
        }

    } catch (error) {
        console.error('Error fetching restaurant details:', error);
        restaurantDetailsContainer.innerHTML = "<p>Failed to load restaurant details. Please try again later.</p>";
    }
}

document.addEventListener('DOMContentLoaded', fetchRestaurant(restaurantId));