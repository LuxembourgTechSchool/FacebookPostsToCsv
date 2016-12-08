# Convert Facebook Posts Data to CSV

This small script takes as input the JSON output of an API result form Facebook Graph API for Posts.

The query is the following:

    me/posts?limit=5000&fields=message,story,created_time,reactions.limit(1000)

Alternatively, you can also try this query:

    me/posts?limit=5000&fields=message,story,created_time,message_tags,shares,reactions.limit(1000)

Note that you need to get the token first and make sure that you choose the **user_posts** permission.

Once you have the result, copy the JSON into a file called for example `posts.json` in the same directory as the script for simplicity.
Then open a command line, go to the location of this script and run:

    python fbToCsv.py posts.json

Now you should see a success message and 2 new CSV files should be created.