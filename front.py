import streamlit as st
import pandas as pd
import folium
from datetime import datetime, timedelta
from streamlit_folium import folium_static
from folium.plugins import Fullscreen
from PIL import Image


# Chargement des données depuis un fichier CSV
df = pd.read_csv('prediction_test.csv', delimiter=';')

# Fonction pour obtenir la probabilité d'incendie pour une commune à une date donnée
def get_probabilite(date, commune):
    probabilite = df[(df['commune'] == commune) & (df['date'] == date)]['probabilite'].values[0]
    return probabilite

def create_map(date):
    # Création d'une carte de France
    m = folium.Map(location=[46.227638, 2.213749], zoom_start=5)

    # Ajout d'un bouton pour afficher la carte en plein écran
    folium.plugins.Fullscreen(position='topright', title='Plein écran', title_cancel='Quitter le plein écran', force_separate_button=True).add_to(m)

    # Filtrage des données pour la date sélectionnée
    df_filtered = df[df['date'] == date.strftime('%d/%m/%Y')]

    # Ajout des marqueurs pour chaque commune avec la couleur correspondant à la probabilité
    for index, row in df_filtered.iterrows():
        commune = row['commune']
        probabilite = float(row['probabilite'])
        opacity = max(min((probabilite - 0.05) / 0.7, 1, 0.7), 0.2)
        if opacity > 0.7 :
            opacity = 0.3
        color = 'green' if probabilite < 0.1 else 'orange' if probabilite < 0.4 else 'red'
        folium.CircleMarker(location=[row['latitude'], row['longitude']], radius=5, color=color, fill=True, fill_color=color).add_to(m)
        folium.Circle(location=[row['latitude'], row['longitude']], radius=50000, fill_color=color, color=color, fill_opacity=0.1, popup=f"Probabilité d'incendie : {probabilite:.2f}").add_to(m)

    # Affichage de la carte
    folium_static(m)


st.sidebar.image('wildfire_logo.png', width=300)
st.sidebar.markdown('<h1 style="text-align:center;">WildFire</br></br>PPE</h1>', unsafe_allow_html=True)

# Affichage du sélecteur de date
date = st.date_input("Sélectionnez une date dans le futur :", value=datetime.today() + timedelta(days=1), min_value=datetime(2023, 3, 31) + timedelta(days=1))


# Affichage de la probabilité pour chaque commune pour la date sélectionnée
for index, row in df.iterrows():
    if datetime.strptime(row['date'], '%d/%m/%Y') == date:
        commune = row['commune']
        probabilite = float(row['probabilite'])
        st.write(f"Probabilité d'incendie pour {commune} le {date.strftime('%d/%m/%Y')} : {probabilite}")

# Création de la carte en fonction de la date sélectionnée
create_map(date)


