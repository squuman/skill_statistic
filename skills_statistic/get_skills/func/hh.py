import requests
import json
import pandas as pd

CLIENT_ID = 'SM8RSFOSSQ6R9GN4U1MP5VC0EIL1F9O8DUFTHVNUN52IS70RN46THNH2V9HPFUR5'
CLIENT_SECRET = 'PQ6RF0UFFEQUFRE5UD24DMC4O8GK3BKFAHSHUPK06QFO7QO5OKJNV1CF6NU71DUO'
ACCESS_TOKEN = 'V878EP9U3UHQK7T9FRTH3A64MUE544CUG03QA3URHPD3MDVJVA5PDLVATQB6U2AP'
REFRESH_TOKEN = 'SRSL3S5L8UGHARDOBT6D91N9CF5QO3QGBFER7F7VT439H8BPKVGS78UKN22MAT02'
CODE = 'OJRICFGG47AP5QASAAHOL6DUAK6FSGO6CMB75AM9F2635O2JEHUO52OE2CDUTI6G'

URL = "https://api.hh.ru"


# get code from https://hh.ru/oauth/authorize?response_type=code&client_id=SM8RSFOSSQ6R9GN4U1MP5VC0EIL1F9O8DUFTHVNUN52IS70RN46THNH2V9HPFUR5


def to_count_elements_in_list(_list):
    result = {}

    for element in _list:
        if element in result:
            result[element] += 1
        else:
            result[element] = 1

    return result


def auth(client_id, client_secret, code):
    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }
    response = requests.post("https://hh.ru/oauth/token", data=params)

    return json.loads(response.text)


def get_vacancies(search_text="", page=0):
    params = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": ACCESS_TOKEN,
        "text": search_text,
        "page": page
    }
    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "User-Agent": "api-test-agent"
    }
    response = requests.get(URL + "/vacancies", data=params, headers=headers)

    return json.loads(response.text)


def get_vacancy_skills(vacancy_name=""):
    data = get_vacancies(vacancy_name)
    pages_count = data['pages']
    skills_list = []

    for page in range(0, pages_count + 1):
        print(str(page) + "/" + str(pages_count))
        vacancies = get_vacancies(vacancy_name, page)

        for vacancy in vacancies['items']:
            response = requests.get(URL + "/vacancies/" + vacancy['id'])

            for skill in json.loads(response.text)['key_skills']:
                skills_list.append(skill['name'])

    return skills_list


def main():
    skills = to_count_elements_in_list(get_vacancy_skills(input("Input vacancy: ")))
    frame = pd.DataFrame(data=skills).transpose()
    print(frame.to_string())


if __name__ == "__main__":
    main()
