const form = document.getElementById('update-restaurant-form');
const result = document.getElementById('result');
const detailsUrl = `/restaurants/${restaurantId}`;
let original = {};
document.getElementById('cancel-link').href = detailsUrl;


async function loadRestaurant() {
    try{
        const response = await fetch(`/api/restaurants/${restaurantId}`);
        if(!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const restaurant = await response.json();
        original = {
            name: restaurant.name,
            address: restaurant.address,
            cuisine: restaurant.cuisine
        };
        for (const [field, value] of Object.entries(original)){
            form.elements[field].value = value;
        }
    } catch (error) {
        console.error('Error loading to the restaurant')
    }
}

form.addEventListener('submit', async function (event) {
    event.preventDefault();
    const current = Object.fromEntries(new FormData(form).entries());
    const changes = {};
    for( const field of Object.keys(original)){
        if(current[field] != original[field]){
            changes[field] = current[field]
        }
    }
    if( Object.keys(changes).length == 0) {
        result.textContent = "No changes to save"
        return;
    }
    try{
        const response = await fetch(`/api/restaurants/${restaurantId}`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(changes)
        });
        if (response.ok){
            window.location.href = detailsUrl;
        } 
    } catch (error){
        console.error('Error updating restaurant details:', error);

    }
});

loadRestaurant();