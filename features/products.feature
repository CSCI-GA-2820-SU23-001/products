Feature: The products service back-end
    As a Product Store owner
    I need a RESTful catalog service
    So that I can manage my products

    Background:
        Given the following products
            | name            | price | description      | category         | stock | create_date | available | likes |
            | Snickers        | 50    | Chocolate        | Food             | 20    | 2023-05-12  | true      | 50    |
            | Axe Body Spray  | 10    | Deodorant        | Personal Hygiene | 50    | 2023-08-02  | true      | 25    |
            | A2 Milk         | 5     | Milk             | Food             | 100   | 2023-06-21  | true      | 65    |
            | IKEA Floor Lamp | 45    | Floor lamp       | Home Furniture   | 70    | 2020-11-26  | true      | 250   |
            | Normal Rice     | 15    | Short grain rice | Food             | 100   | 2021-07-20  | true      | 80    |
            | Whole Milk      | 10    | Whole Milk       | Food             | 0     | 2023-08-04  | false     | 10    |
            | Basmati Rice    | 20    | Rice             | Food             | 0     | 2022-01-11  | false     | 100   |
            | PS5             | 500   | PlayStation 5    | Electronics      | 0     | 2021-08-30  | false     | 1000  |


    Scenario: The server is running
        When I visit the "home page"
        Then I should see "Products Demo RESTful Service" in the title
        And I should not see "404 Not Found"

    Scenario: List all Products
        When I visit the "home page"
        And I press the "Search" button
        Then I should see the message "Success"
        And I should see "Snickers" in the results
        And I should see "PS5" in the results
        And I should not see "Xbox" in the results

    Scenario: Create a Product
        When I visit the "home page"
        And I set the "Name" to "MacBook Pro"
        And I set the "Price" to "2200"
        And I set the "Category" to "Device"
        And I set the "Desc" to "Excellent Laptop"
        And I select "True" in the "Available" dropdown
        And I set the "Likes" to "8"
        And I set the "Stock" to "44"
        And I set the "Create Date" to "10-08-2023"
        And I press the "Create" button
        Then I should see the message "Success"
        When I copy the "Id" field
        And I press the "Clear" button
        Then the "Id" field should be empty
        And the "Name" field should be empty
        And the "Price" field should be empty
        And the "Category" field should be empty
        And the "Desc" field should be empty
        And the "Available" field should be empty
        And the "Likes" field should be empty
        And the "Stock" field should be empty
        And the "Create Date" field should be empty
        When I paste the "Id" field
        And I press the "Retrieve" button
        Then I should see the message "Success"
        And I should see "MacBook Pro" in the "Name" field
        And I should see "8" in the "Likes" field
        And I should see "Device" in the "Category" field
        And I should see "True" in the "Available" dropdown
        And I should see "2023-10-08" in the "Create Date" field

    Scenario: Retrieve a Product
        When I visit the "home page"
        And I set the "Name" to "Watermelon"
        And I set the "Price" to "10"
        And I set the "Category" to "Fruit"
        And I set the "Desc" to "Juicy Fruit"
        And I select "True" in the "Available" dropdown
        And I set the "Likes" to "4"
        And I set the "Stock" to "100"
        And I set the "Create Date" to "06-08-2023"
        And I press the "Create" button
        Then I should see the message "Success"
        When I copy the "Id" field
        And I press the "Clear" button
        Then the "Id" field should be empty
        And the "Name" field should be empty
        And the "Category" field should be empty
        When I paste the "Id" field
        And I press the "Retrieve" button
        Then I should see the message "Success"
        And I should see "Watermelon" in the "Name" field
        And I should see "4" in the "Likes" field
        And I should see "Fruit" in the "Category" field
        And I should see "True" in the "Available" dropdown
        And I should see "2023-06-08" in the "Create_date" field

    Scenario: Delete a Product
        # When I visit the "home page"
        # And I press the "Search" button
        # Then I should see the message "Success"
        # And I should see "Snickers" in the results
        # When I set the "ID" to "26"
        # And I press the "Delete" button
        # Then I should see the message "Product has been Deleted!"
        # When I press the "Clear" button
        # And I press the "Search" button
        # Then I should see the message "Success"
        # # And I should not see "Snickers" in the results
        # Then I should not see "26" in the "ID" field
        When I visit the "home page"
        And I set the "Name" to "Watermelon"
        And I set the "Price" to "10"
        And I set the "Category" to "Fruit"
        And I set the "Desc" to "Juicy Fruit"
        And I select "True" in the "Available" dropdown
        And I set the "Likes" to "4"
        And I set the "Stock" to "100"
        And I set the "Create Date" to "06-08-2023"
        And I press the "Create" button
        Then I should see the message "Success"
        When I copy the "Id" field
        And I press the "Clear" button
        Then the "Id" field should be empty
        And the "Name" field should be empty
        And the "Category" field should be empty
        When I paste the "Id" field
        And I press the "Delete" button
        Then I should see the message "Product has been Deleted!"

