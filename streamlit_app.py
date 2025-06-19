
import streamlit as st
import requests
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', my_dataframe, max_selections=5
)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)

    for fruit in ingredients_list:
        st.subheader(f"{fruit} Nutrition Information")
        response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        st.dataframe(response.json(), use_container_width=True)

    st.write(ingredients_string)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """

    # Define the button once, inside this conditional block
    if st.button('Submit Order'):
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")


