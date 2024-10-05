import streamlit as st
import numpy as np
import pandas as pd
import time

"""
## Your eco-friendly image generator: [INSERT NAME HERE]
#### A memoized stable diffusion image generator
"""

@st.cache_data
def text_entry(entry1) :
    return '...'