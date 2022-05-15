import requests
import sys
import re
import urllib.parse as up
def request(url):
    if not url.startswith("http"):
        url="http://"+url
    try:
        return requests.get(url=url)
    except requests.exceptions.ConnectionError:
        pass
def get_subdomains(url):
    get_subdomains=[]
    with open("subdomains.list","r") as file:
        for line in file:
            get_subdomains.append(line.strip()+"."+url)
    subdomains=[]
    count=1
    for subdomain in get_subdomains:
        print(f"\r>> Finding subdomains, please wait... | Scanned {count}/{len(get_subdomains)}" ,end="")
        sys.stdout.flush()
        get_response=request(subdomain)
        count+=1
        if get_response:
            subdomains.append(subdomain)
    return subdomains
def extract_link_from(url):
    if not url.startswith("http"):
        url="https://"+url
    try:
        response=requests.get(url=url)
        return re.findall('(?:href=")(.*?)"',str(response.content))
    except requests.ConnectionError:
        pass
def crawl(url):
    href_links=extract_link_from(url=url)
    if href_links is not None:
        for link in href_links:
            link=up.urljoin(url,link)
            if "#" in link:
                link=link.split("#")[0]
            if url in link and link not in target_links:
                target_links.append(link)
                print(link)
                crawl(link)
if __name__=="__main__":
    url="http://10.5.23.250/mutillidae/"
    target_links=[]
    subdomains=get_subdomains(url=url)
    subdomains.append(url)
    print("\n","-"*40)
    print(f"[+] Found {len(subdomains)} in {url}" )
    print("-"*40,"\n")
    for subdomain in subdomains:
        print(f"[+] Discovered Sub-domain -->\t{subdomain}")
    for subdomain in subdomains:
        print(f"[+] Crawling.. {subdomain}")
        crawl(subdomain)
        print("\n\n","#"*30,"\n")
    print(f"[+] Found {len(target_links)} directories in {url}")
    
    """
    
    """

    