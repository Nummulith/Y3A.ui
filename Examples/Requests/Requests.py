def Test2(aws, param):
    url = "http://18.192.62.22/"
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        print(html_content)
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

