import csv
import json
import sys

class FacebookPostDataConverter():

    POST_FIELDNAMES         = ['id', 'created_time', 'message', 'story']
    REACTIOM_FIELDNAMES     = ['id', 'name', 'type', 'post']

    # NONE, LIKE, LOVE, WOW, HAHA, SAD, ANGRY, THANKFUL

    def __init__(self, file_path):
        self.file_path = file_path

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
        with open( self.file_path ) as data_file, open(posts_csv_filename, 'w') as posts_csv, open(reactions_csv_filename, 'w') as reactions_csv: 
            
            # Load the JSON data
            data = json.load(data_file, strict = False)

            # Open the CSV DictWriters and write the headers
            posts_writer        = csv.DictWriter(posts_csv, fieldnames=self.POST_FIELDNAMES)
            reactions_writer    = csv.DictWriter(reactions_csv, fieldnames=self.REACTIOM_FIELDNAMES)

            posts_writer.writeheader()
            reactions_writer.writeheader()

            # Loop over all post
            for post in data['data']:
                # Create new post dictionary for the fields:
                post_dict = self.__get_post_dict(post)
                posts_writer.writerow(post_dict)

                post_count += 1

                # Loop over all reactions
                if 'reactions' in post:
                    for reaction in post['reactions']['data']:
                        reaction_dict = self.__get_reaction_dict(reaction, post_dict['id'])
                        reactions_writer.writerow(reaction_dict)

                        reaction_count += 1

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
        data = {
            'id':   reaction['id'],
            'name': reaction['name'],
            'type': reaction['type'],
            'post': post
        }
        return data
