from app.services.order import OrderService

order_service = OrderService("http://localhost:3000")
order = order_service.accept_order(1)
print(order)