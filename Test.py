import streamlit as st
import pandas as pd
import openai

# Function to interact with the API
def call_llm_api(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="meta/llama-3.1-405b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=150,
            api_key = "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", 
        )
        return response
    except Exception as e:
        st.error(f"Error calling LLM API: {e}")
        return None

# Function to extract Python code from the API response
def extract_code_from_response(response):
    if response and "choices" in response and len(response["choices"]) > 0:
        return response["choices"][0].get("message", {}).get("content", "").strip()
    return None

# App title
st.title("Exploragen AI: LLaMA-Powered Interactive Data Analysis")

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
            response = call_llm_api(prompt)
        
        # Extract and display the code
        python_code = extract_code_from_response(response)
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
            st.error(f"Unexpected API response format: {response}")
