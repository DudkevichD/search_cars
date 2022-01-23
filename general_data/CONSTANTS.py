import datetime

from fake_useragent import UserAgent

date = datetime.datetime.now().strftime('%d%m%Y')
USER = UserAgent().random
HEADERS = {'user-agent': USER}
