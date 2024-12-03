import streamlit as st
import pandas as pd
from openai import OpenAI  # NVIDIA OpenAI API wrapper

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
        # Step 3: Generate Code with LLaMA API
        st.write("#### Generating Python Code...")
        try:
            prompt = f"Write Python code to analyze the following dataset based on the question: {user_query}. Assume the data is loaded in a Pandas DataFrame named 'data'."
            completion = client.chat.completions.create(
                model="meta/llama-3.1-405b-instruct",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                top_p=0.7,
                max_tokens=1024,
                stream=True
            )

            # Collect the generated code
            generated_code = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    generated_code += chunk.choices[0].delta.content

            # Clean the generated code to isolate the Python snippet
            start_marker = "```python"
            end_marker = "```"
            if start_marker in generated_code and end_marker in generated_code:
                cleaned_code = generated_code.split(start_marker)[1].split(end_marker)[0].strip()
            else:
                st.error("No valid Python code found in the generated response.")
                st.stop()

            # Display the cleaned code
            st.write("#### Cleaned Code for Execution")
            st.code(cleaned_code, language="python")

        except Exception as e:
            st.error(f"Error generating code with LLaMA: {e}")
            st.stop()

        # Step 4: Validate Dataset Columns and Execute Code
        try:
            # Dynamically execute the cleaned Python code
            local_vars = {"data": data}
            exec(cleaned_code, {}, local_vars)

            # Retrieve a known variable (modify as per code logic)
            result = local_vars.get("average_age")  # Adjust based on variable in code
            if result is not None:
                st.write("Execution Output:")
                st.write(result)
            else:
                st.warning("No output generated. Check the logic of the generated code.")
        except Exception as e:
            st.error(f"Error executing the code: {e}")

else:
    st.info("Please upload a CSV file to get started.")
