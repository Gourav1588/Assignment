# Pizza Delivery Pipeline - README

## What this DAG does
Models a pizza order going from "order taken" to "delivered" for DoughFlow Pizza Co.
7 tasks: take_order -> check_ingredient_stock -> branch_topping_check -> add_toppings -> bake_pizza -> quality_check -> dispatch_delivery

## Why this flow
I kept it close to how a real kitchen would work - order comes in, check if you have the toppings, then either add them or skip straight to baking if something's out of stock. Baking, quality check and delivery happen no matter what, since the pizza still needs to go out even without the extra topping.

## XCom usage
take_order pushes order_id and toppings list. These get pulled by check_ingredient_stock, add_toppings and quality_check later on, so the order info doesn't have to be looked up again in every task.

## Skip logic
check_ingredient_stock checks if mozzarella is in stock (hardcoded as out of stock for this run). branch_topping_check reads that result and either routes to add_toppings or skips it and goes straight to bake_pizza. Used BranchPythonOperator for this, and bake_pizza has trigger_rule=none_failed_min_one_success so it still runs even when one of its upstream tasks was skipped.

## Schedule
30 11,18 * * * - runs at 11:30am and 6:30pm every day, matching lunch and dinner rush instead of just @daily.

## API trigger
Triggered a run using POST /api/v1/dags/pizza_delivery_pipeline/dagRuns from Postman with Basic Auth. Screenshot of request + response attached.
