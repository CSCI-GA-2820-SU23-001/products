Feature: The products service back-end
            As a Ecommerce manager
            I need a RESTful products service
            So that I can keep track of all my products
Background:
            
            Given the server is started
            # Uncomment below after adding products to database
            # Given the following products
                | name      | price    | category  | stock | create_date | available | likes |
                | fido      | 300      | dog       | 1     | 2019-11-18  | True      | 11    |
                | kitty     | 350      | cat       | 2     | 2020-08-13  | true      | 22    |
                | leo       | 400      | lion      | 0     | 2021-04-01  | False     | 33    |
                | sammy     | 250      | snake     | 3     | 2018-06-04  | True      | 44    |       
            

Scenario: The server is running
            When I visit the "home page"
            Then  I should not see "404 Not Found"
            # Uncomment below after implementing UI
            # Then I should see "Product Demo REST API Service"
            # And  I should not see "404 Not Found"