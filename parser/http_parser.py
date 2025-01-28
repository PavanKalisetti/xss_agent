def parse_http_response(response_text):
    """Extract input points from raw HTTP response"""
    soup = BeautifulSoup(response_text, 'html.parser')
    input_points = []

    # Analyze forms
    for form in soup.find_all('form'):
        input_points.append({
            'type': 'form',
            'action': form.get('action'),
            'method': form.get('method', 'GET'),
            'inputs': [input.get('name') for input in form.find_all('input')]
        })

    # Analyze URL parameters
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '?' in href:
            params = href.split('?')[1].split('&')
            input_points.append({
                'type': 'url_param',
                'params': params
            })

    return input_points