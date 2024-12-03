import streamlit as st
import pandas as pd
import io

# Title of the application
st.title("Exploragen AI: Interactive Data Analysis")

# Step 1: File Upload
st.sidebar.title("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Load the data into a DataFrame
    try:
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview")
        st.dataframe(data.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Step 2: User Input for Query
    st.write("### Ask a Question About Your Data")
    user_query = st.text_input(
        "Describe your analysis request (e.g., 'What is the average sales by region?'):"
    )

    if user_query:
        # Step 3: Generate Code (Mockup)
        # For now, we'll generate mock code for prototyping
        generated_code = """
import pandas as pd
# Assuming 'data' is the DataFrame
result = data.groupby('Region')['Sales'].mean()
result
"""
        st.write("#### Generated Code")
        st.code(generated_code, language="python")

        # Step 4: Execute the Code
        st.write("#### Execution Output")
        try:
            # Define the execution environment (sandboxing can be added later)
            local_vars = {"data": data}
            exec(generated_code, {}, local_vars)
            result = local_vars.get("result")

            if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
                st.write(result)
            else:
                st.write("Output:", result)
        except Exception as e:
            st.error(f"Error executing the code: {e}")

else:
    st.info("Please upload a CSV file to get started.")
