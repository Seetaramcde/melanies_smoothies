# Import python packages
import streamlit as st
import numpy as np
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from datetime import date

today = date.today().strftime("%A")

#if today != "Friday":
#    st.write("Orders are only accepted on Friday")
#    st.stop()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")
#option = st.selectbox("How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone"),label_visibility="hidden")

name_on_order = st.text_input('Name on Smoothie!')
st.write("The name on your smoothie will be: ", name_on_order)

session = get_active_session()



my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 fruits!', my_dataframe, placeholder="Choose a Fruit!", max_selections=5)

if ingredients_list:
    
    ingredients_string = ''
    time_to_insert = st.button('Submit Order')

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '  
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + fruit_chosen + """' , '"""+ name_on_order + """')"""
        #st.write(my_insert_stmt)
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
    
    if time_to_insert: st.success('Your smoothi is ordered!', icon='✅')
            
   
    #st.write(ingredients_string)
    #my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
    #        values ('""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)
    #time_to_insert = st.button('Submit Order')
    #st.write(time_to_insert)
    #if(time_to_insert): 
    #    st.write(fruit_chosen)
    
    #my_insert_stmt = ''   
   # if ingredients_string:
    #    session.sql(my_insert_stmt).collect()
     #   st.success('Your smoothi is ordered!', icon='✅')
