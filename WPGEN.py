import streamlit as st

import random

import numpy as np
import matplotlib.pyplot as plt

import sys
import io
from PIL import Image, ImageFilter
import time
from io import BytesIO
import base64


if "offset" not in st.session_state: 
    st.session_state["offset"]=0

if "image" not in st.session_state:
    st.session_state["image"] = None

def random_color(seed=None):
    if seed is not None:
    	random.seed(seed)
    return "#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
    

st.title("Blurry wallpaper generator")
st.text("")
st.text("")
st.text("")



st.sidebar.subheader("Resolution")
height_box = st.sidebar.number_input("height", min_value=10, max_value=5000, value=1080, step=1, 
	format=None, key=None, help=None, on_change=None, args=None, kwargs=None)
	
width_box = st.sidebar.number_input("width", min_value=10, max_value=5000, value=1920, step=1, 
	format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

grid_expander = st.sidebar.beta_expander("Grid dimensions", expanded=False)
with grid_expander:
    st.header("Grid dimensions")
    grid_h = st.slider("rows", min_value=2, max_value=5, value=3, step=1, 
	format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

    grid_w = st.slider("columns", min_value=2, max_value=5, value=3, step=1, 
	format=None, key=None, help=None, on_change=None, args=None, kwargs=None)

st.sidebar.subheader("Blur strength")

blur_str = st.sidebar.slider("", min_value=0, max_value=1000, value=350, step=1, 
	format=None, key=None, help=None, on_change=None, args=None, kwargs=None)


##########################
def on_color_clicked():
    global offset
    with color_pickers_container:
        h = grid_h
        w = grid_w
    
        global pickers
        global first 
    
    random.seed(time.time_ns())
    st.session_state["offset"] = random.randint(-sys.maxsize, sys.maxsize)
           
                      
st.sidebar.header("Tiles color")    

color_pickers_container = st.sidebar.beta_container()

def build_color_pickers(offset):
    with color_pickers_container:
        h = grid_h
        w = grid_w
    
        global pickers
        global first 
    
        cols = st.beta_columns(w)
    
        pickers = []
        for i in range(h):
            pick = []
            for j in range(w):
                with cols[j]:
            	    p = st.color_picker("", value=random_color(seed=j+i*w+offset),
            	     key=str(j+i*w),
             		    help=None, on_change=None, args=None, kwargs=None)
                pick.append(p)
            
            pickers.append(pick)

build_color_pickers(st.session_state["offset"])	

st.sidebar.text("")
shuffle_col = st.sidebar.button("Shuffle colors", key=None, help=None, on_click=on_color_clicked, 
	args=None, kwargs=None)
##########################


# https://stackoverflow.com/q/29643352
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    
    
def get_image(colors, strength=100):
    # convrt in rgb
    rgb_colors = []
    for row in colors:
        rgb = []
        for color in row:
            rgb.append(hex_to_rgb(color))
        rgb_colors.append(rgb)


    # generate canvas
    height = height_box
    width = width_box
    canvas = np.zeros((height, width, 3), dtype=int)


    # draw color patches
    h = grid_h
    w = grid_w

    h_limits = np.linspace(0, height, h+1, dtype=int)
    w_limits = np.linspace(0, width, w+1, dtype=int)
    

    for i in range(h):
        for j in range(w):
            canvas[h_limits[i]:h_limits[i+1], w_limits[j]:w_limits[j+1]] = rgb_colors[i][j]

    
    image = Image.fromarray(canvas.astype('uint8'), 'RGB')
    
    # blur the hell out of it
    #blurred = image.filter(ImageFilter.BoxBlur(radius=5))
    #blurred = image.filter(ImageFilter.GaussianBlur(radius=strength//4))
    #blurred = blurred.filter(ImageFilter.BoxBlur(radius=strength//2))
    blurred = image.filter(ImageFilter.GaussianBlur(radius=strength))
    return np.array(blurred), blurred  
    

###########################
image_container = st.beta_container()
download_container = st.beta_container()
spinner_container = st.empty()

with spinner_container:
    spinner = st.spinner("Generating wallpaper...")

with spinner:
    image, PIL_image = get_image(pickers, strength=blur_str) 
    st.session_state["image"]=image


    if st.session_state["image"] is not None:	
        with image_container:
	        st.image(st.session_state["image"] , caption=None, width=None, use_column_width=None, 
               clamp=False, channels="RGB", output_format="png")
           


def get_image_download_link(img,filename,text):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href =  f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

with download_container:
    st.text("")
    st.text("")  
    st.markdown(get_image_download_link(PIL_image, "WPGEN.png", f"Download {width_box}x{height_box} version"), unsafe_allow_html=True)

    

###########################
with st.sidebar.beta_container():
    st.header("Credits")
    
    st.caption("Lorenzo De Nisi")
    st.markdown("[GitHub](https://github.com/lorenzodenisi)")



    
    
    
    
    
    
    
    
    
    
    
    

