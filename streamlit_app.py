# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize your smoothi!:cup_with_straw: {st.__version__}")
st.write(
  """Choose the friuts you want in your custom Smoothie!
  """
)


NAME_ON_ORDER = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be: ", NAME_ON_ORDER)

ncx=st.connection("snowflake")
session = ncx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredient_list = st.multiselect(

    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections= 5 
)

if ingredient_list:
    
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen +'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)

   
    my_inset_stmt = """insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
    values ('""" + ingredients_string + """','"""  +   NAME_ON_ORDER +   """')"""

    time_to_insert = st.button('submit order')

    if time_to_insert:
        if my_inset_stmt:
            session.sql(my_inset_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")



