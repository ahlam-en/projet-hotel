import streamlit as st
import sqlite3
from datetime import date

# Connexion à la base de données
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# Fonctions de base de données
def get_clients():
    cursor.execute("SELECT * FROM Client")
    return cursor.fetchall()

def get_reservations():
    cursor.execute("SELECT * FROM Reservation")
    return cursor.fetchall()

def get_chambres_disponibles(debut, fin):
    cursor.execute("""
        SELECT * FROM Chambre
        WHERE idChambre NOT IN (
            SELECT idChambre FROM Reservation
            WHERE (? <= dateFin) AND (? >= dateDebut)
        )
    """, (debut, fin))
    return cursor.fetchall()

def ajouter_client(nom, prenom, email):
    cursor.execute("INSERT INTO Client (nom, prenom, email) VALUES (?, ?, ?)", (nom, prenom, email))
    conn.commit()

def ajouter_reservation(idClient, idChambre, dateDebut, dateFin):
    cursor.execute("INSERT INTO Reservation (idClient, idChambre, dateDebut, dateFin) VALUES (?, ?, ?, ?)",
                   (idClient, idChambre, dateDebut, dateFin))
    conn.commit()

# Interface Streamlit
st.title("🏨 Gestion de l'Hôtel")

menu = st.sidebar.radio("Menu", ["Réservations", "Clients", "Chambres Disponibles", "Ajouter un Client", "Ajouter une Réservation"])

if menu == "Réservations":
    st.header("📅 Liste des Réservations")
    reservations = get_reservations()
    for r in reservations:
        st.write(r)

elif menu == "Clients":
    st.header("👥 Liste des Clients")
    clients = get_clients()
    for c in clients:
        st.write(c)

elif menu == "Chambres Disponibles":
    st.header("🛏️ Chambres Disponibles")
    debut = st.date_input("Date de début", value=date.today())
    fin = st.date_input("Date de fin", value=date.today())
    if debut > fin:
        st.error("La date de début doit être avant la date de fin.")
    else:
        chambres = get_chambres_disponibles(debut, fin)
        for ch in chambres:
            st.write(ch)

elif menu == "Ajouter un Client":
    st.header("➕ Ajouter un Client")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    if st.button("Ajouter"):
        if nom and prenom and email:
            ajouter_client(nom, prenom, email)
            st.success("Client ajouté avec succès.")
        else:
            st.warning("Veuillez remplir tous les champs.")

elif menu == "Ajouter une Réservation":
    st.header("➕ Ajouter une Réservation")
    idClient = st.number_input("ID Client", min_value=1, step=1)
    idChambre = st.number_input("ID Chambre", min_value=1, step=1)
    dateDebut = st.date_input("Date de début", value=date.today())
    dateFin = st.date_input("Date de fin", value=date.today())
    if st.button("Ajouter la réservation"):
        if dateDebut <= dateFin:
            ajouter_reservation(idClient, idChambre, dateDebut, dateFin)
            st.success("Réservation ajoutée avec succès.")
        else:
            st.error("La date de début doit être avant la date de fin.")
