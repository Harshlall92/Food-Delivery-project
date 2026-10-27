# Software Engineering Project - Milestone 2

Meeting Date: 2026-10-26

All members were present for this meeting.

## Topics

### Users

Caching: Possibility of caching user emails for faster lookup. Revisit next week for discussion.

#### Roles

- Customer
- Restaurant Owner
- System Admin (maybe)

Each role is defined as a literal in the user model.

#### Attributes

- id (str): generated through uuid7
- Email (str)
- Password (str)
- Role (literal): 'Customer', 'Restaurant Owner', 'System Admin'

Password gets encrypted using one-way Hashing.

Further discussion is required for session management and authentication.

### Orders

Orders are only created after the customer has checked out.
Customers do not have any payment options in this milestone, but a frontend page should be developed for checkout.

#### Attributes

- id (str): generated through uuid7
- customerId(str): must exist in user db
- restaruantId(str): must exist in restaurant db
- totalAmount (float): 
- orderDate
- status (literal): 'Recieved', 'In Progress', 'Out for Delivery', 'Completed'

Possibility of adding 'Cancelled'? Could be a Milestone 3 concern. Could also just define now.

### OrderItem

Order items are defined in thier own model similiar to how Restaurants and Menu Items are persisted.

#### Attributes

- id (str): generated through uuid7
- orderId (str): must exist in orders db
- menuItemId (str): must exist in menu items db
- quantity (int): > 0
- pricePerItem (float): positive

---

### Carts

Carts can only be created for an active restaurant

Carts should be persisted.

Cart id should be saved in the session for the customer.

#### Attributes

- id: (str): generated through uuid7
- customerId (str): must exist in user db
- restaurantId(str): must exist in restaurant db
- items (nested list)

#### CartItems

Each cart item is defined in its own model, however the relationship is not clearly defined by Pydantic. The cart items are nested within the cart model.

- menuItemId (str): must exist in menu items db
- quantity (int): > 0
- pricePerItem (float): positive

### Updates to Existing Components

- Possible frontend migration to React

- Error Handling Service?
  - Is already caught by the API Route
  - Could be a separate service to raise the errors and log them to a file?
