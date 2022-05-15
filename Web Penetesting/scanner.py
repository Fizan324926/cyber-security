import requests
import re
import urllib.parse as up
from bs4 import BeautifulSoup
class Scanner:
    def __init__(self,url,links_to_ignore):
        self.target_url=url
        self.target_links=[]
        self.session=requests.Session()
        self.ignore_links=links_to_ignore
    def extract_links_from(self,url):
        if not url.startswith("http"):
            url="https://"+url
        try:
            response=self.session.get(url)
            return re.findall('(?:href=")(.*?)"',str(response.content))
        except requests.ConnectionError:
            pass
    def crawl(self,url=None):
        if url==None:
            url=self.target_url
        href_links=self.extract_links_from(url)
        if href_links is not None:
            for link in href_links:
                link=up.urljoin(url,link)
                if "#" in link:
                    link=link.split("#")[0]
                if self.target_url in link and link not in self.target_links and  link not in self.ignore_links:
                    self.target_links.append(link)
                    print(link)
                    self.crawl(link)
    def extract_forms(self,url):
        response=self.session.get(url=url)
        soup=BeautifulSoup(response.content,"html.parser")
        return soup.find_all("form")
    def submit_form(self,form,value,url):
        action=form.get("action")
        post_url=up.urljoin(url,action)
        method=form.get("method")
        input_list=form.find_all("input")
        post_data={}
        for input in input_list:
            input_name=input.get("name")
            input_type=input.get("type")
            input_value=input.get("value")
            if input_type=="text":
                input_value=value
            post_data[input_name]=input_value
        if method=="post":
            return self.session.post(post_url,data=post_data)
        return self.session.get(post_url,params=post_data)
    def test_xss_in_form(self,form,url):
        payloads=["<script>alert('XSS')</script>"]
        vulnerabilities={}
        xss_vuln=[]
        for paylaod in payloads:
            response=self.submit_form(form,paylaod,url)
            if paylaod in response.content:
                vulnerabilities["Form"]=form
                vulnerabilities["Payload"]=paylaod
                xss_vuln.append(vulnerabilities)
        if xss_vuln is not None:
            return xss_vuln
    def test_xss_in_link(self,url):
        payloads=["<script>alert('XSS')</script>"]
        vulnerabilities={}
        xss_vuln=[]
        for paylaod in payloads:
            url=url.replace("=","="+paylaod)
            response=self.session.get(url=url)
            if paylaod in response.content:
                vulnerabilities["Form"]=url
                vulnerabilities["Payload"]=paylaod
                xss_vuln.append(vulnerabilities)
        if xss_vuln is not None:
            return xss_vuln
                
    def run_scanner(self):
        for link in self.target_links:
            forms=self.extract_forms(link)
            for form in forms:
                print(f"[+] Testing form in {link}")
                is_vulnerable_to_xss=self.test_xss_in_form(form,link)
                if is_vulnerable_to_xss:
                    print(f"[+] XSS discovered in {link} in form: \n{form}\n")
            if "=" in link:
                print(f"[+] Testing {link}")
                is_vulnerable_to_xss=self.test_xss_in_link(link)
                if is_vulnerable_to_xss:
                    print(f"[+] XSS discovered in {link} \n")