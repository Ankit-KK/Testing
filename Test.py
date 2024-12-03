import pandas as pd
import streamlit as st
from openai import OpenAI

# Initialize the AI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="import pandas as pd
import streamlit as st
from openai import OpenAI

# Initialize the AI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="your-api-key-here"
)

# Title of the application
st.title("Exploragen AI: LLaMA-Powered Interactive Data Analysis")

# Step 1: File Upload
st.sidebar.title("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load the dataset
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview")
        st.dataframe(data.head())

        # Display available columns
        st.write("### Available Columns in the Dataset")
        available_columns = data.columns.tolist()
        st.write(available_columns)

        # User input for query
        st.write("### Ask a Question About Your Data")
        user_query = st.text_input("Describe your analysis request (e.g., 'What is the average sales by region?'):")

        if user_query:
            # Generate code using LLaMA API
            prompt = f"Given the dataset with columns {available_columns} and the user query: '{user_query}', write Python code to analyze the dataset and answer the query."
            response = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024
            )

            # Extract the Python code from the API response
            if "choices" in response:
                response_content = response['choices'][0]['message']['content']

                # Attempt to find the Python code block
                start = response_content.find("```python")
                end = response_content.find("```", start + len("```python"))

                if start != -1 and end != -1:
                    # Extract the code
                    python_code = response_content[start + len("```python"):end].strip()

                    # Display the generated code
                    st.write("#### Generated Python Code")
                    st.code(python_code, language="python")

                    # Execute the code
                    try:
                        # Define a local namespace for code execution
                        local_namespace = {"data": data}
                        exec(python_code, {}, local_namespace)

                        # Try to find results in the local namespace
                        if "result" in local_namespace:
                            st.write("### Execution Output")
                            st.write(local_namespace["result"])
                        else:
                            st.warning("No 'result' variable found in the generated code output.")
                    except Exception as e:
                        st.error(f"Error executing the code: {e}")
                else:
                    st.error("No valid Python code block found in the response.")
            else:
                st.error(f"Unexpected API response format: {response}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to get started.")
"
)

# Title of the application
st.title("Exploragen AI: LLaMA-Powered Interactive Data Analysis")

# Step 1: File Upload
st.sidebar.title("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load the dataset
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview")
        st.dataframe(data.head())

        # Display available columns
        st.write("### Available Columns in the Dataset")
        available_columns = data.columns.tolist()
        st.write(available_columns)

        # User input for query
        st.write("### Ask a Question About Your Data")
        user_query = st.text_input("Describe your analysis request (e.g., 'What is the average sales by region?'):")

        if user_query:
            # Generate code using LLaMA API
            prompt = f"Given the dataset with columns {available_columns} and the user query: '{user_query}', write Python code to analyze the dataset and answer the query."
            response = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024
            )

            # Extract the Python code from the API response
            if "choices" in response:
                response_content = response['choices'][0]['message']['content']

                # Attempt to find the Python code block
                start = response_content.find("```python")
                end = response_content.find("```", start + len("```python"))

                if start != -1 and end != -1:
                    # Extract the code
                    python_code = response_content[start + len("```python"):end].strip()

                    # Display the generated code
                    st.write("#### Generated Python Code")
                    st.code(python_code, language="python")

                    # Execute the code
                    try:
                        # Define a local namespace for code execution
                        local_namespace = {"data": data}
                        exec(python_code, {}, local_namespace)

                        # Try to find results in the local namespace
                        if "result" in local_namespace:
                            st.write("### Execution Output")
                            st.write(local_namespace["result"])
                        else:
                            st.warning("No 'result' variable found in the generated code output.")
                    except Exception as e:
                        st.error(f"Error executing the code: {e}")
                else:
                    st.error("No valid Python code block found in the response.")
            else:
                st.error(f"Unexpected API response format: {response}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to get started.")
