import pandas as pd
import numpy as np


def process_layers(materials,height):
    # Convert the list of materials into a dictionary
    # processed_dict = {f"layer{i+1}": material for i, material in enumerate(materials)}
    chart_data = pd.DataFrame(np.random.randn(20, 1), columns=["c"])
    return chart_data
