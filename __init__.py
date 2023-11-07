"""UAV-DRONE-PATH Module"""

import os


try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
except Exception as e:
    print(f"Exception {e.__class__.__name__} importing module {os. getcwd()}")
    raise e