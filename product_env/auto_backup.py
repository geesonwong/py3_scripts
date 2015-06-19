from datetime import datetime
import os
import time

__author__ = 'Gson'
__date__ = '06-15-2015 15:10'


def main():
    os.system('tar -czf ~/backups/popping/sources/' + datetime.now().strftime('%Y%m%d') + '-' + str(int(time.time())) + '.gz' + ' /var/www')
    for name in os.popen('ls -t ~/backups/popping/sources/').read().split()[15:]:
        os.system('rm ~/backups/popping/sources/' + name)

    os.system('mysqldump -u pop -p3PmYTV3d2DEeQdJs wordpress > ~/backups/popping/datas' + datetime.now().strftime('%Y%m%d') + '-' + str(int(time.time())) + '.sql')
    for name in os.popen('ls -t ~/backups/popping/datas').read().split()[15:]:
        os.system('rm ~/backups/popping/datas/' + name)

if __name__ == "__main__":
    main()
