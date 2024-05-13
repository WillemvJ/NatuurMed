configuration = {
    'product_name': ['CL20', 'CL50', 'CL100', 'AD20', 'AD50', 'AD100'],
    #in ml:
    'product_volume': [20, 50, 100, 20, 50, 100],
    # from case, in working days, leaving 5 days for delivery.
    'product_demand_lead-time': 25,
    # 0 is CL formulation, 1 is AD
    'product_bottle_type': [0, 1, 2, 0, 1, 2],
    'product_mix_type': [0, 0, 0, 1, 1, 1],
    #interpretation of the given Table
    'herb_available_months': [[1, 2, 3], [6, 7, 8, 9], [6, 7, 8, 9, 10], [7, 8, 9], [6, 7, 8, 9], [6, 7, 8, 9],
                              [4, 5, 6, 7, 8], [4, 5, 6, 7, 8, 9], [6, 7, 8, 9, 10, 11]],
    #from the conceptual case:
    'extraction_percentages': [[0.1, 0.1, 0.045, 0.1, 0.12, 0.09, 0.155, 0.09, 0.2],
                               [0.14, 0.14, 0, 0.15, 0.18, 0, 0.19, 0.2, 0]],
    # it is not clear whether these initial amounts are reasonable. Please argue for an appropriate initialization.
    'initial_herb_inventory': [2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000],
    # it is not clear whether these initial amounts are reasonable. Please argue for an appropriate initialization.
    'num_initial_mix_storage_containers': [2, 2],
    'production_volumes_per_line': [[3000, 3000, 1500], [6000, 5500, 3000]],
    # note that first line cannot produce AD products:
    'capabilities_per_line': [[1, 1, 1, 0, 0, 0], [1, 1, 1, 1, 1, 1]],
    # assume that initially, CL20 is set up on machine 1, while AD20 is set up on machine 2
    'initial_product_per_filling_line': [0, 3],
    'filling_line_minor_setup_in_minutes': 60,
    'filling_line_major_setup_in_minutes': 480,
    'mix_expiry_days': 100,
    # in working days:
    'bulk_production_time': 10
}
