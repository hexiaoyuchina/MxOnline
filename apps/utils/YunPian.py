import requests
import json
def send_single_sms(apikey,code,mobile):
    #发送短信
    url='云片网中的端口'
    text='模板中的信息内容您的验证码是{}'.format(code)
    # res=requests.post(url,data={
    #     'apikey':apikey,
    #     'mobile':mobile,
    #     'text':text
    # })
    # res_json=json.loads(res.text)
    return {'code':0,'msg':'success'}
if __name__ == '__main__':
    res=send_single_sms(x,y,z)
    import json
    res_json=json.load(res.text)
    code=res_json['code']
    msg=res_json['msg']
    if code==0:
        print('发送成功')
    else:
        print('发送失败{}'.format(msg))
    res.text


