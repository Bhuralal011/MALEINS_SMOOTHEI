import streamlit as st
import requests
import pandas as pd
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruit you want to customize your smoothie with")

# --- Snowflake Connection ---
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()

# --- User Inputs ---
NAME_ON_ORDER = st.text_input("NAME ON SMOOTHIE")
st.write("The name on your smoothie is ", NAME_ON_ORDER)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    pd_df['FRUIT_NAME'].tolist(),
    max_selections=5
)

# --- Initialize INGREDIENTS_STRING safely ---
INGREDIENTS_STRING = ""
if ingredients_list:
    INGREDIENTS_STRING = ", ".join(ingredients_list)  # comma-separated list
    for fruit_chosen in ingredients_list:
    search_on = pd_df.loc[
        pd_df['FRUIT_NAME'] == fruit_chosen,
        'SEARCH_ON'
    ].iloc[0]

    st.write(f"The search value for {fruit_chosen} is {search_on}.")
    st.subheader(f"{fruit_chosen} Nutrition Information")

    response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")

    if response.status_code == 200:
        data = response.json()

        nutrition_rows = []
        for nutrient, value in data["nutritions"].items():
            nutrition_rows.append({
                "nutrient": nutrient,
                "family": data["family"],
                "genus": data["genus"],
                "id": data["id"],
                "name": data["name"],
                "nutrition": value,
                "order": data["order"]
            })

        sf_df = pd.DataFrame(nutrition_rows)
        st.dataframe(sf_df, use_container_width=True)
    else:
        st.error(f"{fruit_chosen} not found in database.")

    # for fruit_chosen in ingredients_list:
    #     search_on = pd_df.loc[
    #         pd_df['FRUIT_NAME'] == fruit_chosen,
    #         'SEARCH_ON'
    #     ].iloc[0]

    #     st.write(f"The search value for {fruit_chosen} is {search_on}.")
    #     st.subheader(fruit_chosen + " Nutrition Information")
    #     response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
    #     data = response.json()
        # sf_df = pd.DataFrame([data])
        # st.dataframe(sf_df, width="stretch")
      




st.write("Ingredients selected: ", INGREDIENTS_STRING)

# --- Insert Order into Snowflake ---
if st.button("Submit Order"):
    if NAME_ON_ORDER and INGREDIENTS_STRING:
        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, NAME_ON_ORDER)
        VALUES ('{INGREDIENTS_STRING}', '{NAME_ON_ORDER}');
        """
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
    else:
        st.error("Please enter your name and select at least one ingredient.")



# # Import python packages
# import streamlit as st
# import requests
# import pandas as pd
# #from snowflake.snowpark.context import get_active_session
# # Write directly to the app
# st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
# st.write(
#   """Chose the fruit you went to custom your smoothie
#   """
# )
# from snowflake.snowpark.functions import col
# cnx = st.connection("snowflake")
# session = cnx.session()
# #session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select (col('fruit_name'), col('SEARCH_ON'))
# # st.dataframe(data=my_dataframe, use_container_width=True)
# # st.stop()
# # convert the snowpark dataframe to a pandas dataframe so we can use the loc functtion
# pd_df = my_dataframe.to_pandas()
# # st.dataframe(pd_df)
# # st.stop()
# NAME_ON_ORDER = st.text_input("NAME ON SMOOTHIE")
# st.write("The name on your smoothie is ", NAME_ON_ORDER)
# ingredients_list = st.multiselect(
#     ' Choose up to 5 ingredients',
#     my_dataframe,
#     max_selections = 5
#  )
# if ingredients_list:
#     INGREDIENTS_STRING = ' '
#     for fruit_chosen in ingredients_list:
#         INGREDIENTS_STRING += fruit_chosen + ' '
    
#         search_on = pd_df.loc[
#             pd_df['FRUIT_NAME'] == fruit_chosen,
#             'SEARCH_ON'
#         ].iloc[0]
    
#         st.write(
#             'The search value for ',
#             fruit_chosen,
#             ' is ',
#             search_on,
#             '.'
#         )
#         st.subheader(fruit_chosen + ' Nutrition Information')
#         response = requests.get(
#             "https://my.smoothiefroot.com/api/fruit/" + search_on
#         )
#         data = response.json()
#         sf_df = pd.DataFrame([data])
    
#         st.dataframe(sf_df, width="stretch")
# st.write(INGREDIENTS_STRING)
# my_insert_stmt = """ insert into smoothies.public.orders(ingredients , NAME_ON_ORDER)
#         values ('""" + INGREDIENTS_STRING + """' ,'"""+ NAME_ON_ORDER +"""' )"""
# time_to_insert = st.button('submit order')
# if time_to_insert:
#     session.sql(my_insert_stmt).collect()
#     st.success('Your Smoothie is ordered!', icon="✅")

    
    
















    
