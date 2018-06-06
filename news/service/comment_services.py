from news.models import Comment


def delete_comment(comment_id, user_id):
    comment = Comment.objects.get(id=comment_id)
    if comment.user.user.id == user_id:
        comment.delete()


def get_comments_by_item(item_id):
    return Comment.objects.filter(item_id=item_id)
