import sqlite3
from datetime import datetime


__author__ = 'omar'




def createUserTable():
    try:
     c = conn.cursor()
     result =c.execute('''CREATE TABLE user
             (name text , email text PRIMARY KEY, password text, department text,register Date)''')

    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result
def createPostTable():
    try:
     c = conn.cursor()
     result =c.execute('''CREATE TABLE post (question text , id INTEGER PRIMARY KEY,
      upvote INTEGER, downvote INTEGER,views INTEGER,comments INTEGER ,postDate Date,
 tag text,time timestamp, email text ,FOREIGN KEY(email ) REFERENCES user(email))''')

    except sqlite3.OperationalError:
        print("Error")
        return -1
    return 1

def createCommentTable():
    try:
     c = conn.cursor()
     result =c.execute('''CREATE TABLE Comment (comment text , id INTEGER PRIMARY KEY,
      upvote INTEGER, downvote INTEGER,postDate Date,
      time timestamp, email text,postID INTEGER  ,FOREIGN KEY(email ) REFERENCES user(email),FOREIGN KEY(postID ) REFERENCES post(id))''')

    except sqlite3.OperationalError:
        print("Error")
        return -1
    return 1


def insertUser(name,email,password,dept,date):
    try:
         c = conn.cursor()
         result = c.execute("insert into user values (?, ?,?,?,?)", (name, email,password,dept,date))
         conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def insertPost(question,id,email,tags):
    try:
         c = conn.cursor()
         result = c.execute("insert into post values (?, ?,?,?,?,?, ?,?,?,?)", (question, id, 0, 0, 0, 0, datetime.today()
                                                                                , tags, datetime.now(), email))
         conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def insertComment(comment,id,email,postID):
    try:
         c = conn.cursor()
         result = c.execute("insert into comment values (?, ?,?,?,?,?,?,?)", (comment, id,  0, 0, datetime.today()
                                                                                , datetime.now(), email,postID))
         conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result



def selectUserTable():
    try:
     c = conn.cursor()
     result = c.execute('SELECT * FROM user ')


    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def selectPostTable():
    try:
     c = conn.cursor()
     result = c.execute('SELECT * FROM post ')


    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def selectPostTableOrderByDate(type):

    try:
     args = [type,]
     c = conn.cursor()
     result = c.execute('SELECT * FROM post order by ?',args)
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def selectPostTableOrderByUpVote(type):

    try:
     args = [type,]
     c = conn.cursor()
     result = c.execute('SELECT * FROM post order by ?',args)
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def selectPostTaggedBy(type):

    try:
     args = [type,]
     c = conn.cursor()
     result = c.execute('select  * from post where tag = ?',args)
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def getTags():

    try:

     c = conn.cursor()
     result = c.execute('select DISTINCT tag from post')
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result



def getPost(id):
    try:
     c = conn.cursor()
     t=(id,)
     c.execute('SELECT * FROM post where id = ?',t)
     result = (c.fetchone())
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def getAllCommentsOfpost(id):
    try:
     c = conn.cursor()
     t=(id,)
     result =  c.execute('SELECT * FROM comment where postID = ?',t)

    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result
def downVotePost(id):
    try:
     c = conn.cursor()
     t=(id,)
     result =  c.execute('UPDATE  post set downvote=downvote-1 where id = ?',t)
     conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def upVotePost(id):
    try:
     c = conn.cursor()
     t=(id,)
     result =  c.execute('UPDATE  post set upvote=upvote+1 where id = ?',t)
     conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result



def upVoteComment(id):
    try:
       c = conn.cursor()
       t=(id,)
       result =  c.execute('UPDATE  comment set upvote=upvote+1 where id = ?',t)
       conn.commit()
    except sqlite3.OperationalError:
          print("Error")
          return -1

    return result

def downVoteComment(id):
    try:
     c = conn.cursor()
     t=(id,)
     result =  c.execute('UPDATE  comment set downvote=downvote-1 where id = ?',t)
     conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result


def editPostText(text,id):
    try:
     c = conn.cursor()
     args=(text,id)

     result =  c.execute('UPDATE  post set question=? where id = ?',args)
     conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result

def editCommentText(text,id):
    try:
     c = conn.cursor()
     args=(text,id)

     result =  c.execute('UPDATE  comment set comment=? where id = ?',args)
     conn.commit()
    except sqlite3.OperationalError:
        print("Error")
        return -1
    return result




try:
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
except sqlite3.OperationalError:
    print("Error")

#resut = insertPost("Hi,How are you?",9766,"omar@gwu.edu","SEAS")
#print(resut)
#resut = insertPost("Hi,How can user Java?",1222,"kim@gwu.edu","GW")
#print(resut)
#resut = insertPost("Hi,How are you?",224,"Julie@gwu.edu","CS")
#print(resut)

#resut = insertComment("Fine",1,"kim@gwu.edu",9766)
#print(resut)
#resut = insertComment("Download Java?",2,"omar@gwu.edu",1222)
#print(resut)
#resut = insertComment("Go to Eclipse site ",5,"Julie@gwu.edu",1222)
#print(resut)
#resut = insertComment("Greeat",3, "omar@gwu.edu ",224)
#print(resut)


#createUserTable()
#y = insertUser('Omar','omar@gwu.edu','1234567','CS',datetime.date.today())
#y = insertUser('Kim','kim@gwu.edu','112233','CS',datetime.date.today())
#y = insertUser('Julie','Julie@gwu.edu','112233','CS','2003-02-01')
#editCommentText("Download Java!!",2)
#result = selectPostTable()
#for row in result:
#     print ('\n',result.fetchall())

#print('---------------------------------')
#result = selectPostTable()
#print('---------------------------------')
#for row in result:
#     print ('\n',result.fetchall())

#result = getPost(1222)

#print(result)
#downVoteComment(5)
#result =getAllCommentsOfpost(1222)

#for row in result:
#     print (row)



print('---------------------------------')
print('---------------------------------')
print('---------------------------------')
print('---------------------------------')
result = selectPostTableOrderByDate("downvote")
for row in result:
     print (row)
