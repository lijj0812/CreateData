import requests
import urllib3


# eSlVslNYOl1SnLEoWn5c7MQGWVHb8JN8mSxRiqVT77UlM4FhFJ7tJvbnV6LQ1FJi39MWyytICkPa5iEC143SmBcfsBQ5nVJbjtiOldj5oS+8FhoGFxScRroug5GPwoYqJ2EKsOUaXcCidnMfj2kDyrNvwqZo29vpwDPaIHdF1GS3IsgSk73oX4EKxEzBWv5fgHrqx5fNG3X0RQgKnczhKSVpb2C+FmM9e6Zx+ONZIf3sJvfx0Xn8zdWWwXCDT8thtS6onFV+2IvRrGZfly07iP+LJP56KG6+sRrWPjdBAPR3rPehK8D321h4a/CYNSpmYdmjVPcigC3Fpy5eI4BE2Q==
# tUy1N9PvZNNZY0eLDsSXL8xTtzLWJdpcTXdiyfe9L5v+bbUbjpwKwukKWITN0BkFqeP4wZ5tUXrs6UOevVTvu+i7BQ88tawm6x/VPYMgGrXcDxDYayvWW4j/gtYE9RF7x1RLYacnuqZfOETk7YCHblYwlx898Le+aR8VoUGa46McBdUAsmXxbMRr5XJ4lcXWqfeBRvlShb8rleG0yBxz9Hl0unIMso0iZeGwuxSSckwx5AHLbo1hlydZDYTBnPxDT6PM316numRc3QnvpTz7/MYumaBN51nLCvJvSe5KY31hZTgw+9zCk8RWR9t0AzgGQsEc77K6z4GewzQZCJB3AQ==
def get_token():
    url = 'https://dev.recloud.com.cn:5202/token'
    body = {
        'grant_type': 'xrm',
        'username': 'crm\\administrator',
        'password': 'eC4o1DN/yW6rea5wpDdPb3ZS3F1qvF1y9gR1rA/knq1DPKseZnEeNP18jyM9yHIF7wJSmToiYNcisGx/Y+J+vo+nooxvI2FLOPjxy3kTOy0lvLgcuV/PjymxLqNU8fpD4Ug7EpF/0NsHKFvghz2+iLHJAMckkTHpWc0eorlfwB4dmkk5kepz4UFJf3YKTWE+cdn0zrnmlKYT19tR/NuG9G4pCR8VI4QI3mCk7CZI7bYROre6uoOc3uhoGxtCM2YzO81mXV+GrJfR5pKOGguSZjLSCvp9URR9Ey10qsYHUwUGm3Xp6DaeYH8acFWXdMyZKfHztxOyvrEFjPkhhm2E+Q=='
    }
    urllib3.disable_warnings()
    res = requests.post(url, data=body, verify=False)
    # print(res.json()['access_token'])
    return res.json()['access_token']
