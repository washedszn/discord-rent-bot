import requests
import json
from bs4 import BeautifulSoup

# Load config
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
CITY = config['CITY']

def nederwoon(html_content=None):
    # Dev testing so we dont spam requests on site
    with open("raw_html.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    url = f"https://www.nederwoon.nl/search?city={CITY}"

    if (html_content is None):
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text
    
    # Saving the raw HTML content to a file
    with open("raw_html.html", "w", encoding="utf-8") as html_file:
        html_file.write(html_content)

    soup = BeautifulSoup(html_content, 'html.parser')
    properties = soup.select('div.location')
    
    all_properties_data = []

    for prop in properties:
        # Extract property URL
        property_url = 'https://www.nederwoon.nl' + prop.select_one('a.see-page-button')['href']

        # Extracting images' URLs
        images_div = prop.select_one(".slider.slider-overview")
        images = ["https://www.nederwoon.nl" + img["data-src"] for img in images_div.select("img[data-src]")] if images_div else []
        
        # Extracting property title
        title = prop.select_one('h2.heading-sm a').text.strip()
        
        # Extracting address
        address = prop.select_one('p.color-medium.fixed-lh').text.strip()
        
        # Extracting property type and build status
        property_type_build = prop.select_one('p.color-primary.fixed-lh').text.strip().split('|')
        property_type = property_type_build[0].strip()
        build_status = property_type_build[1].strip() if len(property_type_build) > 1 else None
        
        # Extracting property details
        #property_details = [li.text.strip() for li in prop.select('ul li')]
        
        # Extracting viewing status
        #viewing_status = prop.select_one('p.color-tertiary.text-bold').text.strip()
        
        # Extracting price
        price = prop.select_one('p.heading-md.text-regular.color-primary').text.strip()
        
        # Extracting additional details
        additional_details = prop.select_one('p.color-primary.body-sm.text-bold').text.strip()
        
        data = {
            'url': property_url,
            'images': images,
            'title': title,
            'address': address,
            'property_type': property_type,
            'build_status': build_status,
            #'property_details': property_details,
            #'viewing_status': viewing_status,
            'price': price,
            #'additional_details': additional_details
        }
        
        all_properties_data.append(data)
    
    # JSON dump for testing
    with open("properties.json", "w") as outfile:
        json.dump(all_properties_data, outfile, indent=4)

    return all_properties_data