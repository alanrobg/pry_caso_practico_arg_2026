def process_products(raw_products: list) -> list:
    """
    Filtra, transforma y estructura los datos crudos de los productos.
    """
    processed_data = []
    
    for product in raw_products:
        # 1. Filtrar: Descartar productos que no tengan stock disponible
        if product.get("stock", 0) <= 0:
            continue
        
        # 2. Transformar: Calcular el precio final basándonos en el descuento
        original_price = product.get("price", 0.0)
        discount_percentage = product.get("discountPercentage", 0.0)
        
        # Si el precio es 100 y el descuento es 10%, el precio final es 90
        discounted_price = original_price * (1 - (discount_percentage / 100))
        
        # 3. Estructurar: Crear el diccionario final solo con los campos relevantes y limpios
        structured_product = {
            "product_id": product.get("id"),
            "name": str(product.get("title", "")).strip(),
            "category": str(product.get("category", "Uncategorized")).capitalize(),
            "stock_available": product.get("stock"),
            "original_price": round(original_price, 2),
            "final_price": round(discounted_price, 2)
        }
        
        processed_data.append(structured_product)
        
    return processed_data