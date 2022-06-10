#coding:UTF-8

from app import app,sniff_p
# sniff 进程


HAVEN_NO_SNIFF = False
if __name__ == '__main__':
    if HAVEN_NO_SNIFF:
        sniff_p.start()
    app.run(host='0.0.0.0', port=8081)
