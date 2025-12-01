def get_invoice(customer_id: str):
    """Fetch latest invoice for the given customer."""
    return {"invoice_id": "INV123", "amount": 49.0, "status": "paid"}

def initiate_refund(invoice_id: str, amount: float):
    """Process refund for an invoice."""
    return {"status": "success", "refunded": amount}
