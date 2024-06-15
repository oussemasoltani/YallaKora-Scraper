import requests
from bs4 import BeautifulSoup
import csv


date = input("Please enter a Date in the following format MM/DD/YYY: ")
page = requests.get(f"https://www.yallakora.com/Match-Center/?date={date}")

def main (page):

    src = page.content
    soup = BeautifulSoup(src, "lxml")

    matches_details = []

    championships = soup.find_all("div",{'class':'matchCard'})

    def get_match_info(championship):
        championship_title = championship.contents[1].find("h2").text.strip()
        all_matches = championship.find_all('div', {'class': 'ul'})[0].find_all('div', {'class': 'item'})
        number_of_matches = len(all_matches)


        for i in range(number_of_matches):
            #get teams names
            team_A = all_matches[i].find('div',{'class': 'teamA'}).text.strip()
            team_B = all_matches[i].find('div',{'class': 'teamB'}).text.strip()

            #get score
            match_result = all_matches[i].find('div',{'class':'MResult'}).find_all('span',{'class':'score'})
            score= f"{match_result[0].text.strip()} - {match_result[1].text.strip()}"

            #get match time
            match_time = all_matches[i].find('div',{'class':'MResult'}).find('span',{'class':'time'}).text.strip()

            #add match info to matches_details
            matches_details.append({"نوع البطولة": championship_title , "الفريق الاول":team_A , "الفريق الثاني":team_B , "ميعاد المباراة":match_time, "النتيجة":score})


    for i in range(len(championships)):
        get_match_info(championships[i])
    

    keys= matches_details[0].keys()

    # Specify the path to your document
    file_path = r"C:\Users\21623\Documents\Code\KoraLive\match-detailss.csv"

    try:
            with open(file_path, 'w', encoding='utf-8', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(matches_details)
                print("File created successfully.")
    except IOError as e:
            print(f"An error occurred while writing to the file: {e}")



main(page)