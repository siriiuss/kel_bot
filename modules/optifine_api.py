import requests
from bs4 import BeautifulSoup
import re

def optifine_downloads():
    url = "https://optifine.net/downloads"

    html_content = requests.get(url).content

    # BeautifulSoup ile içeriği işle
    soup = BeautifulSoup(html_content, 'html.parser')

    # class'ı "colMirror" olan etiketlerin içeriğini al
    mirror_tags = soup.find_all('td', class_='colMirror')
    mirror_contents = [tag.get_text() for tag in mirror_tags]

    # class'ı "colFile" olan etiketlerin içeriğini al
    file_tags = soup.find_all('td', class_='colFile')
    file_contents = [tag.get_text() for tag in file_tags]

    # Sonuçları göster
    href_list = []
    for tag in mirror_tags:
        a_tag = tag.find('a')
        if a_tag:
            href = a_tag['href']
            href_list.append(href)

    file_version = []
    for href in href_list:
        # Düzenli ifade kullanarak "1.20.1" veya "1.20" gibi kısmı al
        version_match = re.search(r'OptiFine_(.*?)_HD', href)
        if version_match:
            version = version_match.group(1)
            file_version.append(version)

    # file_contents ve file_version listelerini aynı uzunlukta olacak şekilde birleştir
    max_length = max(len(file_contents), len(file_version))
    file_contents.extend([None] * (max_length - len(file_contents)))
    file_version.extend([None] * (max_length - len(file_version)))
    content = list(zip(href_list, file_contents, file_version))
    return content
