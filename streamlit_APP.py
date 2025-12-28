# Import python packages
import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session



# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Chose the fruit you went to custom your smoothie
  """
)

from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()
#session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()
# convert the snowpark dataframe to a pandas dataframe so we can use the loc functtion
pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)
# st.stop()



NAME_ON_ORDER = st.text_input("NAME ON SMOOTHIE")
st.write("The name on your smoothie is ", NAME_ON_ORDER)


ingredients_list = st.multiselect(
    ' Choose up to 5 ingredients',
    my_dataframe,
    max_selections = 5
 )
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    INGREDIENTS_STRING = ' '

    # for fruit_chosen in ingredients_list:
    #    INGREDIENTS_STRING += fruit_chosen + ' '
      
    #    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    #    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
    #    st.subheader(fruit_chosen +' '+ '  Nutrition Information')
    #    smootheifroot_response = requests.get(
    #    "https://my.smoothiefroot.com/api/fruit/watermelon" + fruit_chosen
    #     )
    #    data = smootheifroot_response.json()      # dict
    #    sf_df = pd.DataFrame([data])   # REAL DataFrame
    #    st.dataframe(sf_df, use_container_width=True)
    for fruit_chosen in ingredients_list:
        INGREDIENTS_STRING += fruit_chosen + ' '
    
        search_on = pd_df.loc[
            pd_df['FRUIT_NAME'] == fruit_chosen,
            'SEARCH_ON'
        ].iloc[0]
    
        st.write(
            'The search value for ',
            fruit_chosen,
            ' is ',
            search_on,
            '.'
        )
    
        st.subheader(fruit_chosen + ' Nutrition Information')
    
        response = requests.get(
            "https://my.smoothiefroot.com/api/fruit/" + search_on
        )
    
        data = response.json()
        sf_df = pd.DataFrame([data])
    
        st.dataframe(sf_df, width="stretch")

st.write(INGREDIENTS_STRING)

    
      

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients , NAME_ON_ORDER)
            values ('""" + INGREDIENTS_STRING + """' ,'"""+ NAME_ON_ORDER +"""' )"""

    # st.write(my_insert_stmt)
    # st.stop()


    time_to_insert = st.button('submit order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
    

# # import requests
# smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())

# sf_df = st.dataframe(data=smoothiefroot_response.json() , use_container_width=True)



# smootheifroot_response = requests.get(
#     "https://my.smoothiefroot.com/api/fruit/watermelon"
# )

# data = smootheifroot_response.json()      # dict
# sf_df = pd.DataFrame([data])   # REAL DataFrame

# st.dataframe(sf_df, use_container_width=True)












    
