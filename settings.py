config = {
    'product_name': ['CL20', 'CL50', 'CL100', 'AD20', 'AD50', 'AD100'],
    'product_volume': [20, 50, 100, 20, 50, 10],
    'product_demand_lead-time': 30,
    # 0 is CL formulation, 1 is AD
    'product_type': [0, 0, 0, 1, 1, 1],
    'herb_available_months': [[1, 2, 3], [6, 7, 8, 9], [6, 7, 8, 9, 10], [7, 8, 9], [6, 7, 8, 9], [6, 7, 8, 9],
                              [4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9], [6, 7, 8, 9, 10, 11]],
    'herb_extract_ratios': [3.5, 2.5, 5, 4, 4, 3.5, 4, 4, 5],
    'initial_herb_inventory': [1000 for _ in range(9)],
    'production_volumes_per_line': [[3000, 3000, 1500], [6000, 5500, 3000]],
    # note that first line cannot produce AD products:
    'capabilities_per_line': [[1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1]],
    # assume that initially, AD20 is set up on machine 2, while CL20 is set up on machine 1.
    'initial_product_per_filling_line': [0, 3],
    'filling_line_minor_setup_in_minutes': 10,
    'filling_line_major_setup_in_minutes': 120
}
