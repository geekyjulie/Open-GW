

class Post():

	def __init__(self, questionID, upVote, downVote, commentNumber):
		self.questionID = questionID
		self.upVote = upVote
		self.downVote = downVote
		self.commentNumber = commentNumber
		

class Comment():

    def __init__(self, commentID, upVote, downVote):
        self.commentID = commentID
        self.upVote = upVote
        self.downVote = downVote
