import matplotlib.pyplot as plt


def calculate_deltas(closed_orders):
    """
    Calculate deltas for each product based on closed orders.
    Delta is calculated as delivery_date - arrival_date for delivered orders.
    For undelivered orders (delivery_date is None), delta is set to 100.
    """
    product_deltas = []

    # Iterate over each deque in closed_orders, where each deque is dedicated to a specific product
    for order_deque in closed_orders:
        deltas = []
        for order in order_deque:
            if order.delivery_date is not None:
                delta = order.delivery_date - order.arrival_date
            else:
                delta = 100  # Set delta to 100 for undelivered orders
            deltas.append(delta)
        product_deltas.append(deltas)

    return product_deltas





def plot_cumulative_deltas(product_deltas, product_names):
    """Plot cumulative number of orders exceeding delta days for all products in a single plot."""
    plt.figure(figsize=(12, 8))  # Set the figure size

    for deltas, product_name in zip(product_deltas[:6], product_names[:6]):
        if deltas:  # Check if there are deltas to plot
            thresholds = list(range(0, 20, 1))
            cumulative_counts = [len([delta for delta in deltas if delta >= threshold]) for threshold in thresholds]

            plt.plot(thresholds, cumulative_counts, marker='o', label=product_name)  # Use product_name as label for the legend
        else:
            print(f"No data to plot for {product_name}")  # Handle case where no data exists

    plt.title('Cumulative Number of Orders Exceeding Delta Days Across All Products')
    plt.xlabel('Delta Days (Delivery date - Arrival Date)')
    plt.ylabel('Cumulative Number of Orders')
    plt.grid(True)
    plt.legend(title="Products")  # Add a legend to distinguish the lines
    plt.show()


def visualize_order_deltas(closed_orders, config):
    """ Calculate and plot deltas for closed orders. """
    deltas = calculate_deltas(closed_orders)
    product_names = config['product_name']
    plot_cumulative_deltas(deltas, product_names)
