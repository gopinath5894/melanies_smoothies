# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you wanted in your custom smoothie !"
)

nameon_order=st.text_input('Name on Smoothie:')
st.write('The Name on your Order will be : ',nameon_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredients_list=st.multiselect('choose up to 5 Ingredients'
                                ,my_dataframe
                               ,max_selections=5)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen+' | '
#st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + nameon_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    timeto_insert=st.button('Submit Order')

    if timeto_insert:
        session.sql(my_insert_stmt).collect()
        #st.write(session.sql(my_insert_stmt).collect())
        st.success("Your Smoothie is ordered! "+nameon_order, icon="✅")

