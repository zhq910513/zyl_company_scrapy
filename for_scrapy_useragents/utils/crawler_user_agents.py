import requests
import json
from scrapy.selector import Selector


def main():
    resp = requests.get(
       'https://developers.whatismybrowser.com/useragents/'
       'explore/hardware_type_specific/computer/'
    )
    resp = Selector(text=resp.content.decode())
    user_agents = []
    for tr in resp.css('tbody tr'):
        user_agents.append({
            'user_agent': tr.css('td')[0].css('a ::text').extract_first(),
            'type': tr.css('td')[1].css('::text').extract_first(),
            'device': 'web'
        })
    with open('user_agents.json', 'w') as f:
        f.write(json.dumps(user_agents))


if __name__ == '__main__':
    main()
