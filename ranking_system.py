
def score(ups, downs):
    return abs(ups - downs)

def top_rank(post):
	rank = score(post.upVote, post.downVote) + post.commentNumber
	return rank

def top_rank_comment(comment):
    rank = score(comment.upVote, comment.downVote)
    return rank
