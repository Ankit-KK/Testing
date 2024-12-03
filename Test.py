import streamlit as st
import pandas as pd
from openai import OpenAI  # NVIDIA API

# Initialize NVIDIA NeMo API client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Function to interact with the NVIDIA NeMo API
def call_llm_api(prompt):
    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.1-405b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        return response.strip()
    except Exception as e:
        st.error(f"Error calling NVIDIA NeMo API: {e}")
        return None

# App title
st.title("Exploragen AI: NeMo-Powered Interactive Data Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Display available columns
    available_columns = data.columns.tolist()
    st.write("### Available Columns in the Dataset")
    st.write(available_columns)

    # Get user query
    user_query = st.text_input("Describe your analysis request (e.g., 'What is the average sales by region?'):")

    if user_query:
        # Generate the API prompt
        prompt = (
            f"Given the dataset with columns {available_columns} and the query: '{user_query}', "
            f"write Python code to analyze the dataset. "
            f"Return only the code. Do not include explanations, comments, or extra text."
        )

        # Call the API
        with st.spinner("Generating code..."):
            python_code = call_llm_api(prompt)
        
        # Display the code
        if python_code:
            st.write("#### Generated Python Code")
            st.code(python_code, language="python")

            # Attempt to execute the code
            try:
                local_namespace = {"data": data}
                exec(python_code, {}, local_namespace)

                # Display execution result if 'result' is available
                if "result" in local_namespace:
                    st.write("### Execution Output")
                    st.write(local_namespace["result"])
                else:
                    st.warning("No 'result' variable found in the generated code.")
            except Exception as e:
                st.error(f"Error executing the code: {e}")
        else:
            st.error("Failed to generate Python code from the API response.")
