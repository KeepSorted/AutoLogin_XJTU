import requests
import json

class AutoLoginXJTU:
  def __init__(self, config):
    if 'username' in config and 'password' in config:  # 检查参数
      self.url = 'http://10.6.8.2:901/include/auth_action.php' # 校园网登录地址
      self.username = config['username']
      self.password = config['password']
      self.headers = {  #模拟请求头
        'Host': '10.6.8.2:901',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Origin': 'http://10.6.8.2:901',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://10.6.8.2:901/srun_portal_pc.php?ac_id=1&',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
      }
    else:
      raise NameError
  
  # 检查是否在线
  def isOnline(self):
    url = 'http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp'  #时间检查api，获得当前时间
    try:
      res = requests.get(url, timeout = 10).text 
    except:
      print('Something wrong happened when check network status!')
      return False
    else:
      if 'data' in res:  # 如果返回结果中有时间，说明在线
        print('you are online!')
        return True
      else:
        print('you are offline!') #否则不在线
        return False
  
  # 登录
  def login(self):
    payload = { #负载，包含用户名密码
      'action': 'login',
      'username': self.username,
      'password': self.password,
      'ac_id': '1',
      'user_ip': '',
      'nas_ip': '',
      'user_mac': '',
      'save_me': 0,
      'ajax': 1
    }
    try:
      print('try to login...')
      r = requests.post(self.url, headers = self.headers, data = payload)  #尝试登录
    except:
      print('Error occour when login!')
      return False
    else:
      if r.status_code == 200:
        response = r.text
        if response.split(',')[0] == 'login_ok': # 验证登录服务器返回结果
          print('login successfull!')
          print(response)
          with open('cookie', 'w') as cookieFile: # 存储cookie
            cookieFile.write(response)
          return True
        else:
          print('login failed!')
          return False
      else:
        print('login failed!')
        return False

  #自动登录
  def autoLogin(self):
    res = self.isOnline()
    if not res: #如果不在线
      self.login()

  #注销
  def logout(self):
    headers = self.headers
    try:
      with open('cookie', 'r') as cookieFile:
        code = cookieFile.readline().split(',')
        cookie = 'login=' + code[1] + '; double_stack_login=' + code[2] + '; login=' + code[1]
        headers['Cookie'] = cookie
    except:
      print('open cookie file failed!')

    payload = { #负载，包含用户名密码
      'action': 'logout',
      'username': self.username,
      'password': self.password,
      'ajax': 1
    }

    try: # 尝试登录
      print('try to logout...')
      print(headers)
      r = requests.post(self.url, headers = headers, data = payload)  #尝试登录
    except: # 登录失败
      print('Logout failed! Something wrong happend')
      return False
    else: 
      if r.status_code == 200:
        response = r.text.encode('UTF-8').decode('UTF-8')
        print('logout successfull!')
        print(response)
        return True
      else:
        print('logout failed!')
        return False

def main():
  with open('config.json', 'r') as infile: # 打开配置文件
    config = infile.read() 
    config = json.loads(config)

    autoLogin = AutoLoginXJTU(config = config) # 初始化配置
    autoLogin.autoLogin()  # 自动登录
    # autoLogin.logout() # 注销

if __name__ == '__main__':
  main()