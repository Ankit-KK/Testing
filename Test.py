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

            st.code(generated_code, language="python")
        except Exception as e:
            st.error(f"Error generating code with LLaMA: {e}")
            st.stop()

        # Step 4: Execute the Generated Code
st.write("#### Execution Output")
try:
    # Define the execution environment
    local_vars = {"data": data}

    # Strip unnecessary text from generated code (basic filtering)
    generated_code_lines = generated_code.split("\n")
    filtered_code = "\n".join(
        line for line in generated_code_lines if not line.startswith("#") and "Example Output" not in line
    )

    st.write("Filtered Code for Execution:")
    st.code(filtered_code, language="python")

    # Execute the filtered code
    exec(filtered_code, {}, local_vars)

    # Extract the result if available
    result = local_vars.get("average_age_by_gender")

    if result is not None:
        if isinstance(result, pd.Series) or isinstance(result, pd.DataFrame):
            st.write(result)
        else:
            st.write("Output:", result)
    else:
        st.warning("No output variable found. Please review the generated code.")
except Exception as e:
    st.error(f"Error executing the code: {e}")


else:
    st.info("Please upload a CSV file to get started.")
