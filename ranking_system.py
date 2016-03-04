
def score(ups, downs):
    return (ups - downs)

def top_rank(post):
	rank = score(post.upvote, post.downvote)
	return rank
