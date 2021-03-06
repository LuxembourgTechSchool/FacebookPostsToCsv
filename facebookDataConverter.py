import csv
import json
import sys

class FacebookPostDataConverter():

    POST_FIELDNAMES         = ['id', 'created_time', 'message', 'story']
    REACTIOM_FIELDNAMES     = ['id', 'name', 'type', 'post']

    # NONE, LIKE, LOVE, WOW, HAHA, SAD, ANGRY, THANKFUL

    def __init__(self, token):
        self.token = token

    def convertToCsv(self, output_id='default'):
        ''' Opens the JSON file containing the Facebook Graph API result from this query:
        me/posts?limit=5000&fields=message,story,created_time,reactions.limit(1000)
        and create 2 simple CSV output files. One CSV lists all the posts and the other the
        reactions mapped to the person and associated post.
        '''
        success = False

        post_count = 0
        reaction_count = 0

        # Prepare the filenames for the new CSV files
        posts_csv_filename = 'posts_{}.csv'.format(output_id)
        reactions_csv_filename = 'reactions_{}.csv'.format(output_id)

        # Open the JSON file and create 2 new CSV files. They are automatically overridden.
        #with open( self.file_path ) as data_file, open(posts_csv_filename, 'w') as posts_csv, open(reactions_csv_filename, 'w') as reactions_csv: 
        with open(posts_csv_filename, 'w', encoding='utf-8') as posts_csv, open(reactions_csv_filename, 'w', encoding='utf-8') as reactions_csv: 
            
            # Load the JSON data
            #data = json.load(data_file, strict = False)
            data = self.__get_fb_data(self.token)

            # Open the CSV DictWriters and write the headers
            posts_writer        = csv.DictWriter(posts_csv, fieldnames=self.POST_FIELDNAMES)
            reactions_writer    = csv.DictWriter(reactions_csv, fieldnames=self.REACTIOM_FIELDNAMES)

            posts_writer.writeheader()
            reactions_writer.writeheader()

            # Loop over all post
            for post in data['data']:
                # Create new post dictionary for the fields:
                try:
                    post_dict = self.__get_post_dict(post)
                
                    posts_writer.writerow(post_dict)

                    post_count += 1

                    # Loop over all reactions
                    if 'reactions' in post:
                        for reaction in post['reactions']['data']:
                            reaction_dict = self.__get_reaction_dict(reaction, post_dict['id'])
                            reactions_writer.writerow(reaction_dict)

                            reaction_count += 1
                except Exception as exception:
                    print('SORRY, 1 POST SKIPPED. IT CONTAINS SOMETHING STRANGE.')

            success = True
        
            print('{} Posts have been saved.'.format(post_count))
            print('{} Reactions have been saved.'.format(reaction_count))

        if success:
            return [posts_csv_filename, reactions_csv_filename]
        else:
            return None

    def __get_post_dict(self, post):
        ''' Transform a post row into a Python dictionary based on
        the POST_FIELDNAMES defined.
        '''
        data = {}
        for field in self.POST_FIELDNAMES:
            if field in post:
                data[field] = post[field]
            else:
                data[field] = ''
        return data

    def __get_reaction_dict(self, reaction, post):
        ''' Transform a reaction row into a Python dictionary.
        '''
        data = {}
        if ('id' in reaction) and ('name' in reaction):
            data['id'] = reaction['id']
            data['name'] = reaction['name']
            data['post'] = post

        if 'type' in reaction:
            data['type'] = reaction['type']
        else:
            print('__get_reaction_dict did not find "type" post "{}", and reaction "{}"'.format(post, reaction))
            data['type'] = 'LIKE'

        return data

    def __get_fb_data(self, token):
        try:
            # For Python 3.0 and later
            from urllib.request import urlopen
        except ImportError:
            # Fall back to Python 2's urllib2
            from urllib2 import urlopen

        url = "https://graph.facebook.com/v2.8/me/posts?limit=5000&fields=message%2Cstory%2Ccreated_time%2Creactions.limit(1000)&access_token={}".format(token)
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)



