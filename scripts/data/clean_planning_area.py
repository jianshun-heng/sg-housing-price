from bs4 import BeautifulSoup

def format_geojson_planning_area(gdf):
    # Define a function to extract header cells and data cells from an HTML string
    def extract_cells_from_html(html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        rows_of_interest = soup.find_all('tr', bgcolor=["#E3E3F3", ""])
        th_elements = []
        td_elements = []
        for row in rows_of_interest:
            th_elements.extend(row.find_all('th'))
            td_elements.extend(row.find_all('td'))
        th_content = [th.get_text(strip=True) for th in th_elements]  # Header cells
        td_content = [td.get_text(strip=True) for td in td_elements]  # Data cells
        info_dict = dict(zip(th_content, td_content))
        return info_dict

    # Apply the extraction function to the 'Description' column
    gdf['Extracted_Data'] = gdf['Description'].apply(extract_cells_from_html)

    # Create new columns for each key-value pair in the dictionary
    for key in gdf['Extracted_Data'][0].keys():
        gdf[key] = gdf['Extracted_Data'].apply(lambda x: x.get(key))

    # # Drop the original 'Description' and 'Extracted_Data' columns if not needed
    gdf = gdf.drop(columns=['Description', 'Extracted_Data'])
    
    return gdf