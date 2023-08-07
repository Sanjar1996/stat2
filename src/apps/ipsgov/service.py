import base64
import json

import xmltodict as xmltodict
from pip._vendor import requests
from rest_framework.response import Response
from rest_framework import status


def get_iskm_egov_token():
    usr_pass = b"hNhNfVqHrHQrDRS5If7evEZAQcYa:yVfzNbEruUkOfOXxFibL8UPZuP4a"
    b64_val = base64.b64encode(usr_pass)

    url = "https://iskm.egov.uz:9444/oauth2/token?grant_type=password&username=goskomles-user2&password" \
          "=BsmpOkp7lQzdmu8UL2EO "

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic %s' % b64_val.decode("utf-8")
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(b64_val.decode("utf-8"))
    print(response.text)
    data = json.loads(response.text)
    if 'access_token' in data:
        return data['access_token']
    else:
        return ''


def get_iskm_egov_token_user1():
    usr_pass = b"wNJo0NGxSMEBZs5CVNzuu5K77f0a:E9hiLpCf4_maCsFFDMXmXy88Am4a"
    b64_val = base64.b64encode(usr_pass)

    url = "https://iskm.egov.uz:9444/oauth2/token?grant_type=password&username=goskomles-user1&password" \
          "=C4uBik9iWeBvxFmg "

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic %s' % b64_val.decode("utf-8")
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(b64_val.decode("utf-8"))
    print(response.text)
    data = json.loads(response.text)
    if 'access_token' in data:
        return data['access_token']
    else:
        return ''


def check_job_status(pin, company_tin):
    url = "https://apimgw.egov.uz:8243/labour/service/citizen/status/v1"

    payload = json.dumps({
        "pin": pin, #32907895870017,
        "company_tin": company_tin #307575940
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % get_iskm_egov_token()
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    data = json.loads(response.text)
    if 'result' in data:
        return data['result']['data']['status']
    else:
        return 0


def get_userdata_from_pinfl(pinfl, passport_serial):
    url = "https://apimgw.egov.uz:8243/gcp/pinpp/v1"

    payload = f"""<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" 
              xmlns:eas=\"http://fido.com/EasuEGServices\">\n   
              <soapenv:Header/>\n   <soapenv:Body>\n     
              <eas:GetDataByPinppRequest>\n         
              <eas:Data><![CDATA[<?xml version=\"1.0\"?>\n
              <DataByPinppRequest xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" 
              xsi:noNamespaceSchemaLocation=\"file:///d:/STS/workspaceEASU/EasuEGServices/src/main/resources/xsdData/GetDatabyPinpp.xsd\">\n    
              <queryID>1</queryID>\n    
              <pinpp>{pinfl}</pinpp>\n    
              <document>{passport_serial}</document>\n    
              <langId>2</langId>\n    
              <!--Element orgcode is optional-->\n    
              <orgcode>string</orgcode>\n    
              <orgtin>string</orgtin>\n   
              <fio>string</fio>\n    
              <pin>string</pin>\n    
              <is_consent>Y</is_consent>    \n
              </DataByPinppRequest>]]></eas:Data>\n        
              <eas:Signature>?</eas:Signature>\n         
              <eas:PublicCert>?</eas:PublicCert>\n        
              <eas:SignDate>?</eas:SignDate>\n     
              </eas:GetDataByPinppRequest>\n   
              </soapenv:Body>\n</soapenv:Envelope>"""
    #41109752710063
    #AA8331973
    headers = {
        'Content-Type': 'text/xml',
        'Authorization': 'Bearer %s' % get_iskm_egov_token_user1()
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    output_dict1 = json.loads(json.dumps(xmltodict.parse(response.text)))

    print('1=====', output_dict1)
    print('4=====', output_dict1["env:Envelope"]["env:Body"]["GetDataByPinppResponse"]["Data"]["#text"])
    output_dict = json.loads(json.dumps(xmltodict.parse(output_dict1["env:Envelope"]["env:Body"]["GetDataByPinppResponse"]["Data"]["#text"])))
    print('3=====', output_dict)
    # print(output_dict['env:Envelope']['env:Body']['GetDataByPinppResponse']['Data']['personaldata']['row']["document"])
    # pinpp = output_dict["env:Envelope"]["env:Body"]['GetDataByPinppResponse']["pinpp"]
    result = {}
    if output_dict1['env:Envelope']['env:Body']['GetDataByPinppResponse']['Data']["#text"]:
        print('test1')
        result['Pasport seriya raqami:'] = output_dict['personaldata']['row']['document']
        result['Familyasi:'] = output_dict['personaldata']['row']['surnamelatin']
        result['Ismi:'] = output_dict['personaldata']['row']['namelatin']
        result['Sharifi:'] = output_dict['personaldata']['row']['patronymlatin']
        result["Tug'ilgan vaqti:"] = output_dict['personaldata']['row']['birth_date']
        result["Tug'ilgan joyi:"] = output_dict['personaldata']['row']['birthplace']
        result["Tug'ilgan davlati:"] = output_dict['personaldata']['row']['birthcountry']
        result["Millati:"] = output_dict['personaldata']['row']['nationality']
        result['Jinsi:'] = "Erkak" if output_dict['personaldata']['row']['sex'] == 1 else "Ayol"
        result['Kim tomonidan berilgan:'] = output_dict['personaldata']['row']['docgiveplace']
        result['Berilgan vaqti:'] =  output_dict['personaldata']['row']['docdatebegin']
        result['Amal qilish muddati:'] = output_dict['personaldata']['row']['docdateend']
        print(result)
    else:
        print('test2')
        result['Natija'] = 'Topilmadi'
    return Response(result, status=status.HTTP_200_OK)
