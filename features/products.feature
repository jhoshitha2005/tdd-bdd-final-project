Feature: The product store service back-end
  As a Product Store Owner
  I need a RESTful catalog service
  So that I can keep track of all my products

Background:
  Given the following products
      | name       | description     | price   | available | category   |
      | Hat        | A red fedora    | 59.95   | True      | CLOTHS     |
      | Shoes      | Blue shoes      | 120.50  | False     | CLOTHS     |
      | Big Mac    | 1/4 lb burger   | 5.99    | True      | FOOD       |
      | Sheets     | Full bed sheets | 87.00   | True      | HOUSEWARES |

Scenario: The server is running
  When I visit the "Home Page"
  Then I should see "Product Catalog Administration" in the title
  And I should not see "404 Not Found"

Scenario: Create a Product
  When I visit the "Home Page"
  And I set the "Name" to "Hammer"
  And I set the "Description" to "Claw hammer"
  And I select "True" in the "Available" dropdown
  And I select "Tools" in the "Category" dropdown
  And I set the "Price" to "34.95"
  And I press the "Create" button
  Then I should see the message "Success"

Scenario: Read a Product
  Given a product exists with the name "Hammer"
  When I request the product details for "Hammer"
  Then I should see the description "Claw hammer"
  And I should see the price "34.95"
  And I should see "True" as available
  And I should see "Tools" as the category

Scenario: Update a Product
  Given a product exists with the name "Hammer"
  When I update the "Price" to "39.95" for product "Hammer"
  Then I should see the message "Success"
  And the product "Hammer" price should be "39.95"

Scenario: Delete a Product
  Given a product exists with the name "Hammer"
  When I delete the product "Hammer"
  Then I should see the message "Deleted successfully"
  And the product "Hammer" should no longer exist

Scenario: List All Products
  When I request the list of all products
  Then I should see at least the products "Hat", "Shoes", "Big Mac", and "Sheets"

Scenario: Search Products by Category
  When I search products by category "CLOTHS"
  Then I should see the products "Hat" and "Shoes"
  And I should not see the product "Big Mac"

Scenario: Search Products by Availability
  When I search products by availability "True"
  Then I should see the products "Hat", "Big Mac", and "Sheets"
  And I should not see the product "Shoes"

Scenario: Search Products by Name
  When I search for a product by name "Big Mac"
  Then I should see the product "Big Mac"
  And I should not see the product "Hat"

