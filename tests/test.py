from app.services.order import OrderService

order_service = OrderService("http://localhost:8085")
order = order_service.accept_order(1)
print(order)
