import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz
import os
import plotly.express as px
# %config Completer.use_jedi = False
import ipywidgets as widgets
from ipyfilechooser import FileChooser
from pathlib import Path
import shutil

from IPython.core.display import display, HTML
display(HTML(
    '<style>'
        '#notebook { padding-top:0px !important; } ' 
        '.container { width:100% !important; } '
        '.end_space { min-height:0px !important; } '
    '</style>'
))