# Import python packages
import streamlit as st
import requests
import pandas
from snowflake.snowpark.functions import col
from datetime import date

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")
#option = st.selectbox("How would you like to be contacted?",
#    ("Email", "Home phone", "Mobile phone"),label_visibility="hidden")

name_on_order = st.text_input('Name on Smoothie!')
st.write("The name on your smoothie will be: ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredients_list = st.multiselect('Choose up to 5 fruits!', my_dataframe, placeholder="Choose a Fruit!", max_selections=5)

if ingredients_list:
    
    ingredients_string = ''
    time_to_insert = st.button('Submit Order')

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '  
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' , '"""+ name_on_order + """')"""
        #st.write(my_insert_stmt)
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
    
    st.success('Your smoothi is ordered!', icon='✅')
            
   
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
