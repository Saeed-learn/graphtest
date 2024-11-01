import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import BytesIO

# Set the page layout
st.set_page_config(layout="wide")

st.title("Customizable Graph Generator")

# Sidebar inputs
st.sidebar.header("1. Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

st.sidebar.header("2. Graph Settings")
graph_type = st.sidebar.selectbox(
    "Select Graph Type", 
    ["Line Plot", "Bar Plot", "Scatter Plot", "Histogram"]
)
x_col, y_col = None, None
color_picker = st.sidebar.color_picker("Choose a color for the plot", "#1f77b4")

st.sidebar.header("3. Customize Labels")
plot_title = st.sidebar.text_input("Plot Title", "My Plot")
x_label = st.sidebar.text_input("X-axis Label", "X-axis")
y_label = st.sidebar.text_input("Y-axis Label", "Y-axis")

# Output options
st.sidebar.header("4. Output Options")
output_format = st.sidebar.selectbox("Download Format", ["SVG", "PNG", "JPG"])

# Main app
if uploaded_file:
    # Load the data
    df = pd.read_csv(uploaded_file)
    st.write("## Data Preview", df.head())
    
    # Let user select X and Y columns
    columns = df.columns.tolist()
    x_col = st.selectbox("Choose X-axis column", columns)
    y_col = st.selectbox("Choose Y-axis column", columns)
    
    # Generate the plot based on user selections
    fig, ax = plt.subplots(figsize=(10, 6))
    if graph_type == "Line Plot":
        ax.plot(df[x_col], df[y_col], color=color_picker, label=y_col)
    elif graph_type == "Bar Plot":
        ax.bar(df[x_col], df[y_col], color=color_picker, label=y_col)
    elif graph_type == "Scatter Plot":
        ax.scatter(df[x_col], df[y_col], color=color_picker, label=y_col)
    elif graph_type == "Histogram":
        ax.hist(df[y_col], bins=20, color=color_picker, label=y_col)
    
    # Customize plot
    ax.set_title(plot_title, color=color_picker)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend()
    st.pyplot(fig)

    # Download option
    st.write("### Download Plot")
    buffer = BytesIO()
    format_extension = output_format.lower()
    fig.savefig(buffer, format=format_extension)
    st.download_button(
        label=f"Download plot as {output_format}",
        data=buffer,
        file_name=f"custom_plot.{format_extension}",
        mime=f"image/{format_extension}",
    )

else:
    st.info("Awaiting CSV file upload.")
