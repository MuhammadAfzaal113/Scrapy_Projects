import scrapy
from scrapy import Selector
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser
import requests

class RegistrationSearchSpider(scrapy.Spider):
    name = 'registration_search'

    # client = ScraperAPIClient('421190a8f95430feb72dbdecde6c9e29')
    # start_urls = [client.scrapyGet(url='https://search.bpb.nsw.gov.au/PublicRegister/RegistrationSearch.aspx')]
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MicrosoftAjax': 'Delta=true',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Origin': 'https://search.bpb.nsw.gov.au',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://search.bpb.nsw.gov.au/PublicRegister/RegistrationSearch.aspx',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }
    start_urls = ['https://search.bpb.nsw.gov.au/PublicRegister/RegistrationSearch.aspx']

    def parse(self, response):
        self.headers['Cookie'] = response.headers['Set-Cookie'].decode()
        view_state = response.css('#__VIEWSTATE::attr(value)').get()
        view_state_gen = response.css('#__VIEWSTATEGENERATOR::attr(value)').get()


        url = "https://search.bpb.nsw.gov.au/PublicRegister/RegistrationSearch.aspx"
        payload = "ctl00%24ctl00%24ScriptManager1=ctl00%24ctl00%24main%24MainArea%24ctl01%7Cctl00%24ctl00%24main" \
                  "%24MainArea%24RefineSearchSection%24ctl17&__EVENTTARGET=ctl00%24ctl00%24main%24MainArea" \
                  "%24RefineSearchSection%24ctl17&__EVENTARGUMENT=&__VIEWSTATE=yGVtXTMV5bj5J4kzp1FX5koXuPF" \
                  "%2BqFBK6NUfKrnJlaGjMBCDwsWIf%2Fu88DvFW7c9Za4wnxZlIVq5Q73hsoRc36Z9BMbcKiOe" \
                  "%2Bg6w9bh9zRvliKs8kYq7DCgmDkzmIYokTqPsmBMq7ucfwsllNX%2Fs049sjbSat21IHfgP96etlXF6NXRrqfAMT92ycEuMD" \
                  "%2FEozBSJV3jd9cMhZ%2Bmi5z9CSumpwMnRjtVVNT4gKSU4LK5yEuaigLn%2BlA1ZkOl" \
                  "%2F1rdQidIL0YVEMcODy8xPpro1iuoHQ2I1XzQMZ54FzMAwXeqt6NZiP%2BVYy7jW%2Bdcic1%2BnwU" \
                  "%2FGTnCsuhfpQ3ShelnvniRgfV70k3h5BtDwReMm1UGSZZIYatiRf1oWxOi0ELA6PqUHDi" \
                  "%2BDKc2GC5Cztcxuoy3EENutS9iXkDJcNmj" \
                  "%2FHNwtWlezcrIQNInIwpTaAzZqRHgtysn2YuIj1qDCk9ioReWC1mAoy7ojz85Jyq5H4wUJF53j2A5ES1DkAfQQGUyDQNKcSz28eacp5zzy0Rm2Nk8kth49J1BIAWFDBaI5TWyMyBGotpviPwR%2F9cR0HI92SwUJFgotBtSqadb6WJeTxCqQieKW3hUDiFYY0Zp5KKcXvL%2FUDqAll45v9GKFwkuNWnSuaSumM0Ppwbwy2DumczDr9RSmeT5e3Q3ObNONLMraC9UypbtvYQ0NOKuuqcIGDlwgUzPZEG0Gtewt4ZUP0RedAC5Ay3Q2NrWDFEM%2BxB%2FlXtZ%2Fut6ZjQFf6YbP1mKUY%2BN%2BdzRx2xM2NGzg9lE0X46Erozk%2FTzSXpT0Yp%2BG5SqGc685FQUmZJXcx6Ire92Sx%2FM2hLglIux%2F8d7WavLPyrQ6Oapcrnjm4WKt0l9MKUIv4iOdu7OHKYdqJ7AJG9wOf1a6dFO3LLDK2sk5pvZHJXXlbOpzU4HZQar0pSYwsT3qaBuA0HNzVh2bfhK7prabOHTUG0fmb282XG4IYZIZwqAOY%2BtabPmaHv%2B0wzuIEc2UaF31pokopRkEdfctrhjS9SQ5HOa3%2FRxvxC7h0GdjPkT66A98sBGA%2Fky%2Bt2WlZJW7i%2Bf7V3g2iLYmyL8nmjPjDpeu2FZItw8tvpwDBN42VBk7gu%2BuAoKhLlqyHU4%2BjW12l7bc2XoGr3ZoPoHCI1dq1UGpAzOqvpVEbsnrMLXPmGjGlbl5%2Buv7nGccWwXsCNqTb7zsnI%2BFZTBKph845vU0eTHzwUqfHCga%2FW1tiUuVf83ueDZbk5BQewP5C3G6N%2Fe%2BaO0t3E6suS2%2FbIxo2Bx20O39RqhDJw5oSOgukldIkfYeGXwlBs4sr0%2B3ALE6LWdcR%2BWbYtgy03elmvzxXtMNQ%2FL8FX1pwej4JyVBjeuw0zRhevgI6b27HRGj%2FJqjiYME76Rc7a9Wj82XEgrfOeRmXyFc1ip1Ia%2F%2FHBB3hcc9jqo8JVi1yBxZgXgiPNyABi5f0cHg7VIR3m4GIaN4RFBoIJY6peQCPoGXcE1dtJmaGF9%2Fqxn24VgFF2LijMIOwzdJh4pCVW9QyLTHuiAm%2B3MZydkAIodKVAbLMabhjgngnYhrKiSkH4Nx5hW7mrP%2BY9cQGsktUFFENsQI%2Fy4NbuoBz4%2FecxEFQeSPdGLZOoFDVaK4Z0gEFQ8h4Tc5PWUhQFMU6gWAM6Z%2BIeTZr1YT0ib3%2FmY5DSTd85vTftmvW2rJNy3jdU12sxWLy0sW7q4iiLccJFNuK2BsHyaB1JuT2qwKPT69gu4B%2BxYrBVm4hO%2F11yQweZ%2BmgwOxxyBU1FhH2xXkjkIil0DVPuXZDAOi5CD76zwu1dPZJNZAA9mPXrRGFanwHmJiZiGzNtGDdiitY9x5%2FJKNaxrv%2BobFnzuTZd2vTT%2FQpNyocAZ8XsykY%2B7PQd%2BEsmCXSZ2%2B9zDEX7x5blDYrrImMzEwV5l%2FLXfrWQ6fxn%2BN83ZjFyG8uif1qLYSlXs3jpCgHzFgSUBh66ixcNBPPfDTqHiIvzmR5lywUwCoAVnw40e7U1TLtwWeTFvAvE%2FUOzajTgCFkVO8IgYKUEj8PfqMrtPSqGGtmDlQUizWMm3lNQWPVSFvvcGIUMHkFASciRdh1S%2Bny%2BhNudRJQ%2FodpSGy%2B6FIPqnPqwX5ZtQkCApPGnhIUmLWtzi3S3LRDnogWoLjAFBXHQYCANtXE4wEBBfCRBRXsO4fp8j3CIu2BBXrj7Klqj5sUHtjCa00nCFU0%2BWxhbZWFe7At25lUUGFKzEAGxLYYTBcUw3e01QCU76GMDpyy4LxnwZ3GgNkuQ%3D%3D&__VIEWSTATEGENERATOR={}&__SCROLLPOSITIONX=0&__SCROLLPOSITIONY=0&__VIEWSTATEENCRYPTED=&__PREVIOUSPAGE=1x1IjZ4Wp_mK-mymJrNxsbcVHMwZxCpq8gy-zLuWWH7-uyKKLF2Gt4m-rzbZOFvpZZywaPY3KFiDpuTPrJAO0INw7uAgCxsn8PG6Cg710zsubORmiIjIGsmyJnZltaup0&ctl00%24ctl00%24main%24MainArea%24SimpleSearchSection%24Keyword={}&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Registrationnumber=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Dateregisteredfrom=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Dateregisteredto=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Dateceasedfrom=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Dateceasedto=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Certifiername=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Organisation=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Suburb=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24State=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24Postcode=&ctl00%24ctl00%24main%24MainArea%24AdvancedSearchSection%24ClassesOfRegistration=&ctl00_ctl00_main_MainArea_AdvancedSearchSection_ClassesOfRegistration_ClientState=&ctl00%24ctl00%24main%24MainArea%24ctl03%24Ref_Keyword=a&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Certifiertype=INDIVIDUAL&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Registrationnumber=&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Certifiername=&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Organisation=&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Registrationstatus=005&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Suburb=&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_State=&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Postcode=&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_RegistrationClass%241=on&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_RegistrationClass%242=on&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_RegistrationClass%243=on&ctl00%24ctl00%24main%24MainArea%24RefineSearchSection%24Ref_Sortby=&hiddenInputToUpdateATBuffer_CommonToolkitScripts=1&__ASYNCPOST=true& "
        payload = payload.format(view_state_gen, 'a')
        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'X-MicrosoftAjax': 'Delta=true',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'Origin': 'https://search.bpb.nsw.gov.au',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://search.bpb.nsw.gov.au/PublicRegister/RegistrationSearch.aspx',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            '__VIEWSTATE' : view_state,
            'Cookie': 'NSW BC portal session cookie=bhcpcwvex2abymk33x2f1vys'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        self.parse_form(response.url)
        Sel = Selector(text=response.text)
        # view = Sel.css('')
        # self.start_scraping(Sel)

    def parse_form(self, response):

        for i in range(97 , 123):
            keyword = chr(i)
            view_state = response.css('#__VIEWSTATE::attr(value)').get()

            yield FormRequest(response.url ,callback = self.start_scraping,  formdata={

                'ctl00$ctl00$ScriptManager1' : 'ctl00$ctl00$main$MainArea$ctl01 | ctl00$ctl00$main$MainArea$ctl03$RefineSearchButton',
                '__EVENTTARGET': 'ctl00$ctl00$main$MainArea$ctl03$RefineSearchButton',
                '__VIEWSTATE': view_state,
                '__VIEWSTATEGENERATOR': '56F2A902',
                'ctl00$ctl00$main$MainArea$ctl03$Ref_Keyword': keyword,
                'ctl00$ctl00$main$MainArea$RefineSearchSection$Ref_Certifiertype': 'INDIVIDUAL',
                'ctl00$ctl00$main$MainArea$RefineSearchSection$Ref_Registrationstatus': '005',
                'ctl00$ctl00$main$MainArea$RefineSearchSection$Ref_RegistrationClass$1': 'on',
                'ctl00$ctl00$main$MainArea$RefineSearchSection$Ref_RegistrationClass$2': 'on',
                'ctl00$ctl00$main$MainArea$RefineSearchSection$Ref_RegistrationClass$3': 'on',
            }, method='POST' )

    def start_scraping(self, response):
        open_in_browser(response)
        for row in response.css('div'):
            item = {
                'Certifier_name' : self.clean(row.css('.font-weight-bold a::text').get()),
                'Reg_number' : self.clean(row.css('.col-md-6').css('::text').get()),
                'Reg_period_from' : self.clean(row.css('.font-weight-bold~ .col-md-6+ .col-md-6').css('::text').get()), # self.get_period_from(row),
                'Reg_period_to' : self.clean(row.css('.font-weight-bold~ .col-md-6+ .col-md-6').css('::text').get()), # self.get_period_to(row),
                'Reg_class' : self.clean(row.css('.text-secondary > .col-md-6+ .col-md-12').css('::text').get()),
                'Organization_name' : self.clean(row.css('#ctl00_ctl00_main_MainArea_ResultDataList .data-list .col-md-12:nth-child(1)').css('::text').get()),
                'Business_address' : '',
                'Postal_address' : '',
                'Tel_no' : self.clean(row.css('#ctl00_ctl00_main_MainArea_ResultDataList .data-list .col-md-12+ .col-md-6').css('::text').get()),
                'Mobile_no' : self.clean(row.css('#ctl00_ctl00_main_MainArea_ResultDataList .data-list .col-md-6+ .col-md-6').css('::text').get()),
                'Email_address' : self.clean(row.css('#ctl00_ctl00_main_MainArea_ResultDataList .data-list .col-md-6+ .col-md-12').css('::text').get()),
                'Condition' : '',
                'Insurance_details' : self.clean(row.css('#ctl00_ctl00_main_MainArea_ResultDataList .col-md-12:nth-child(5)').css('::text').get())
            }
            print(item)


    def clean(self,text):
        return (text or '').replace('"', "").replace('\n', ' ').replace('\r', ' ') \
            .replace('\xa0', ' ').replace('\t', '').replace('\xad', '-').strip()
