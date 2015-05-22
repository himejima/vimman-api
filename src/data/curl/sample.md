# operators
## GET
$ curl http://www.vimmanbot.local/api/operators/

## GET
$ curl http://www.vimmanbot.local/api/operators/1

## POST
$ curl http://www.vimmanbot.local/api/operators/ -F "operators[username]=usernamedesu" -F "operators[password]=passworddesu" -F "operators[state]=1"

## PUT
$ curl http://www.vimmanbot.local/api/operators/5 -X PUT -F "operators[username]=username_update" -F "operators[password]=password2" -F "operators[state]=0"

## DELETE
$ curl http://www.vimmanbot.local/api/operators/5 -X DELETE


# questions
## GET
$ curl http://www.vimmanbot.local/api/questions/

## GET
$ curl http://www.vimmanbot.local/api/questions/1

## POST
$ curl http://www.vimmanbot.local/api/questions/ -F "questions[content]=question11111" -F "questions[state]=1" -F "questions[answer]=answer1"

## PUT
$ curl http://www.vimmanbot.local/api/questions/14 -X PUT -F "questions[content]=question_updater" -F "questions[state]=0" -F "questions[answer]=456"

## DELETE
$ curl http://www.vimmanbot.local/api/questions/1 -X DELETE

# responses
## GET
$ curl http://www.vimmanbot.local/api/responses/

## GET
$ curl http://www.vimmanbot.local/api/responses/1

## POST
$ curl http://www.vimmanbot.local/api/responses/ -F "responses[type]=1" -F "responses[content]=content desu" -F "responses[state]=1"

## PUT
$ curl http://www.vimmanbot.local/api/responses/3 -X PUT -F "responses[type]=0" -F "responses[content]=res_content" -F "responses[state]=0"

## DELETE
$ curl http://www.vimmanbot.local/api/responses/3 -X DELETE

# tweets
## GET
$ curl http://www.vimmanbot.local/api/tweets/

## POST
$ curl http://www.vimmanbot.local/api/tweets/ -F "tweets[type]=question11111" -F "tweets[tweet_id]=1" -F "tweets[content]=answer1" -F "tweets[post_url]=http://google.com"

# informations
## GET
$ curl http://www.vimmanbot.local/api/informations/

## GET
$ curl http://www.vimmanbot.local/api/informations/1

## POST
$ curl http://www.vimmanbot.local/api/informations/ -F "informations[content]=情報" -F "informations[state]=0"

## PUT
$ curl http://www.vimmanbot.local/api/informations/8 -X PUT -F "informations[content]=infoinfo" -F "informations[state]=1"

## DELETE
$ curl http://www.vimmanbot.local/api/informations/7 -X DELETE
