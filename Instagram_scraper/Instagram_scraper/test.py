import urllib.parse
from urllib.parse import urlencode
f = {"id":"19700668658","include_reel":True,"fetch_mutual":True,"first":18,"after":"QVFBN09MSXVaeTAwUVF3bHR4YURJV2FKMXNIWlFaUmM1ZUVqNUtyaWNlZ2dDYlBveEhDUl9peXdTRkFZb0FQMnJhcV9DU082SFMtaC1mWWtURHhuSjVvLQ=="}
url = urlencode(f)
end = "https://z-p3.www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables=" + url
query = 'Hellö Wörld@Python'

after = "24%7Dafter"+"QVFDZnhSUDdnU0hVbjVpYUx2QV9rbURKOUpQdTNLRlU5bUNqTlFoa3gwZzlGNnlrLVk0eEY2M0VOUldieGRXa3d6d192blZsZzFETmVMWnF3Vk1ueFRKVw=="
ab = 'https://z-p3.www.instagram.com/graphql/query/?query_hash=c76146de99bb02f6415203be841dd25a&variables={"id":"19700668658","include_reel":true,"fetch_mutual":true,"first":18,"after":"QVFBN09MSXVaeTAwUVF3bHR4YURJV2FKMXNIWlFaUmM1ZUVqNUtyaWNlZ2dDYlBveEhDUl9peXdTRkFZb0FQMnJhcV9DU082SFMtaC1mWWtURHhuSjVvLQ=="}'
# url = urllib.parse.quote(ab)
strin = "QVFBN09MSXVaeTAwUVF3bHR4YURJV2FKMXNIWlFaUmM1ZUVqNUtyaWNlZ2dDYlBveEhDUl9peXdTRkFZb0FQMnJhcV9DU082SFMtaC1mWWtURHhuSjVvLQ=="
strin = strin[:-2]
a = urllib.parse.unquote(url)
# print(url)
print(strin)