# coding:UTF-8
from app import app,sniff_p

WELCOME_MSG = '''
  __  __ _       _        _____                           
 |  \/  (_)     (_)      / ____|                          
 | \  / |_ _ __  _ _ __ | |  __  _____   _____ _ __ _ __  
 | |\/| | | '_ \| | '_ \| | |_ |/ _ \ \ / / _ \ '__| '_ \ 
 | |  | | | | | | | | | | |__| | (_) \ V /  __/ |  | | | |
 |_|  |_|_|_| |_|_|_| |_|\_____|\___/ \_/ \___|_|  |_| |_|
                                                          
'''

HAVEN_NO_SNIFF = False
if __name__ == '__main__':
    print(WELCOME_MSG)
    if HAVEN_NO_SNIFF:
        sniff_p.start()
    app.run(host='0.0.0.0', port=8081, use_reloader=False, debug=False)
