import random
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.entities.customer import Customer, Order, Product, OrderItem

fake = Faker()
fake.unique.clear()

statuses = ["active", "trial", "churned"]
order_statuses = ["completed", "pending", "cancelled"]
categories = ["saas", "subscription", "hardware"]


async def create_sample_data(db: AsyncSession):
    async with db.begin():
        await db.execute(
            text(
                "TRUNCATE TABLE order_items, orders, products, customers RESTART IDENTITY CASCADE"
            )
        )

        # Create products
        products = [
            Product(
                name=fake.bs().title(),
                category=random.choice(categories),
                price=round(random.uniform(20, 500), 2),
            )
            for _ in range(10)
        ]
        db.add_all(products)
        await db.flush()

        # Create customers and nested data
        for _ in range(20):
            customer = Customer(
                name=fake.name(),
                email=fake.unique.email(),
                location=fake.city(),
                signup_date=fake.date_between(start_date="-2y", end_date="today"),
                status=random.choice(statuses),
            )
            db.add(customer)
            await db.flush()

            for _ in range(random.randint(1, 5)):
                order = Order(
                    customer_id=customer.id,
                    order_date=fake.date_between(
                        start_date=customer.signup_date, end_date="today"
                    ),
                    status=random.choice(order_statuses),
                )
                db.add(order)
                await db.flush()

                for _ in range(random.randint(1, 3)):
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=random.choice(products).id,
                        quantity=random.randint(1, 10),
                    )
                    db.add(order_item)
