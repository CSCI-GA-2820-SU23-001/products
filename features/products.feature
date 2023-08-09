Feature: The products service back-end
    As a Product Store owner
    I need a RESTful catalog service
    So that I can manage my products

Background:
    Given the following products
        | name            | price       | description           | category         | stock | create_date | available | likes |
        | Snickers        | 50          | Chocolate             | Food             | 20    | 2023-05-12  | true      | 50    | 
        | Axe Body Spray  | 10	        | Deodorant	            | Personal Hygiene | 50	   | 2023-08-02  | true      | 25    |
        | A2 Milk	      | 5           | Milk                  | Food	           | 100   | 2023-06-21  | true      | 65    |
        | IKEA Floor Lamp |	45          | Floor lamp            | Home Furniture   | 70    | 2020-11-26  | true      | 250   |
        | Normal Rice     | 15          | Short grain rice      | Food             | 100   | 2021-07-20  | true      | 80    |
        | Whole Milk      | 10          | Whole Milk            | Food             | 0     | 2023-08-04	 | false     | 10    |
        | Basmati Rice    | 20          | Rice                  | Food             | 0     | 2022-01-11  | false     | 100   |
        | PS5             | 500         | PlayStation 5         | Electronics      | 0     | 2021-08-30  | false     | 1000  |
            

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Products Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all Products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "Snickers" in the results
    And I should see "PS5" in the results
    And I should not see "Xbox" in the results