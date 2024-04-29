import streamlit as st
import pandas as pd
from urllib.parse import urlparse
import base64

def parse_urls(data):
    # This function parses URLs and returns a DataFrame with the URL components
    components = ['Scheme', 'Netloc', 'Path', 'Query', 'Fragment']
    rows = []

    for url in data:
        parsed_url = urlparse(url)
        rows.append([parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.query, parsed_url.fragment])

    return pd.DataFrame(rows, columns=components)

def download_link(object_to_download, download_filename, download_link_text):
    # Generates a link to download the given object stored in a DataFrame
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

def main():
    st.title('URL Structure Analyzer')

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        # Display column headers to user for selection
        if data.columns.size > 0:
            selected_columns = st.multiselect('Select the column(s) that contain URLs:', data.columns)
            
            if selected_columns:
                url_data = pd.Series(data[selected_columns].values.ravel('K')).dropna().unique()
                parsed_data = parse_urls(url_data)
                st.write(parsed_data)
                
                # Link to download the parsed URL data
                tmp_download_link = download_link(parsed_data, 'parsed_urls.csv', 'Download parsed URL data')
                st.markdown(tmp_download_link, unsafe_allow_html=True)
            else:
                st.info('Please select at least one column containing URLs.')
        else:
            st.error('The uploaded CSV does not contain any columns.')

if __name__ == "__main__":
    main()
