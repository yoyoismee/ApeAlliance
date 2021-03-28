import streamlit as st
import random
from ape_guard import do_magic, do_magic_2
import cv2
import matplotlib.pyplot as plt
from io import StringIO

logo = cv2.imread("res/ape_up.png")
logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
logo = cv2.resize(logo, (200, 200))
st.image(logo)

st.title('Ape Together Strong')

st.write('Ape Scout will venture into the chain for ya')
user_input = st.text_input('Contract Address')
bot = st.button('APE Scout!')

st.write('Ape Reader can read your contract')
uploaded_file = st.file_uploader("Choose a file")
bot2 = st.button('APE Read!')

if bot:
    st.title("Your ape going places - not the moon but places")
    magic = do_magic(user_input)
if bot2:
    if uploaded_file is not None:
        st.title("Quiet! Ape Reading")
        string = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        magic = do_magic_2(string)
    else:
        bot2 = False
if bot or bot2:
    st.title("Ape is back!")
    if magic["score"] < 5:
        logo = cv2.imread("res/ape_dead.png")
        logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
        logo = cv2.resize(logo, (200, 200))
        st.image(logo)
    else:
        logo = cv2.imread("res/ape_up.png")
        logo = cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)
        logo = cv2.resize(logo, (200, 200))
        st.image(logo)
    st.title(f'{magic["score"]} / 10 - overall security')
    for k in magic.keys():
        st.write(f'{k} {magic[k]}')
