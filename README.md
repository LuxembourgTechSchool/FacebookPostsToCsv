# Convert Facebook Posts Data to CSV

This small script takes as input the JSON output of an API result form Facebook Graph API for Posts.

Here is the direct link to the [Graph Explorer of Facebook](https://developers.facebook.com/tools/explorer/?method=GET&path=me%2Fposts%3Flimit%3D5000%26fields%3Dmessage%2Cstory%2Ccreated_time%2Cmessage_tags%2Cshares%2Creactions.limit(1000)&version=v2.8).

The query is the following:

    me/posts?limit=5000&fields=message,story,created_time,reactions.limit(1000)

Alternatively, you can also try this query:

    me/posts?limit=5000&fields=message,story,created_time,message_tags,shares,reactions.limit(1000)

It justs request 5000 posts, and includes maximum 1000 reactions per posts. 
Feel free to change those values if you have a lot more activity.

Note that you need to get the token first and make sure that you choose the **user_posts** permission.

Copy the Token that you received on the graph API and use it as `<YOUR_TOKEN>` in the next command.

Open a command line, go to the location of this script and run:

    python fbToCsv.py <YOUR_TOKEN>

Now you should see a success message and 2 new CSV files should be created.