from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import requests
import xmltodict, json
from django.utils.translation import gettext_lazy as _

from ...service import check_job_status, get_userdata_from_pinfl

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXV"
headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'SOAPAction': 'N/A'
}


class GetCitizenInfoViewOld(APIView):
    # URL: http://127.0.0.1:8000/api/ipsgov/v1/get_citizen_info/32907895870016

    def get(self, request, tin):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            import requests
            import xmltodict, json
            url = "https://ips.gov.uz/mediate/ips/MOI/GetCitizenInfoServiceNew?wsdl"
            payload = f"<x:Envelope\n    xmlns:x=\"http://schemas.xmlsoap.org/soap/envelope/\"\n    xmlns:get=\"urn:megaware:/mediate/ips/MOI/GetCitizenInfoServiceNew/GetCitizenInfoServiceNew.wsdl\">\n    <x:Header/>\n    <x:Body>\n        <get:PinppAddress>\n            <get:pinpp>{tin}</get:pinpp>\n        </get:PinppAddress>\n    </x:Body>\n</x:Envelope>"
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            #print("GetCitizenInfoServiceNew:", str(output_dict))
            if output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"][
                "AnswereId"] == "5":
                return Response({"answereMessage": output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"][
                    "PinppAddressResult"]["AnswereMessage"], "answereComment":
                                     output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"][
                                         "PinppAddressResult"]["AnswereComment"]}, status=status.HTTP_200_OK)
            citizen_info = {
                "district":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["District"]["Value"],
                "country":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Country"]["Value"],
                "region":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Region"]["Value"],
                "cadastre":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Cadastre"],
                "address":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Address"],
                "registrationDate":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["RegistrationDate"],
                "temproaryRegistrations":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "TemproaryRegistrations"],
            }
            return Response(citizen_info, status=status.HTTP_200_OK)  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetTinbyPasNumViewOld(APIView):
    # URL: http://127.0.0.1:8000/api/ipsgov/v1/get_tin_by_pass/AA5741847

    def get(self, request, passnum):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        try:
            import requests
            import xmltodict, json
            url = "https://ips.gov.uz:443/mediate/ips/STC/GetTinbyPasNumNew?wsdl"
            payload = f"<x:Envelope xmlns:x=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:get=\"urn:megaware:/mediate/ips/STC/GetTinbyPasNumNew/GetTinbyPasNumNew.wsdl\">\r\n    <x:Header/>\r\n    <x:Body>\r\n        <get:GetTinbyPas>\r\n            <get:action>get_tin</get:action>\r\n            <get:pass_ser>{passnum[:2]}</get:pass_ser>\r\n            <get:pass_num>{passnum[2:]}</get:pass_num>\r\n            <get:lang>2</get:lang>\r\n        </get:GetTinbyPas>\r\n    </x:Body>\r\n</x:Envelope>"
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            if output_dict["env:Envelope"]["env:Body"]["n1:FormData"]["err_code"] == "1":
                return Response({"err_text": output_dict["env:Envelope"]["env:Body"]["n1:FormData"]["err_text"]},
                                status=status.HTTP_200_OK)
            return Response(output_dict["env:Envelope"]["env:Body"]["n1:FormData"]["root"]["list"],
                            status=status.HTTP_200_OK)  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetPersonDocInfoService(APIView):
    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pnfl' in data and data['pnfl'] is None:
            return Response({"message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = "https://ips.gov.uz:443/mediate/ips/PC/PersonDocInfoService"
            payload = f"""<x:Envelope
                    xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:per="urn:megaware:/mediate/ips/PC/PersonDocInfoService/PersonDocInfoService.wsdl">
                    <x:Header/>
                    <x:Body>
                        <per:CEPRequest>
                            <per:AuthInfo>
                                <per:userSessionId></per:userSessionId>
                                <per:WS_ID></per:WS_ID>
                                <per:LE_ID></per:LE_ID>
                            </per:AuthInfo>
                            <per:Data>&lt;?xml version=&quot;1.0&quot; encoding=&quot;utf-8&quot;?&gt;
                              &lt;DataCEPRequest&gt;  &lt;pinpp&gt;{data['pnfl']}&lt;/pinpp&gt;&lt;document&gt;{data['pass_series']}&lt;/document&gt; &lt;langId&gt;1&lt;/langId&gt;&lt;/DataCEPRequest&gt;
                            </per:Data>
                            <per:Signature></per:Signature>
                            <per:PublicCert></per:PublicCert>
                            <per:SignDate></per:SignDate>
                        </per:CEPRequest>
                    </x:Body>
                </x:Envelope>
                """
            print('URL:')
            print(url)
            print('Header:')
            print(headers)
            print('PAYLOAD:')
            print(payload)
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            print('RESPONSE :')
            print(response)
            print('RESPONSE JSON:')
            print(output_dict)
            result = {}
            response_str = output_dict["env:Envelope"]["env:Body"]["n1:CEPResponse"]['Data']
            response_data = json.loads(json.dumps(xmltodict.parse(response_str)))
            if output_dict["env:Envelope"]["env:Body"]["n1:CEPResponse"]["Result"]:
                result['Pasport seriya raqami:'] = response_data['datacepresponse']['row']['document']
                result['Familyasi:'] = response_data['datacepresponse']['row']['surname_latin']
                result['Ismi:'] = response_data['datacepresponse']['row']['name_latin']
                result['Sharifi:'] = response_data['datacepresponse']['row']['patronym_latin']
                result["Tug'ilgan vaqti:"] = response_data['datacepresponse']['row']['birth_date']
                result["Tug'ilgan joyi:"] = response_data['datacepresponse']['row']['birth_place']
                result["Tug'ilgan davlati:"] = response_data['datacepresponse']['row']['birth_country']
                result["Millati:"] = response_data['datacepresponse']['row']['nationality']
                result['Jinsi:'] = "Erkak" if response_data['datacepresponse']['row']['sex'] == 1 else "Ayol"
                result['Kim tomonidan berilgan:'] = response_data['datacepresponse']['row']['doc_give_place']
                result['Berilgan vaqti:'] = response_data['datacepresponse']['row']['date_begin_document']
                result['Amal qilish muddati:'] = response_data['datacepresponse']['row']['date_end_document']
            else:
                result['Natija'] = 'Topilmadi'
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print("error", e.args)
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetCitizenInfoView(APIView):
    # URL: http://127.0.0.1:8000/api/ipsgov/v1/get_citizen_info/32907895870016

    def post(self, request):
        print("TEST")
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'jsh_shir' in data and data['jsh_shir'] is None:
            return Response({"message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = "https://ips.gov.uz/mediate/ips/MOI/GetCitizenInfoServiceNew?wsdl"
            payload = f"""
                <x:Envelope
                    xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:get="urn:megaware:/mediate/ips/MOI/GetCitizenInfoServiceNew/GetCitizenInfoServiceNew.wsdl">
                    <x:Header/>
                    <x:Body>
                        <get:PinppAddress>
                            <get:pinpp>{data['jsh_shir']}</get:pinpp>
                        </get:PinppAddress>
                    </x:Body>
                </x:Envelope>
            """
            response = requests.request("POST", url, headers=headers, data=payload)
            print(response)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            if output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"][
                "AnswereId"] == "5":
                return Response({"answereMessage": output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"][
                    "PinppAddressResult"]["AnswereMessage"], "answereComment":
                                     output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"][
                                         "PinppAddressResult"]["AnswereComment"]}, status=status.HTTP_200_OK)
            citizen_info = {
                "Shaxar":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["District"]["Value"],
                "Mamlakat":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Country"]["Value"],
                "Viloyat":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Region"]["Value"],
                "Kadastra":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Cadastre"],
                "Manzil":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["Address"],
                "Ro'yxatdan o'tgan vaqti":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "PermanentRegistration"]["RegistrationDate"],
                "Vaqtinchalik yashash manzili":
                    output_dict["env:Envelope"]["env:Body"]["n1:PinppAddressResponse"]["PinppAddressResult"]["Data"][
                        "TemproaryRegistrations"],
            }
            return Response(citizen_info, status=status.HTTP_200_OK)  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetTinbyPasNumView(APIView):
    # URL: http://127.0.0.1:8000/api/ipsgov/v1/get_tin_by_pass/

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        try:
            url = "https://ips.gov.uz:443/mediate/ips/STC/GetTinbyPasNumNew"
            payload = f"""<x:Envelope xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:get="urn:megaware:/mediate/ips/STC/GetTinbyPasNumNew/GetTinbyPasNumNew.wsdl">
                    <x:Header/>
                    <x:Body>
                        <get:GetTinbyPas>
                            <get:action>get_tin</get:action>
                            <get:pass_ser>{data['passport_number'][:2]}</get:pass_ser>
                            <get:pass_num>{data['passport_number'][2:]}</get:pass_num>
                            <get:lang>ru</get:lang>
                        </get:GetTinbyPas>
                    </x:Body>
                </x:Envelope>"""
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            print("output_dict", output_dict)
            if output_dict["env:Envelope"]["env:Body"]["n1:FormData"]["err_code"] == "1":
                return Response({"err_text": output_dict["env:Envelope"]["env:Body"]["n1:FormData"]["err_text"]},
                                status=status.HTTP_200_OK)
            return Response(output_dict["env:Envelope"]["env:Body"]["n1:FormData"]["root"]["list"],
                            status=status.HTTP_200_OK)  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetPensionService(APIView):
    """4.	Информация о размерах пенсии """

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pnfl' in data and data['pnfl'] is None:
            return Response({"Holati": "⚠ Error", "message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = "https://ips.gov.uz:443/mediate/ips/PensionService/GetRequestPensService"
            payload = f"""<x:Envelope 
                    xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:get="urn:megaware:/mediate/ips/PensionService/GetRequestPensService/GetRequestPensService.wsdl">
                    <x:Header/>
                    <x:Body>
                        <get:requestPensRequest>
                            <get:Data> &lt;?xml version="1.0"?&gt;
                      &lt;datacepresponse&gt;
                      &lt;row&gt;
                      &lt;type&gt;1&lt;/type&gt;
                      &lt;lang&gt;1&lt;/lang&gt;
                      &lt;pinpp&gt;{data['pnfl']}&lt;/pinpp&gt;
                      &lt;/row&gt;
                      &lt;/datacepresponse&gt;</get:Data>
                        </get:requestPensRequest>
                    </x:Body>
                </x:Envelope>
                """
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            result = {}
            if output_dict["env:Envelope"]["env:Body"]["n1:GetLegalEntityInfo"]["Result"]:
                response_str = output_dict["env:Envelope"]["env:Body"]["n1:GetLegalEntityInfo"]["Data"]
                response_dict = json.loads(json.dumps(xmltodict.parse(response_str)))
                working_history = None
                try:
                    working_history = response_dict['requestpension']['row']
                    response_dict['requestpension'].pop("row")
                except:
                    result["Faoliyat tarixi"] = "Topilmadi"
                result = response_dict['requestpension']
                if working_history:
                    list_item_count = 1
                    for item in working_history:
                        result[f'{list_item_count}) Faoliytat tarixi:'] = item['beginperiod'] + " / " + item[
                            'endperiod']
                        list_item_count += 1
            else:
                result['Natija'] = 'Topilmadi'
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print("e", e.args)
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetPensionAssngServive(APIView):
    """5. Информация о факте назначения пенсии"""

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pnfl' in data and data['pnfl'] is None:
            return Response({"Holati": "⚠ Error", "message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = "https://ips.gov.uz:443/mediate/ips/PensionService/GetPensionAssgnService"
            payload = f"""<x:Envelope 
                        xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" 
                        xmlns:get="urn:megaware:/mediate/ips/PensionService/GetPensionAssgnService/GetPensionAssgnService.wsdl">
                        <x:Header/>
                        <x:Body>
                            <get:pensionAssingRequest>
                                <get:Data>&lt;?xml version="1.0"?&gt;
                          &lt;datacepresponse&gt;
                          &lt;row&gt;
                          &lt;type&gt;1&lt;/type&gt;
                          &lt;lang&gt;1&lt;/lang&gt;
                          &lt;pinpp&gt;{data['pnfl']}&lt;/pinpp&gt;
                          &lt;/row&gt;
                          &lt;/datacepresponse&gt;</get:Data>
                            </get:pensionAssingRequest>
                        </x:Body>
                    </x:Envelope>
                    """
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            result = {}
            if output_dict["env:Envelope"]["env:Body"]["n1:GetLegalEntityInfo"]["Result"]:
                response_str = output_dict["env:Envelope"]["env:Body"]["n1:GetLegalEntityInfo"]["Data"]
                response_dict = json.loads(json.dumps(xmltodict.parse(response_str)))
                try:
                    result = response_dict['row']['out_text']['query']
                except:
                    result['Natija:'] = response_dict['row']['out_text']
            else:
                result['Natija:'] = "Malumot topilmadi"
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            print("e", e.args)
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetPensionSizeService(APIView):
    """6.Информация о размерах выданных пенсий, пособий (в разрезе периода) - """

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pnfl' in data and data['pnfl'] is None:
            return Response({"Holati": "⚠ Error", "message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = "https://ips.gov.uz:443/mediate/ips/PensionService/GetSizePensService"
            payload = f"""<x:Envelope 
                    xmlns:x="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:get="urn:megaware:/mediate/ips/PensionService/GetSizePensService/GetSizePensService.wsdl">
                    <x:Header/>
                    <x:Body>
                        <get:sizePensRequest>
                            <get:Data>&lt;?xml version="1.0"?&gt;
                      &lt;datacepresponse&gt;
                      &lt;row&gt;
                      &lt;type&gt;1&lt;/type&gt;
                      &lt;lang&gt;2&lt;/lang&gt;
                      &lt;pinpp&gt;{data['pnfl']}&lt;/pinpp&gt;
                      &lt;begin_period&gt;{data['start']}&lt;/begin_period&gt;
                      &lt;end_period&gt;{data['end']}&lt;/end_period&gt;
                      &lt;/row&gt;
                      &lt;/datacepresponse&gt;</get:Data>
                        </get:sizePensRequest>
                    </x:Body>
                </x:Envelope>"""
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            result = {}
            if output_dict["env:Envelope"]["env:Body"]["n1:GetLegalEntityInfo"]["Result"]:
                response_str = output_dict["env:Envelope"]["env:Body"]["n1:GetLegalEntityInfo"]["Data"]
                response_dict = json.loads(json.dumps(xmltodict.parse(response_str)))
                response_data = None
                history_list = None
                result['Hulosa'] = response_dict["sizepension"]['out_text']
                try:
                    response_data = response_dict["sizepension"]["data"]
                    history_list = response_dict['sizepension']['row']
                except:
                    return Response(result, status=status.HTTP_200_OK)
                result.update(response_data)
                for_count = 1
                if history_list:
                    for history in history_list:
                        result[f"{for_count})"] = f"""
                        {history['period'][:4]} - {history['month']}, qiymati-{history['summa']}"""
                        for_count += 1

            else:
                print("ERROR ELSEGA TUSHIB QOLDI", )
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class ObtainingCheckCertificate(APIView):
    """
        Obtain a certificate of conviction
        Fuqoro sudlanganligi to'g'risidagi malumotni olish uchun so'rovnoma yuborish va shu so'rov natijasini olish uchun bizga id keladi
        Example: 1-Fuqaro malumotini yuborish kerak va qaytgan id raqamni ko'rsatish kerak
    """

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        try:
            url = "https://ips.gov.uz:443/mediate/ips/MOI/CheckApplicant?wsdl"
            payload = f"""
                <x:Envelope
                    xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:che="urn:megaware:/mediate/ips/MOI/CheckApplicant/CheckApplicant.wsdl">
                    <x:Header/>
                    <x:Body>
                        <che:search>
                            <che:firstname>{data['first_name']}</che:firstname>
                            <che:lastname>{data['last_name']}</che:lastname>
                            <che:birth_year>{data['birth_year']}</che:birth_year>
                            <che:pinfl>{data['pnfl']}</che:pinfl>
                            <che:middlename>{data['midd_name']}</che:middlename>
                            <che:extra>?</che:extra>
                        </che:search>
                    </x:Body>
                </x:Envelope>
            """
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            if output_dict["env:Envelope"]["env:Body"]["n1:Form_data"]["request_id"]:
                result = {"So'rovingiz tekshirish uchun maxfiy raqam":
                              output_dict["env:Envelope"]["env:Body"]["n1:Form_data"]["request_id"],
                          "message": "Bu raqamni quyidagi 19-formaga 2 daqiqadan so'ng yuborib natija olishingiz mumkin"}
                return Response(result, status=status.HTTP_200_OK)
            else:
                return Response({"msg": False}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetObtainingResult(APIView):
    """
        ObtainingCheckCertificate dan olingan id ni shu API ga yuboramiz va natijani tekshiramiz
    """

    def post(self, request):
        data = request.data  # request_id
        if "request_id" in data and data['request_id'] == None:
            return Response({"Holati": "⚠ Error",
                            "message": "17-formadan olingan so'rov raqamni yuborilishi shart"})
        try:
            url = 'https://ips.gov.uz:443/mediate/ips/MOI/GetResult?wsdl'
            payload = f"""
                            <x:Envelope
                                xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                                xmlns:get="urn:megaware:/mediate/ips/MOI/GetResult/GetResult.wsdl">
                                <x:Header/>
                                <x:Body>
                                    <get:status>
                                        <get:id>{data['request_id']}</get:id>
                                    </get:status>
                                </x:Body>
                            </x:Envelope>
                        """
            resp = requests.request("POST", url, headers=headers, data=payload)
            response_data = json.loads(json.dumps(xmltodict.parse(resp.text)))
            response_state = response_data["env:Envelope"]["env:Body"]["n1:Form_data"]["success"]
            result = {}
            if response_state == 'true':
                result["Yurobirlan so'rov"] = response_data["env:Envelope"]["env:Body"]["n1:Form_data"]['result'][
                    'id']
                result["So'rov natijasi"] = \
                    response_data["env:Envelope"]["env:Body"]["n1:Form_data"]['result']['search_methods'][
                        'by_pinfl']
                result["So'rovning holati"] = "Tekshiruv yakunlangan" if \
                    response_data["env:Envelope"]["env:Body"]["n1:Form_data"]['result'][
                        'is_checked'] == "true" else ""
            elif response_state == 'false':
                result['Holati'] = f"{data['request_id']} raqamli so'rovgiz to'liq tekshirilmagan... "
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetDivorceInfo(APIView):
    """9.	Информация о разводе физических лиц"""

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pnfl' in data and data['pnfl'] is None:
            return Response({
                            "Holati": "⚠ Error",
                            "message": "Jismoniy shaxsning identifikatsion raqamini yuboring"

                            },
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            url = "https://ips.gov.uz:443/mediate/ips/RegisteryOffice/DivorceInfo"
            payload = f"""
                        <x:Envelope
                            xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                            xmlns:div="urn:megaware:/mediate/ips/RegisteryOffice/DivorceInfo/DivorceInfo.wsdl">
                            <x:Header/>
                            <x:Body>
                                <div:GetDivorceInfo>
                                    <div:ID>54</div:ID>
                                    <div:pnfl>{data['pnfl']}</div:pnfl>
                                    <div:token>154591210</div:token>
                                </div:GetDivorceInfo>
                            </x:Body>
                        </x:Envelope>"""
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            result = {"Natija:": output_dict["env:Envelope"]["env:Body"]["n1:element4"]["result_message"]}
            return Response(result, status=status.HTTP_200_OK)  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetDeathCertInfo(APIView):
    """Получение информации касательно свидетельства о смерти 31908922170037"""

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        try:
            url = "https://ips.gov.uz/mediate/ips/RegisteryOffice/DeathCertInfo"
            payload = f"""
                        <x:Envelope
                            xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                            xmlns:dea="urn:megaware:/mediate/ips/RegisteryOffice/DeathCertInfo/DeathCertInfo.wsdl">
                            <x:Header/>
                            <x:Body>
                                <dea:DeathCertInfo>
                                    <dea:ID>87</dea:ID>
                                    <dea:pnfl>{data['pnfl']}</dea:pnfl>
                                    <dea:token>154591210</dea:token>
                                </dea:DeathCertInfo>
                            </x:Body>
                        </x:Envelope>
                        """
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            result = {"Natija:": output_dict["env:Envelope"]["env:Body"]["n1:Response"]["result_message"]}
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class GetPositionInfo(APIView):
    """11.	Информация о текущей должности"""

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        response_state = None
        result = {}
        try:
            url = "https://ips.gov.uz:443/mediate/ips/JobPosition/GetCurrentPosition"
            payload = f"""<x:Envelope
                            xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                            xmlns:get="urn:megaware:/mediate/ips/JobPosition/GetCurrentPosition/GetCurrentPosition.wsdl">
                            <x:Header/>
                            <x:Body>
                                <get:GetCurrentPosition>
                                    <get:id>234</get:id>
                                    <get:pnfl>{data['pnfl']}</get:pnfl>
                                </get:GetCurrentPosition>
                            </x:Body>
                        </x:Envelope>"""
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            response_state = \
                output_dict["env:Envelope"]["env:Body"]["n1:GetCurrentPositionResponse"]['GetCurrentPositionResult'][
                    'result']['success']
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)
        if response_state == 'True':
            response_data = \
                output_dict["env:Envelope"]["env:Body"]["n1:GetCurrentPositionResponse"]['GetCurrentPositionResult'][
                    'result']['data']
            child_data = response_data.pop('data')['InnerDataResponseModel']
            result = response_data
            result.update(child_data)
        elif response_state == 'False':
            result['Natija:'] = \
                output_dict["env:Envelope"]["env:Body"]["n1:GetCurrentPositionResponse"]['GetCurrentPositionResult'][
                    'result']['message']
        else:
            result['Natija:'] = "Malumot topilmadi"
        return Response(result, status=status.HTTP_200_OK)


class GetPositionHistoryService(APIView):
    """12.	Получение информации о истории должностей"""

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        response_state = None
        result = {}
        output_dict = None
        try:
            url = "https://ips.gov.uz:443/mediate/ips/JobPosition/GetPositionHistory"
            payload = f"""
                    <x:Envelope
                        xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                        xmlns:get="urn:megaware:/mediate/ips/JobPosition/GetPositionHistory/GetPositionHistory.wsdl">
                        <x:Header/>
                        <x:Body>
                            <get:GetPositionHistory>
                                <get:id>2</get:id>
                                <get:pnfl>{data['pnfl']}</get:pnfl>
                            </get:GetPositionHistory>
                        </x:Body>
                    </x:Envelope>
            """
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            response_state = \
                output_dict["env:Envelope"]["env:Body"]["n1:GetPositionHistoryResponse"]['GetPositionHistoryResult'][
                    'result']['success']
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)
        if response_state == "True":
            res_data = \
                output_dict["env:Envelope"]["env:Body"]["n1:GetPositionHistoryResponse"]['GetPositionHistoryResult'][
                    'result']['data']
            profile = res_data['profile'] if res_data['profile'] else ""
            experiences = res_data['experiences']['anyType'] if res_data['experiences']['anyType'] else ""
            if all((profile, experiences)):
                res_data.pop('profile')
                res_data.pop('experiences')
                result = res_data
                result['PROFILE'] = "---------------------"
                result.update(profile)
                result['EXPERIENCES'] = "---------------------"
                result.update(experiences)
            else:
                result = res_data
        elif response_state == "False":
            result['Natija:'] = \
                output_dict["env:Envelope"]["env:Body"]["n1:GetPositionHistoryResponse"]['GetPositionHistoryResult'][
                    'result']['message']
        else:
            result['Natija:'] = "Malumot topilmadi"
        return Response(result, status=status.HTTP_200_OK)  # True


class GetOwnershipPnflService(APIView):
    """16.	Получение данных о недвижимости."""

    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        response_state = None
        result = {}
        try:
            url = "https://ips.gov.uz:443/mediate/ips/Cadastre/GetOwnerbyPinpp"
            payload = f"""
                        <x:Envelope
                            xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
                            xmlns:get="urn:megaware:/mediate/ips/Cadastre/GetOwnerbyPinpp/GetOwnerbyPinpp.wsdl">
                            <x:Header/>
                            <x:Body>
                                <get:getDataByPINFL>
                                    <get:pinfl>{data['pnfl']}</get:pinfl>
                                    <get:time>{data['time']}</get:time>
                                    <get:id>23</get:id>
                                </get:getDataByPINFL>
                            </x:Body>
                        </x:Envelope>"""
            response = requests.request("POST", url, headers=headers, data=payload)
            output_dict = json.loads(json.dumps(xmltodict.parse(response.text)))
            response_state = \
                output_dict["env:Envelope"]["env:Body"]["n1:getDataByPINFLResponse"]['getDataByPINFLResult']['code']
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)
        print("response_state", response_state == '1')
        if response_state == '1':
            response_data = output_dict["env:Envelope"]["env:Body"]["n1:getDataByPINFLResponse"]['getDataByPINFLResult']
            cada_str = response_data["cadastr_list"]
            response_data.pop("cadastr_list")
            result = response_data
            result.update(cada_str)
        elif response_state == '2':
            response_data = output_dict["env:Envelope"]["env:Body"]["n1:getDataByPINFLResponse"]['getDataByPINFLResult']
            result = response_data
        else:
            result['Natija:'] = "Malumot topilmadi"
        return Response(result, status=status.HTTP_200_OK)


class Post_check_job_status(APIView):
    def post(self, request):
        print("TEST")
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pin' in data and data['pin'] is None:
            return Response({"message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            val = check_job_status(data['pin'], data['stir'])
            job_status = {
                "status": val
            }
            return Response(job_status, status=status.HTTP_200_OK)  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)


class Post_userdata_from_pinfl(APIView):
    def post(self, request):
        if request.headers.get('Custom-Auth') != token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        data = request.data
        if 'pnfl' in data and data['pnfl'] is None and 'pass_series' in data and data['pass_series'] is None:
            return Response({"message": "Jismoniy shaxsning identifikatsion raqamini yuboring"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            val = get_userdata_from_pinfl(data['pnfl'], data['pass_series'])

            return val  # True
        except Exception as e:
            return Response(e.args, status=status.HTTP_204_NO_CONTENT)
