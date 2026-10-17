const menuItemEditor = document.getElementById('menu-item-editor');
const createMenuItemForm = document.getElementById('create-menu-item-form');
const menuItemResult = document.getElementById('menu-item-result');

async function readError(response) {
    const error = await response.json();
    return Array.isArray(error.detail)
        ? error.detail.map(e => e.msg).join(', ')
        : error.detail;
}

async function refreshMenu() {
    await Promise.all([fetchRestaurant(restaurantId), loadMenuItemEditor()]);
}

function makeField(labelText, type, name, value) {
    const label = document.createElement('label');
    label.textContent = labelText;

    const input = document.createElement('input');
    input.type = type;
    input.name = name;
    input.value = value ?? '';
    if (name === 'name') input.required = true;
    if (name === 'price') {
        input.step = '0.01';
        input.min = '0.01';
        input.required = true;
    }
    label.appendChild(input);
    return label;
}

function buildMenuItemForm(item) {
    const form = document.createElement('form');
    form.className = 'menu-item-edit-form';

    form.appendChild(makeField('Name: ', 'text', 'name', item.name));
    form.appendChild(makeField('Description: ', 'text', 'description', item.description));
    form.appendChild(makeField('Price: ', 'number', 'price', item.price));

    const saveButton = document.createElement('button');
    saveButton.type = 'submit';
    saveButton.textContent = 'Save';
    form.appendChild(saveButton);

    form.addEventListener('submit', async function (event) {
        event.preventDefault();

        const current = Object.fromEntries(new FormData(form).entries());
        current.price = Number(current.price);

        // Only send the fields that changed
        const changes = {};
        for (const field of ['name', 'description', 'price']) {
            if (current[field] !== item[field]) {
                changes[field] = current[field];
            }
        }
        if (Object.keys(changes).length === 0) {
            menuItemResult.textContent = 'No changes to save.';
            return;
        }

        try {
            const response = await fetch(
                `/api/restaurants/${restaurantId}/menu-items/${item.id}`,
                {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(changes)
                }
            );

            if (response.ok) {
                menuItemResult.textContent = `"${current.name}" was updated.`;
                await refreshMenu();
            } else {
                menuItemResult.textContent = `Could not update item: ${await readError(response)}`;
            }
        } catch (error) {
            console.error('Error updating menu item:', error);
            menuItemResult.textContent = 'Could not reach the server. Please try again.';
        }
    });

    return form;
}

async function loadMenuItemEditor() {
    try {
        const response = await fetch(`/api/restaurants/${restaurantId}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const restaurant = await response.json();

        menuItemEditor.innerHTML = '';
        if (restaurant.menu_items.length === 0) {
            menuItemEditor.textContent = 'No menu items yet. Add one below.';
            return;
        }
        for (const item of restaurant.menu_items) {
            menuItemEditor.appendChild(buildMenuItemForm(item));
        }
    } catch (error) {
        console.error('Error loading menu items:', error);
        menuItemEditor.textContent = 'Failed to load menu items.';
    }
}

// Creating a new menu item
createMenuItemForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const data = Object.fromEntries(new FormData(createMenuItemForm).entries());
    data.price = Number(data.price);
    if (!data.description) delete data.description;   // description is optional

    try {
        const response = await fetch(`/api/restaurants/${restaurantId}/menu-items`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            const created = await response.json();
            menuItemResult.textContent = `"${created.name}" was added.`;
            createMenuItemForm.reset();
            await refreshMenu();
        } else {
            menuItemResult.textContent = `Could not add item: ${await readError(response)}`;
        }
    } catch (error) {
        console.error('Error creating menu item:', error);
        menuItemResult.textContent = 'Could not reach the server. Please try again.';
    }
});

loadMenuItemEditor();