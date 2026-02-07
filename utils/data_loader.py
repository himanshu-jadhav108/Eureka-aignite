import streamlit as st
import pandas as pd
from data.sample_generator import generate_sample_data


def load_and_validate_data(uploaded_file=None):

    if uploaded_file is not None:
        try:
            # Reset file pointer (CRITICAL FIX)
            uploaded_file.seek(0)

            # Check file size
            if uploaded_file.size == 0:
                st.error("❌ Uploaded file is empty.")
                return None

            # Try reading safely
            df = pd.read_csv(uploaded_file)

            if df.empty:
                st.error("❌ Uploaded CSV contains no data.")
                return None

            st.sidebar.success("✅ File uploaded successfully!")

        except pd.errors.EmptyDataError:
            st.error("❌ The file is empty or invalid CSV format.")
            return None

        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None

    else:
        df = generate_sample_data()
        st.sidebar.info("📊 Using AI-generated sample data")

    # Validate required columns
    required_cols = ['date', 'product_id', 'units_sold']
    missing = [col for col in required_cols if col not in df.columns]

    if missing:
        st.error(f"❌ Missing required columns: {', '.join(missing)}")
        return None

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce').fillna(0)
    df = df.sort_values('date').reset_index(drop=True)

    return df


# import streamlit as st
# import pandas as pd
# from data.sample_generator import generate_sample_data


# def load_and_validate_data(uploaded_file=None):
#     """Load CSV file or generate sample data, then validate and clean it."""

#     if uploaded_file is not None:
#         try:
#             # Reset pointer (important when re-uploading)
#             uploaded_file.seek(0)

#             # Check file size safely
#             if uploaded_file.size == 0:
#                 st.error("❌ Uploaded file is empty.")
#                 return None

#             # Read CSV
#             df = pd.read_csv(uploaded_file)

#             if df.empty:
#                 st.error("❌ Uploaded CSV contains no data.")
#                 return None

#             # Clean column names (VERY IMPORTANT)
#             df.columns = df.columns.str.strip().str.lower()

#             st.sidebar.success("✅ File uploaded successfully!")

#             # Show clean preview
#             with st.expander("📂 Preview Uploaded Data", expanded=False):
#                 st.dataframe(df.head(20), use_container_width=True)

#         except pd.errors.EmptyDataError:
#             st.error("❌ The file is empty or invalid CSV format.")
#             return None

#         except Exception as e:
#             st.error(f"❌ Error loading file: {str(e)}")
#             return None

#     else:
#         df = generate_sample_data()
#         st.sidebar.info("📊 Using AI-generated sample data")

#     # Required columns
#     required_cols = ['date', 'product_id', 'units_sold']
#     missing = [col for col in required_cols if col not in df.columns]

#     if missing:
#         st.error(
#             f"❌ Missing required columns: {', '.join(missing)}\n\n"
#             "Required format: date, product_id, units_sold"
#         )
#         return None

#     # Convert data types safely
#     df['date'] = pd.to_datetime(df['date'], errors='coerce')
#     df = df.dropna(subset=['date'])

#     df['units_sold'] = pd.to_numeric(df['units_sold'], errors='coerce')
#     df['units_sold'] = df['units_sold'].fillna(0)

#     # Sort properly
#     df = df.sort_values(['product_id', 'date']).reset_index(drop=True)

#     return df
