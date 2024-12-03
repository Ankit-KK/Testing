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
        st.write(data.columns.tolist())

        # Step 3: User Input for Query
        st.write("### Ask a Question About Your Data")
        user_query = st.text_input("Describe your analysis request (e.g., 'What is the average sales by region?'):")
        
        if user_query:
            # Step 4: Generate Code with LLaMA API
            prompt = f"Given the dataset with columns {data.columns.tolist()} and the user query: '{user_query}', write Python code to analyze the dataset and answer the query."
            completion = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024
            )

            # Collect the generated code
            generated_code = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    generated_code += chunk.choices[0].delta.content
            
            # Clean the generated code and display it
            start_marker = "```python"
            end_marker = "```"
            if start_marker in generated_code and end_marker in generated_code:
                cleaned_code = generated_code.split(start_marker)[1].split(end_marker)[0].strip()
            else:
                st.error("No valid Python code found in the generated response.")
                st.stop()

            st.write("#### Cleaned Code for Execution")
            st.code(cleaned_code, language="python")

            # Step 5: Execute the Generated Code
            try:
                local_vars = {"data": data}
                exec(cleaned_code, {}, local_vars)

                # Get the result of the execution
                result = local_vars.get("result")  # Change 'result' based on your code output variable
                if result is not None:
                    st.write("Execution Output:")
                    st.write(result)
                else:
                    st.warning("No output generated. Check the logic of the generated code.")
            except Exception as e:
                st.error(f"Error executing the code: {e}")

    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV file to get started.")
