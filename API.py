import streamlit as st
import requests

def extract_citations(item):
    d = {'id': item['id'], 'links': item['link']}
    return d

def fetch_data_from_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = []
        if 'data' not in data or not isinstance(data['data'], dict) or 'data' not in data['data']:
            raise ValueError("Invalid data format received from the API")

        items = data['data']['data']
        for item in items:
            if not isinstance(item, dict):
                continue

            sources = item.get('source', [])
            citations = []
            for source in sources:
                citations.append(extract_citations(source))
            results.append({
                'citations': citations
            })

        return results

    except requests.RequestException as e:
        st.error(f"An error occurred while fetching the data: {e}")
        return None
    except ValueError as e:
        st.error(e)
        return None

# Streamlit UI components
st.title("API Data Fetcher")
api_url = st.text_input("Enter API URL:")
fetch_button = st.button("Fetch Data")

# Fetch data when button is clicked
if fetch_button:
    if api_url:
        citations = fetch_data_from_api(api_url)
        if citations:
            st.write("Citations from API:")
            for item in citations:
                st.write(item['citations'])
    else:
        st.warning("Please enter an API URL.")