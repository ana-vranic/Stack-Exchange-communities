# Data Preparation Pipeline

Several steps are needed in order to extract time-stamped interactions sorted by type from raw XML data.
## xml_to_csv

The first step is to convert .xml files to .csv.

We start with:
- Posts.xml
- Comments.xml
- Users.xml
- Votes.xml

Scripts are found in `xml_to_csv` folder. Each script processes a specific type of interactions found in XML data and select data for the first 180 days. 
All scripts can be run using `filter_data.sh`

> users.csv  {"@UserId" "@UserName" "Age" "Location" 'UserCreationDate' "Reputation" "Views" "UpVotes" "DownVotes" "LastAccess"}

> questions.csv   {"QId", "QUserId",  "QTags", "QTime", "QAcceptedAnswerId", "QScore", "QViewCount", "QAnswerCount", "QCommentCount"}

> answers.csv     {"AId", "AUserId",  "QId", "ATime", "AScore",  "ACommentCount"}

> comments.csv   {"CId", "CUserId",  "PId",  "@UserName", "CTime",  'CScore'}

> accepted answers acc_answers.csv {"QId_x", "QUserId", "QTags", "QTime","QAcceptedAnswerId", "QScore", "QViewCount", "QAnswerCount", "QCommentCount","AId", "AUserId", "ATime", "AScore" , "ACommentCount"}

> votes.csv {"PostId", 	"Vote",  "VTime"}

## filter_interactions

Second step is to filter specific interactions from previously extracted CSV files. 

Scripts are found in `filter_interactions` folder. `interactions_data.sh` takes a list of communities from `area51.txt` or `launched.txt` and produces csv files of timestamped interactions related to posts (questions, answers, accepted answers), while `comments_data.sh` does the same for comments.

- question-answer  AnswerUserId(ResponduserId), questionUserId(PostUserId), answerTime
- accepted-answer  QuestionUserId(RespodUserId) - answerUserId(PostUserId), answerTime
- q/a - comment    CommentUserId(RespondUserId) - answer/questionUserId(PostUserId), commentTime
- posted questions - QuestionUserId (PostUserId) - questionTime

Interactions stores as CSV files with columns [PostUserId, RespondUserId, Time, days] are input for code which calculates dynamical reputation `dynamical_reputation.py`.