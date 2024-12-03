import pandas as pd
import streamlit as st
from openai import OpenAI

# Initialize LLaMA API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Title of the application
st.title("Exploragen AI: LLaMA-Powered Interactive Data Analysis")

# Step 1: File Upload
st.sidebar.title("Upload Your Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load the data into a DataFrame
        data = pd.read_csv(uploaded_file)
        st.write("### Uploaded Data Preview")
        st.dataframe(data.head())

        # Step 2: Display available columns
        st.write("### Available Columns in the Dataset")
        available_columns = data.columns.tolist()
        st.write(available_columns)

        # Step 3: User Input for Query
        st.write("### Ask a Question About Your Data")
        user_query = st.text_input("Describe your analysis request (e.g., 'What is the average sales by region?'):")
        
        if user_query:
            # Step 4: Generate Code with LLaMA API
            prompt = f"Given the dataset with columns {available_columns} and the user query: '{user_query}', write Python code to analyze the dataset and answer the query."
            completion = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024
            )

            # Parse the generated response
            if isinstance(completion, dict) and 'choices' in completion:
                # Extract the content from the API response
                generated_response = completion['choices'][0]['message']['content']

                # Attempt to extract the Python code from the response
                start = generated_response.find("```python")
                end = generated_response.find("```", start + len("```python"))

                if start != -1 and end != -1:
                    # Extract code block
                    generated_code = generated_response[start + len("```python"):end].strip()

                    # Display the cleaned code
                    st.write("#### Generated Python Code")
                    st.code(generated_code, language="python")

                    # Step 5: Execute the Generated Code
                    try:
                        local_vars = {"data": data}
                        exec(generated_code, {}, local_vars)

                        # Assuming the code outputs a variable named 'result'
                        result = local_vars.get("avg_age_by_gender")
                        if result is not None:
                            st.write("### Execution Output")
                            st.write(result)
                        else:
                            st.warning("No output generated. Check the logic of the generated code.")
                    except Exception as e:
                        st.error(f"Error executing the code: {e}")
                else:
                    st.error("No valid Python code block found in the response.")
            else:
                st.error(f"Unexpected API response format: {completion}")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to get started.")
