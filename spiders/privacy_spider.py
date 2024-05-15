import scrapy
import hashlib
import json
from datetime import datetime

class PrivacySpider(scrapy.Spider):
        name = "privaseer"
        def start_requests(self):
                self.state['items_count'] = self.state.get('items_count', 369)
                with open('/data/privseer/third-crawl/urls_to_crawl2', 'r', encoding='utf-8') as f:
                        urls = f.readlines()
                for u in urls:
                        yield scrapy.Request(u.strip(), callback=self.parse, errback=self.errback_custom)

        def parse(self, response):
                language = ''
                modified = ''
                request_url = ''
                request = response.request
                if request:
                        request_url = request.url
                filename = hashlib.sha1(response.url.encode()).hexdigest()
                if 'html' in response.headers.get('Content-Type').decode('utf-8'):
                        self.state['items_count'] = self.state.get('items_count') + 1
                        folder_number = self.state.get('items_count') // 10000
                        with open('urls/'+str(folder_number)+'/'+filename+'.html', 'w', encoding='utf-8') as f:
                                f.write(response.text)
                        with open('success', 'a', encoding='utf-8') as f:
                                f.write(json.dumps({'hash':filename, 'response':response.url, 'request':request_url, 'folder_number':str(folder_number), 'timestamp':str(datetime.now())})+'\n')
#                except AttributeError:
#                        if 'pdf' in response.headers.get('Content-Type').decode('utf-8'):
#                                with open('urls/'+filename+'.pdf', 'wb') as f:
#                                        f.write(response.body)
#                                with open('success', 'a', encoding='utf-8') as f:
#                                        f.write(json.dumps({'code':filename, 'response':response.url, 'request':request_url, 'language':language, 'modified':modified})+'\n')

        def errback_custom(self, failure):
                status = ''
                if hasattr(failure.value, 'response'):
                        if hasattr(failure.value.response, 'status'):
                                status = failure.value.response.status
                with open('errors', 'a') as f:
                        f.write(str(failure.type)+' || '+str(status)+' || '+str(failure.request.url)+'\n')

