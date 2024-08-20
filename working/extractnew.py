# # 1 stands for legitimate
# # 0 stands for suspicious
# # -1 stands for phishing

# from bs4 import BeautifulSoup
# import urllib, bs4, re
# import socket

# from google import google
# import whois
# from datetime import datetime
# import time


# def having_ip_address(url):
#     match = re.search(
#         '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
#         '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
#         '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
#         '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
#     if match:
#         # print match.group()
#         return -1
#     else:
#         # print 'No matching pattern found'
#         return 1

# def url_length(url):
#     if len(url) < 54:
#         return 1
#     elif len(url) >= 54 | len(url) <= 75:
#         return 0
#     else:
#         return -1

# def https_token(url):
#     match = re.search('https://|http://', url)
#     if match.start(0) == 0:
#         url = url[match.end(0):]
#     match = re.search('http|https', url)
#     if match:
#         return -1
#     else:
#         return 1

# def shortening_service(url):
#     match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
#                       'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
#                       'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
#                       'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
#                       'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
#                       'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
#                       'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
#                       'tr\.im|link\.zip\.net',
#                       url)
#     if match:
#         return -1
#     else:
#         return 1

# def having_at_symbol(url):
#     match = re.search('@', url)
#     if match:
#         return -1
#     else:
#         return 1

# def double_slash_redirecting(url):
#     # since the position starts from, we have given 6 and not 7 which is according to the document
#     list = [x.start(0) for x in re.finditer('//', url)]
#     if list[len(list) - 1] > 6:
#         return -1
#     else:
#         return 1

# def prefix_suffix(domain):
#     match = re.search('-', domain)
#     if match:
#         return -1
#     else:
#         return 1

# def url_of_anchor(wiki, soup, domain):

#     i = 0
#     unsafe = 0
#     for a in soup.find_all('a', href=True):
#         # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and ::
#         # might not be
#         # there in the actual a['href']
#         if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
#                 wiki in a['href'] or domain in a['href']):
#             unsafe = unsafe + 1
#         i = i + 1
#         # print a['href']
#     try:
#         percentage = unsafe / float(i) * 100
#     except:
#         return 1
#     if percentage < 31.0:
#         return 1
#         # return percentage
#     elif 31.0 <= percentage < 67.0:
#         return 0
#     else:
#         return -1

# def favicon(wiki, soup, domain):
#     for head in soup.find_all('head'):
#         for head.link in soup.find_all('link', href=True):
#             dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
#             if wiki in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
#                 return 1
#             else:
#                 return -1
#     return 1


# #Domain
# def google_index(url):
#     site = google.search(url, 5)
#     if site:
#         return 1
#     else:
#         return -1

# def having_sub_domain(url):
#     # Here, instead of greater than 1 we will take greater than 3 since the greater than 1 conition is when www and
#     # country domain dots are skipped
#     # Accordingly other dots will increase by 1
#     if having_ip_address(url) == -1:
#         match = re.search(
#             '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
#             '([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',
#             url)
#         pos = match.end(0)
#         url = url[pos:]
#     list = [x.start(0) for x in re.finditer('\.', url)]
#     if len(list) <= 3:
#         return 1
#     elif len(list) == 4:
#         return 0
#     else:
#         return -1

# def domain_registration_length(domain):
#     expiration_date = domain.expiration_date
#     today = time.strftime('%Y-%m-%d')
#     today = datetime.strptime(today, '%Y-%m-%d')
#     registration_length = abs((expiration_date - today).days)

#     if registration_length / 365 <= 1:
#         return -1
#     else:
#         return 1

# def age_of_domain(domain):
#     creation_date = domain.creation_date
#     expiration_date = domain.expiration_date
#     ageofdomain = abs((expiration_date - creation_date).days)
#     if ageofdomain / 30 < 6:
#         return -1
#     else:
#         return 1


# #Abnormal
# def submitting_to_email(soup):
#     for form in soup.find_all('form', action=True):
#         if "mailto:" in form['action']:
#             return -1
#         else:
#             return 1
#     return 1

# def abnormal_url(domain, url):
#     hostname = domain.name
#     match = re.search(hostname, url)
#     if match:
#         return 1
#     else:
#         return -1


# #Content Based
# def i_frame(soup):
#     for i_frame in soup.find_all('i_frame', width=True, height=True, frameBorder=True):
#         if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameBorder'] == "0":
#             return -1
#         else:
#             return 1
#     return 1

# # Links in <Script> and <Link> tags
# def links_in_tags(wiki, soup, domain):
#     i = 0
#     success = 0
#     for link in soup.find_all('link', href=True):
#         dots = [x.start(0) for x in re.finditer('\.', link['href'])]
#         if wiki in link['href'] or domain in link['href'] or len(dots) == 1:
#             success = success + 1
#         i = i + 1

#     for script in soup.find_all('script', src=True):
#         dots = [x.start(0) for x in re.finditer('\.', script['src'])]
#         if wiki in script['src'] or domain in script['src'] or len(dots) == 1:
#             success = success + 1
#         i = i + 1
#     try:
#         percentage = success / float(i) * 100
#     except:
#         return 1

#     if percentage < 17.0:
#         return 1
#     elif 17.0 <= percentage < 81.0:
#         return 0
#     else:
#         return -1

# # //////////////////////////////////////

# def main(url):
#     # url = sys.argv[1]
#     with open('/opt/lampp/htdocs/BE/markup.txt', 'r') as file:
#         soup_string = file.read()

#     soup = BeautifulSoup(soup_string, 'html.parser')

#     status = []

#     hostname = url
#     h = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
#     z = int(len(h))
#     if z != 0:
#         y = h[0][1]
#         hostname = hostname[y:]
#         h = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
#         z = int(len(h))
#         if z != 0:
#             hostname = hostname[:h[0][0]]

#     status.append(having_ip_address(url))
#     status.append(url_length(url))
#     status.append(shortening_service(url))
#     status.append(having_at_symbol(url))
#     status.append(double_slash_redirecting(url))
#     status.append(prefix_suffix(hostname))
#     status.append(having_sub_domain(url))

#     dns = 1
#     try:
#         domain = whois.query(hostname)
#     except:
#         dns = -1

#     if dns == -1:
#         status.append(-1)
#     else:
#         status.append(domain_registration_length(domain))

#     status.append(favicon(url, soup, hostname))
#     status.append(https_token(url))
#     # status.append(request_url(url, soup, hostname))
#     status.append(url_of_anchor(url, soup, hostname))
#     status.append(links_in_tags(url, soup, hostname))
#     # status.append(sfh(url, soup, hostname))
#     status.append(submitting_to_email(soup))

#     if dns == -1:
#         status.append(-1)
#     else:
#         status.append(abnormal_url(domain, url))

#     status.append(i_frame(soup))

#     if dns == -1:
#         status.append(-1)
#     else:
#         status.append(age_of_domain(domain))

#     status.append(dns)

#     # status.append(web_traffic(soup))
#     # status.append(google_index(url))
#     # status.append(statistical_report(url, hostname))

#     # print('\n1. Having IP address\n2. URL Length\n3. URL Shortening service\n4. Having @ symbol\n'
#     #       '5. Having double slash\n6. Having dash symbol(Prefix Suffix)\n7. Having multiple subdomains\n'
#     #       '8. SSL Final State\n8. Domain Registration Length\n9. Favicon\n10. HTTP or HTTPS token in domain name\n'
#     #       '11. Request URL\n12. URL of Anchor\n13. Links in tags\n14. SFH\n15. Submitting to email\n16. Abnormal URL\n'
#     #       '17. IFrame\n18. Age of Domain\n19. DNS Record\n20. Web Traffic\n21. Google Index\n22. Statistical Reports\n')
#     print(status)
#     return status

# if __name__ == "__main__":
#     main()


from bs4 import BeautifulSoup
import urllib
import re
import socket
import whois
from datetime import datetime
import time
# import google

def having_ip_address(url):
    match = re.search(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
        r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'  # IPv4
        r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'  # IPv4 in hexadecimal
        r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        return 0
    else:
        return 1

def url_length(url):
    if len(url) < 54:
        return 1
    elif len(url) >= 54 | len(url) <= 75:
        return 0
    else:
        return 0

def https_token(url):
    """
    Check if the URL contains the 'https' token in its domain part.
    
    :param url: The URL to analyze.
    :return: 1 if 'https' is found in the domain part, 0 otherwise.
    """
    match = re.search('https://', url)
    if match and match.start(0) == 0:
        return 1
    else:
        return 0

def shortening_service(url):
    match = re.search(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      r'tr\.im|link\.zip\.net',
                      url)
    if match:
        return 0
    else:
        return 1

def having_at_symbol(url):
    match = re.search(r'@', url)
    if match:
        return 0
    else:
        return 1

def double_slash_redirecting(url):
    double_slashes = [x.start(0) for x in re.finditer('//', url)]
    
    if double_slashes and double_slashes[-1] > 6:
        return 0
    else:
        return 1

def prefix_suffix(domain):
    match = re.search(r'-', domain)
    if match:
        return 0
    else:
        return 1

def url_of_anchor(wiki, soup, domain):
    i = 0
    unsafe = 0
    for a in soup.find_all('a', href=True):
        if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (
                wiki in a['href'] or domain in a['href']):
            unsafe = unsafe + 1
        i = i + 1
    try:
        percentage = unsafe / float(i) * 100
    except:
        return 1
    if percentage < 31.0:
        return 1
    elif 31.0 <= percentage < 67.0:
        return 0
    else:
        return 0

def favicon(wiki, soup, domain):
    for head in soup.find_all('head'):
        for head.link in soup.find_all('link', href=True):
            dots = [x.start(0) for x in re.finditer(r'\.', head.link['href'])]
            if wiki in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
                return 1
            else:
                return 0
    return 1

# def google_index(url):
#     site = google.search(url, 5)
#     if site:
#         return 1
#     else:
#         return -1

def having_sub_domain(url):
    if having_ip_address(url) == -1:
        match = re.search(
            r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
            r'([01]?\d\d?|2[0-4]\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}',
            url)
        pos = match.end(0)
        url = url[pos:]
    list = [x.start(0) for x in re.finditer(r'\.', url)]
    if len(list) <= 3:
        return 1
    elif len(list) == 4:
        return 0
    else:
        return 0

def domain_registration_length(domain):
    expiration_date = domain.expiration_date
    today = time.strftime('%Y-%m-%d')
    today = datetime.strptime(today, '%Y-%m-%d')
    registration_length = abs((expiration_date - today).days)

    if registration_length / 365 <= 1:
        return 0
    else:
        return 1

def age_of_domain(domain):
    creation_date = domain.creation_date
    expiration_date = domain.expiration_date
    ageofdomain = abs((expiration_date - creation_date).days)
    if ageofdomain / 30 < 6:
        return 0
    else:
        return 1

def submitting_to_email(soup):
    for form in soup.find_all('form', action=True):
        if "mailto:" in form['action']:
            return 0
        else:
            return 1
    return 1

def abnormal_url(domain, url):
    hostname = domain.name
    match = re.search(hostname, url)
    if match:
        return 1
    else:
        return 0

def i_frame(soup):
    for i_frame in soup.find_all('i_frame', width=True, height=True, frameBorder=True):
        if i_frame['width'] == "0" and i_frame['height'] == "0" and i_frame['frameBorder'] == "0":
            return 0
        else:
            return 1
    return 1

def links_in_tags(wiki, soup, domain):
    i = 0
    success = 0
    for link in soup.find_all('link', href=True):
        dots = [x.start(0) for x in re.finditer(r'\.', link['href'])]
        if wiki in link['href'] or domain in link['href'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for script in soup.find_all('script', src=True):
        dots = [x.start(0) for x in re.finditer(r'\.', script['src'])]
        if wiki in script['src'] or domain in script['src'] or len(dots) == 1:
            success = success + 1
        i = i + 1

    try:
        percentage = success / float(i) * 100
    except:
        return 1

    if percentage < 17.0:
        return 0
    elif 17.0 <= percentage < 81.0:
        return 0
    else:
        return 1

def main(url):
    with open('./markup.txt', 'r') as file:
        soup_string = file.read()

    soup = BeautifulSoup(soup_string, 'html.parser')

    status = []

    hostname = url
    h = [(x.start(0), x.end(0)) for x in re.finditer(r'https://|http://|www.|https://www.|http://www.', hostname)]
    z = int(len(h))
    if z != 0:
        y = h[0][1]
        hostname = hostname[y:]
        h = [(x.start(0), x.end(0)) for x in re.finditer(r'/', hostname)]
        z = int(len(h))
        if z != 0:
            hostname = hostname[:h[0][0]]

    status.append(having_ip_address(url))
    status.append(url_length(url))
    status.append(shortening_service(url))
    status.append(having_at_symbol(url))
    status.append(double_slash_redirecting(url))
    status.append(prefix_suffix(hostname))
    status.append(having_sub_domain(url))

    dns = 1
    try:
        domain = whois.query(hostname)
    except:
        dns = -1

    if dns == -1:
        status.append(-1)
    else:
        status.append(domain_registration_length(domain))

    status.append(favicon(url, soup, hostname))
    status.append(https_token(url))
    status.append(url_of_anchor(url, soup, hostname))
    status.append(links_in_tags(url, soup, hostname))
    status.append(submitting_to_email(soup))

    if dns == -1:
        status.append(-1)
    else:
        status.append(abnormal_url(domain, url))

    status.append(i_frame(soup))

    if dns == -1:
        status.append(-1)
    else:
        status.append(age_of_domain(domain))

    status.append(dns)

    return status

if __name__ == "__main__":
    main()