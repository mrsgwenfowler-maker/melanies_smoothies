# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
from snowflake.snowpark.table import WhenMatchedClause

# Write directly to the app
st.title("🥤 Pending Smoothie Orders! 🥤")
st.write(
  """Orders that need to be filled.
  """
)


session = get_active_session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
my_dataframe = session.table("smoothies.public.orders") \
    .filter(col("ORDER_FILLED") == 0) \
    .collect()
# editable_df = st.data_editor(my_dataframe)


if my_dataframe:
    editable_df = st.data_editor(my_dataframe)
    submitted = st.button('Submit')
    if submitted:

        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df, schema=og_dataset.schema)
          
        try:
            og_dataset.merge(edited_dataset
                       , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                         , [WhenMatchedClause().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                        )   
            st.success('Someone clicked the button.', icon="👍")
        except:
            st.write('Something went wrong')
else:
    st.success('Someone clicked the button.', icon="👍")
