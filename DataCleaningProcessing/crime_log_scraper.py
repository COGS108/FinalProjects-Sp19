# Need to fix - do not use
from urllib.request import urlretrieve

link_list = []

for i in range(1, 32):
    try:
        link_list.append('http://www.police.ucsd.edu/docs/reports'\
                '/CallsandArrests/CallsForService/April%20'\
                + str(i) + ',%202018.pdf')
    except:
        link_list.append('http://www.police.ucsd.edu/docs/reports'\
                '/CallsandArrests/CallsForService/April%20'\
                + str(i) + ',%202018%20UPDATED.pdf')
    else:
        continue
for i in range(1, len(link_list)):
    urlretrieve(link_list[i], 'April ' + str(i) + ', 2018')

