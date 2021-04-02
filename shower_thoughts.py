import requests

headers = {
    'authority': 'www.reddit.com',
    'cache-control': 'no-cache',
    'sec-ch-ua': '^\\^Google',
    'sec-ch-ua-mobile': '?0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'image',
    'accept-language': 'sl-GB,sl;q=0.9,en-GB;q=0.8,en;q=0.7,sl-SI;q=0.6',
    'cookie': 'edgebucket=XjuEz8Y1yTaFSYPncG; csv=1; __gads=ID=5970f129e54e565a:T=1608810906:S=ALNI_Mb_phbTD6S36l5DCPL9pOCjF9XnkA; eu_cookie_v2=3; pc=g9; over18=1; G_ENABLED_IDPS=google; reddit_session=12592833^%^2C2021-02-21T17^%^3A39^%^3A50^%^2Ce15d7d7b337d7dafa0d088918f0714d304c51339; loid=00000000000007hwox.2.1334817567000.Z0FBQUFBQmdNcHJtbkNqc1VtRHRrQUwxdFVSeUdHUkNHY0paX1BrdWV3Q2dabTE1VEdscHNHaGhpVVJSamxNdGhqcUhUcWI1UkVjTWxwa2Q3LW5iaElvU0twaFd0c0F0OGRpQlVRcE5sNTlBMTllQTl4dHlCMnhmcnd3ZFlZR1VsZHF1UVpwcWNBbHY; __stripe_mid=40edcb86-c02e-4e68-b174-cd5d873061505e49f3; eu-cookies-opted=^{^%^22opted^%^22:true^%^2C^%^22nonessential^%^22:true^}; __aaxsc=1; session=670dc9679b0f213dbb95cd219ae581893f23fc4cgASVSQAAAAAAAABKpcRlYEdB2BlwSN0tkn2UjAdfY3NyZnRflIwoYWU0ZjYyMWJhZTg5M2EwZjA0MTg3MzNjMmNjMzdmNzBkZTcyNTdjZJRzh5Qu; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MTczNjY5MzEsInN1YiI6IjEyNTkyODMzLXBDS3hsMHdVSXh6QWJLbG1XZFJwcHgwbGZQVSIsImxvZ2dlZEluIjp0cnVlLCJzY29wZXMiOlsiKiIsImVtYWlsIl19.jJRODhwii_3sTKfZaq9DtXKxfXf_ukFSol8iIeLeG0Q; Pfyber_recentclicks2=t3_bfork2^%^2Ct3_coz6ft^%^2Ct3_43z4gp^%^2Ct3_36rsj8; recent_srs=t5_2r8ot^%^2Ct5_2szyo^%^2Ct5_2qizd^%^2Ct5_2rrlp^%^2Ct5_2r7yd^%^2Ct5_30u7h^%^2Ct5_2qwmn^%^2C; aasd=1^%^7C1617364384074; session_tracker=gampioqrhpfpaljbjk.0.1617364588993.Z0FBQUFBQmdad1p0elVDaEE2VnJKUUZhZ0tBbVEyTzZhSW4wMDFOdDBKZnYxOHNZN3AxQXJYS2ZDWlBrNHU2ZHNybXpOTllCQTRRQjhrYnlWdlRjX1NCQ1I5NUtrbDFMUGtfUFhQWW9YY2Y0UDBuQXRadkoyRHZ1R3ZiQUQ1a3ZFMl9fcnh3S1BkZ3o',
    'pragma': 'no-cache',
    'referer': 'https://www.reddit.com/r/Showerthoughts/top/.json?count=5',
}
params = (
    ('count', '100'),
    ('limit', '1000')
)

shower_thoughts = []


def get_shower_thoughts():
    response = requests.get('https://www.reddit.com/r/Showerthoughts/top/.json',
                            headers=headers,
                            params=params
                            ).json()["data"]["children"]
    for r in response:
        shower_thoughts.append(r["data"]["title"])
    return shower_thoughts
