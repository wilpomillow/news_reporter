from requests import get, post, Session
from bs4 import BeautifulSoup
from gtts import gTTS
from playsound import playsound

# pages = int(input("Pages of news to read: "))
pages = 5
page_number = 0
story_count = 10

s = Session()
save_counter = 0
domain = 'https://www.reuters.com/'

for i in range(0, pages + 1):
    reuters_url = str(f'https://www.reuters.com/news/archive/worldnews?view=page&page={page_number}&pageSize={story_count}')
    response = s.get(reuters_url)
    page_number += 1

    if response.status_code == 200:
        soup = BeautifulSoup(response.content,features="html.parser")
        story_counter = 0
        
        headlines = soup.select('''a''')
        # print(headlines)
        
        for j in headlines:
            aref = str(j).strip(' ')
            if (str('class="story-title"') in aref) == True:
                
                # if story_counter < int(story_count - 1):
                if story_counter < int(len(headlines)):    
                    split_a_tag = str(j).split('<h3 class="story-title">')
                    headline = split_a_tag[1].lstrip().rstrip('</a>').strip(":").rstrip().rstrip('/h3>').rstrip('<').replace('&amp;',' and ')
                    news_link = str(domain+split_a_tag[0].lstrip('<a href="').rstrip().rstrip('">'))
                    
                    story_request = s.get(news_link)
                    story_page = BeautifulSoup(story_request.content,features="html.parser")
                    story_content = story_page.select('p')
                    story_content = [format(paragraph).rstrip('</p>').lstrip('<p>') for paragraph in story_content]
                    story_content = story_content[1:len(story_content)-3]
                    story = ''.join(story_content).replace('&amp;',' and ')

                    story_re_list = story_content[0:2]
                    story_read = ''.join(story_re_list).replace('&amp;',' and ')

                    print(headline)
                    print('[LINK:',news_link,']')
                    print(story,'\n')

                    story_counter += 1
                    save_counter += 1

                    read_this = str(headline+' '+story_read)
                    tts = gTTS(read_this, lang="en")
                    file_name = str('headlines/'+headline.title().replace(' ','').replace(':','').replace(",",'')[0:25]+".mp3")
                    # file_name = str("headlines/headline"+str(save_counter)+".mp3")
                    tts.save(file_name)
                    playsound(file_name)

            else:
                1+1
                
    else:
        print('Cannot connect to internet. Please try again.')
        exit()    