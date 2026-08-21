from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
import logging

default_args = {
    'owner': 'gourav',
    'retries': 1,
}

with DAG(
    dag_id='pizza_delivery_pipeline',
    default_args=default_args,
    description='DoughFlow Pizza Co. — order to delivery pipeline',
    schedule_interval='30 11,18 * * *',   # 11:30 (lunch) and 18:30 (dinner) daily
    start_date=datetime(2026, 8, 1),
    catchup=False,                        
    tags=['pizza', 'assignment'],
) as dag:

    
    def take_order_func(**context):
        """Simulates a new order coming in: generates order ID and topping list."""
        order_id = "ORD-1042"
        toppings = ["mozzarella", "pepperoni"]

        log = logging.getLogger("airflow.task")
        log.info(f"New order received: {order_id} with toppings {toppings}")

        # Push data to XCom so downstream tasks can read it
        ti = context['ti']
        ti.xcom_push(key='order_id', value=order_id)
        ti.xcom_push(key='toppings', value=toppings)

    take_order = PythonOperator(
        task_id='take_order',
        python_callable=take_order_func,
    )

    def check_stock_func(**context):
        """Checks whether all requested toppings are in stock."""
        log = logging.getLogger("airflow.task")
        ti = context['ti']

        
        toppings = ti.xcom_pull(task_ids='take_order', key='toppings')
        order_id = ti.xcom_pull(task_ids='take_order', key='order_id')

        
        out_of_stock_items = ["mozzarella"]
        missing = [t for t in toppings if t in out_of_stock_items]

        if missing:
            log.warning(f"[{order_id}] Out of stock: {missing}. Topping step will be skipped.")
            in_stock = False
        else:
            log.info(f"[{order_id}] All toppings in stock: {toppings}")
            in_stock = True

        ti.xcom_push(key='topping_in_stock', value=in_stock)

    check_ingredient_stock = PythonOperator(
        task_id='check_ingredient_stock',
        python_callable=check_stock_func,
    )

    def decide_branch_func(**context):
        """Decides whether to run add_toppings or skip straight to bake_pizza."""
        log = logging.getLogger("airflow.task")
        ti = context['ti']

        in_stock = ti.xcom_pull(task_ids='check_ingredient_stock', key='topping_in_stock')

        if in_stock:
            log.info("Topping in stock — routing to add_toppings.")
            return 'add_toppings'
        else:
            log.critical("Topping unavailable — skipping add_toppings, going straight to bake.")
            return 'bake_pizza'

    branch_topping_check = BranchPythonOperator(
        task_id='branch_topping_check',
        python_callable=decide_branch_func,
    )

    def add_toppings_func(**context):
        """Adds the requested toppings onto the pizza base."""
        log = logging.getLogger("airflow.task")
        ti = context['ti']

        order_id = ti.xcom_pull(task_ids='take_order', key='order_id')
        toppings = ti.xcom_pull(task_ids='take_order', key='toppings')

        log.info(f"[{order_id}] Applying toppings: {toppings}")
        log.debug(f"[{order_id}] Topping application sequence complete — layer order: cheese first, then pepperoni.")

    add_toppings = PythonOperator(
        task_id='add_toppings',
        python_callable=add_toppings_func,
    )

    bake_pizza = BashOperator(
        task_id='bake_pizza',
        bash_command='echo "Pizza is now baking... "; sleep 3; echo "Baking complete."',
        trigger_rule='none_failed_min_one_success',
    )

    def quality_check_func(**context):
        """Performs a final quality check before dispatch."""
        log = logging.getLogger("airflow.task")
        ti = context['ti']

        order_id = ti.xcom_pull(task_ids='take_order', key='order_id')
        in_stock = ti.xcom_pull(task_ids='check_ingredient_stock', key='topping_in_stock')

        if in_stock:
            log.info(f"[{order_id}] Quality check passed — pizza matches order exactly.")
        else:
            log.warning(f"[{order_id}] Quality check passed with note: delivered without out-of-stock topping.")

    quality_check = PythonOperator(
        task_id='quality_check',
        python_callable=quality_check_func,
    )

    dispatch_delivery = BashOperator(
        task_id='dispatch_delivery',
        bash_command='echo " Pizza dispatched for delivery. Order complete."',
    )


    take_order >> check_ingredient_stock >> branch_topping_check
    branch_topping_check >> [add_toppings, bake_pizza]
    add_toppings >> bake_pizza
    bake_pizza >> quality_check >> dispatch_delivery

