from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
#TODO: un-used library?
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import requests

driver = webdriver.Chrome()
driver.maximize_window()
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#TODO: Is this locators used anywhere?
# Locators
B_THREE = (By.XPATH, "//img[@name='space62']")
C_FOUR_1 = (By.XPATH, "//img[@name='space53']")
C_FOUR_2 = (By.XPATH, "//img[@onclick='didClick(5, 3)']")
MAKE_A_MOVE = EC.visibility_of_element_located((By.XPATH, "//p[@id='message']"))
D_FIVE = (By.XPATH, "//img[@name='space44']")

#TODO: Un-used code?
# Explicit wait
wait = WebDriverWait(driver, 15)

# 1. Open the url
driver.get('https://deckofcardsapi.com/')
# 1.1. Make a screenshot if 'options.headless = True' it fits the screen
# driver.get_screenshot_as_file('site_is_up.png')
S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
driver.set_window_size(S('Width'),S('Height'))
driver.find_element(By.TAG_NAME, 'body').screenshot('site_is_up.png')
# 1.2. Verify the url 'https://deckofcardsapi.com/' is here
expected_url = 'https://deckofcardsapi.com/'
actual_url = driver.current_url
#TODO: you need to use some assertion library or test framework to make test cases
if expected_url in actual_url:
    print(f'Expected "{expected_url}", and got: "{actual_url}"\n')
else:
    print(f'Expected "{expected_url}", but got: "{actual_url}"\n')

# 2. Get a new deck
r=requests.get('https://deckofcardsapi.com/api/deck/new/')
print(f'Get a new deck')
#TODO: Not a good way to assert status_code, there is a lot of codes between 300 and 200, for example 204 No Content. You need to find success in requirements and assert only that.
if 300 >= r.status_code >= 200:
    print(f'"success": true')
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"shuffled": {(r.json()["shuffled"])}')
print(f'"remaining": {r.json()["remaining"]}')

# 3. Shuffle the deck
#TODO: Bad variable name, in the future if other people work on same big project, they will not be able to understand what is this variable from.
r=requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1')
print(f'\nShuffle the deck')
#TODO: Not a good way to assert status_code
if 300 >= r.status_code >= 200:
    print(f'"success": true')
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"shuffled": {(r.json()["shuffled"])}')
print(f'"remaining": {r.json()["remaining"]}')

# 4. Deal three cards to each of two players

#TODO: Code duplication, you can create one method to get cards from same deck for different players. Any number of players.
# 4.1. To player 1
#TODO: Bad variable name
r=requests.get('https://deckofcardsapi.com/api/deck/new/draw/?count=3')
print(f'\nDeal three cards to each of two players')
print(f'To player 1')
#TODO: Not a good way to assert status_code
if 300 >= r.status_code >= 200:
    print(f'"success": true')
deck_id = r.json()["deck_id"]
print(f'"deck_id": "{deck_id}"')
print(f'"cards": {(r.json()["cards"])}')
print(f'"remaining": {r.json()["remaining"]}\n')

#TODO: Code duplication, you can create one method to get cards from same deck for different players. Any number of players.
# 4.2. Count the score of player 1
#TODO: Bad variable name
pics_score = r.json()["cards"]
print(f'1th player.\n1th card: "{pics_score[0]["value"]}";\n2d card: "{pics_score[1]["value"]}";\n3d card: "{pics_score[2]["value"]}"')
#TODO: Bad variable name
total_1 = []
#TODO: Code duplication, You can create config file, with JACK, QUEEN, KING, ACE values, since their API doesnt have that values.duplication
if len(pics_score[0]["value"]) < 3:
    total_1.append(int(pics_score[0]["value"]))
elif type(pics_score[0]["value"]) != int:
    if pics_score[0]["value"] == 'JACK' or pics_score[0]["value"] == 'QUEEN' or pics_score[0]["value"] == 'KING':
        total_1.append(10)
    elif pics_score[0]["value"] == 'ACE':
        total_1.append(11)

if len(pics_score[1]["value"]) < 3:
    total_1.append(int(pics_score[1]["value"]))
elif type(pics_score[1]["value"]) != int:
    if pics_score[1]["value"] == 'JACK' or pics_score[1]["value"] == 'QUEEN' or pics_score[1]["value"] == 'KING':
        total_1.append(10)
    elif pics_score[1]["value"] == 'ACE':
        total_1.append(11)

if len(pics_score[2]["value"]) < 3:
    total_1.append(int(pics_score[2]["value"]))
elif type(pics_score[2]["value"]) != int:
    if pics_score[2]["value"] == 'JACK' or pics_score[2]["value"] == 'QUEEN' or pics_score[2]["value"] == 'KING':
        total_1.append(10)
    elif pics_score[2]["value"] == 'ACE':
        total_1.append(11)
print(f'{total_1}: total_1 = {sum(total_1)}')

#TODO: Code duplication, you can create one method to get cards from same deck for different players. Any number of players.
# 4.3. To player 2
print(f'\nTo player 2')
message = "https://deckofcardsapi.com/api/deck/" + deck_id + "/draw/?count=3"
r=requests.get(message, params=deck_id)
if 300 >= r.status_code >= 200:
    print(f'"success": true')
print(f'"deck_id": "{r.json()["deck_id"]}"')
print(f'"cards": {(r.json()["cards"])}')
print(f'"remaining": {r.json()["remaining"]}')
# 4.2. Count the score of player 1
pics_score = r.json()["cards"]
print(f'\n2d player.\n1th card: "{pics_score[0]["value"]}";\n2d card: "{pics_score[1]["value"]}";\n3d card: "{pics_score[2]["value"]}"')
#TODO: Bad variable name
total_2 = []
if len(pics_score[0]["value"]) < 3:
    total_2.append(int(pics_score[0]["value"]))
elif type(pics_score[0]["value"]) != int:
    if pics_score[0]["value"] == 'JACK' or pics_score[0]["value"] == 'QUEEN' or pics_score[0]["value"] == 'KING':
        total_2.append(10)
    elif pics_score[0]["value"] == 'ACE':
        total_2.append(11)

if len(pics_score[1]["value"]) < 3:
    total_2.append(int(pics_score[1]["value"]))
elif type(pics_score[1]["value"]) != int:
    if pics_score[1]["value"] == 'JACK' or pics_score[1]["value"] == 'QUEEN' or pics_score[1]["value"] == 'KING':
        total_2.append(10)
    elif pics_score[1]["value"] == 'ACE':
        total_2.append(11)

if len(pics_score[2]["value"]) < 3:
    total_2.append(int(pics_score[2]["value"]))
elif type(pics_score[2]["value"]) != int:
    if pics_score[2]["value"] == 'JACK' or pics_score[2]["value"] == 'QUEEN' or pics_score[2]["value"] == 'KING':
        total_2.append(10)
    elif pics_score[2]["value"] == 'ACE':
        total_2.append(11)
print(f'{total_2}: total_2 = {sum(total_2)}')

# 5. Check whether either has a blackjack
#TODO: There is 3 numbers in array, you need to also add total_1[2]
if total_1[0] + total_1[1] == 21:
    print(f'\n1th player has a blackjack')

if total_2[0] + total_2[1] == 21:
    print(f'\n2d player has a blackjack')

