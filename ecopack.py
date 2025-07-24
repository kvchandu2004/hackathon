import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont

# Page Configuration
st.set_page_config(page_title="EcoPack - Sustainable Packaging Optimizer", layout="wide")
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            background-color: #f4f4f4 !important;
            padding: 1rem;
            border-right: 1px solid #ddd;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Title and Subtitle
st.title("\U0001F331 EcoPack - Sustainable Packaging Optimizer")
st.subheader("Optimize your packaging materials for sustainability, cost, and efficiency.")

# Sidebar: User Inputs
st.sidebar.header("\U0001F4E6 Packaging Material Selection")
available_materials = st.sidebar.multiselect("Select the materials you have", ["Plastic", "Paper", "Cardboard", "Biodegradable", "Metal", "Glass"], default=["Plastic", "Paper", "Cardboard"])
if not available_materials:
    st.sidebar.warning("Please select at least one material.")
    st.stop()
material = st.sidebar.selectbox("Material Type", available_materials)
weight = st.sidebar.slider("Weight (g)", 10, 1000, 100)
dimensions = st.sidebar.slider("Total Dimensions (cm³)", 10, 5000, 500)
thickness = st.sidebar.slider("Thickness (mm)", 0.1, 5.0, 0.5)
ink_type = st.sidebar.selectbox("Printing Ink Type", ["Water-based", "Petroleum-based", "UV-based"])
region = st.sidebar.selectbox("Region", ["North America", "Europe", "Asia", "Other"])

# Sustainability Scores & Costs
material_scores = {"Plastic": 20, "Paper": 70, "Cardboard": 80, "Biodegradable": 90, "Metal": 50, "Glass": 60}
cost_per_kg = {"Plastic": 1.5, "Paper": 2.0, "Cardboard": 2.5, "Biodegradable": 3.0, "Metal": 4.5, "Glass": 5.0}

# Sustainability Score Calculation
def calculate_sustainability(material, weight, dimensions, thickness):
    weight_factor = max(0, 100 - weight / 10)
    dimension_factor = max(0, 100 - dimensions / 50)
    thickness_factor = max(0, 100 - thickness * 20)
    return (material_scores[material] * 0.5) + (weight_factor * 0.2) + (dimension_factor * 0.2) + (thickness_factor * 0.1)

sustainability_score = calculate_sustainability(material, weight, dimensions, thickness)
carbon_emission_factors = {"Plastic": 6.0, "Paper": 1.2, "Cardboard": 1.5, "Biodegradable": 0.8, "Metal": 10.0, "Glass": 5.5}
carbon_footprint = (carbon_emission_factors[material] * (weight / 1000))
total_cost = (weight / 1000) * cost_per_kg[material]

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric(label="\U0001F6E0 Sustainability Score", value=f"{sustainability_score:.1f}/100")
col2.metric(label="\U0001F30D Carbon Footprint", value=f"{carbon_footprint:.2f} kg CO₂")
col3.metric(label="\U0001F4B0 Estimated Cost", value=f"${total_cost:.2f}")

# Sustainability Badge Generator (HTML + CSS)
def generate_html_badge(score):
    star_count = round(score / 20)
    stars = "★" * star_count
    badge_html = f"""
    <div style="
        width: 150px; height: 150px; 
        background-color: green; 
        border-radius: 50%;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        color: white; font-family: Arial, sans-serif;
        font-weight: bold; text-align: center;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
    ">
        <div style="font-size: 18px;">EcoPack</div>
        <div style="font-size: 22px; color: gold; margin-top: 5px;">{stars}</div>
    </div>
    """
    return badge_html

# Display the Badge
st.markdown(generate_html_badge(sustainability_score), unsafe_allow_html=True)


# Visualization
st.subheader("\U0001F4CA Cost vs Sustainability Trade-off")
data = pd.DataFrame({"Material": available_materials, "Sustainability Score": [material_scores[m] for m in available_materials], "Cost ($/kg)": [cost_per_kg[m] for m in available_materials]})
fig = px.scatter(data, x="Cost ($/kg)", y="Sustainability Score", size="Sustainability Score", color="Material", title="Cost vs Sustainability Trade-off")
st.plotly_chart(fig)

# Recycling Guide
st.subheader("\U0000267B Recycling & Disposal Guide")
recycling_guide = {
    "Plastic": "Recycle PET (1) and HDPE (2) plastics curbside. Avoid PVC (3) and PS (6).",
    "Paper": "Recycle clean paper. Avoid waxed or food-contaminated paper.",
    "Cardboard": "Flatten and recycle. Waxed cardboard is not recyclable.",
    "Biodegradable": "Compostable in industrial facilities. Check local options.",
    "Metal": "Recycle aluminum and steel curbside. Separate mixed metals.",
    "Glass": "Recycle clear, green, and brown glass separately."
}
st.info(recycling_guide[material])

# Alternative Packaging Suggestion
st.warning(f"\U0001F504 Alternative Suggestion: {material} can be replaced with more sustainable options like biodegradable materials or recycled content.")

# Footer
st.caption("\U0001F680 Built for a Hackathon | EcoPack Team")
