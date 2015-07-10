import facebook
import json
import codecs
from termcolor import colored


def pretty_print(str):
    print json.dumps(str, indent=4, sort_keys=True)

def pretty(str):
    return json.dumps(str, indent=4, sort_keys=True)

# Function to display and append lines to the given file
def my_print(para,filelink,color):
    if(color == 0):
        print para
    elif(color == 1):
        print colored(para, 'green')
    else:
        print colored(para, 'red')
        
    if(para.isdigit()):
        para = str(para)
        
    file_out = codecs.open(filelink, 'a', encoding="utf-8")
    file_out.write(para)
    file_out.write("\n")
    file_out.close()


def main():

  # Add your teammates / friends' facebook name here.
  MemList = ['Teammate1', 'Teammate2']
  
  #Filename in which the output data is dumped
  file_liked = 'workfile_likes.txt'
  #File in which complete response by GraphAPI will be dumped for debugging
  f = open('workfile.txt', 'w')


  cfg = {
    "page_id"      : "123456789000000",  # your page id
    "access_token" : "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" # access token from developers.facebook.com
    }

  api = get_api(cfg)
  #Fetch all recent posts from the page
  posts = api.get_connections(id=cfg['page_id'], connection_name='feed')
  
  # Dump posts in the file for debugging
  f.write(pretty(posts))
  
  print 'Initiating... '
  m = len(posts['data'])
  
  my_print("Posts " + str(m),file_liked,0)
  
  for x in range(0, m):
    if(posts['data'][x]['from']['id'] in (cfg['page_id'])):
        my_print('#################################################################################',file_liked,0)
        my_print("Post ID " + posts['data'][x]['id'],file_liked,0)
        my_print('---------------------------------------------------------------------------------',file_liked,0)
        my_print("Message " + posts['data'][x]['message'],file_liked,0)
        my_print('---------------------------------------------------------------------------------',file_liked,0)
        if('share' in posts['data'][x]):
            my_print("Share " + str(posts['data'][x]['shares']['count']),file_liked,0)
            my_print('---------------------------------------------------------------------------------',file_liked,0)
        my_print('---------------------------------------------------------------------------------',file_liked,0)
        n = len(posts['data'][x]['likes']['data'])
        liked = []
        for y in range(0,n):
            # Team members who has liked the post
            if(posts['data'][x]['likes']['data'][y]['name'] in MemList):
                my_print(pretty(posts['data'][x]['likes']['data'][y]['name']),file_liked,1)
                liked.append(posts['data'][x]['likes']['data'][y]['name'])
            else:
                my_print(pretty(posts['data'][x]['likes']['data'][y]['name']),file_liked,0)
        
        # Team members didnt like the post
        my_print('These team members didnt liked',file_liked,2)
        for z in MemList:
            if(z not in liked):
                my_print(z,file_liked,2)
        my_print('#################################################################################',file_liked,0)
        liked = []
  f.close()
  
def get_api(cfg):
  graph = facebook.GraphAPI(cfg['access_token'])
  # Get page token to post as the page. 
  resp = graph.get_object('me/accounts')
  page_access_token = None
  for page in resp['data']:
    if page['id'] == cfg['page_id']:
      page_access_token = page['access_token']
  graph = facebook.GraphAPI(page_access_token)
  return graph

if __name__ == "__main__":
  main()
