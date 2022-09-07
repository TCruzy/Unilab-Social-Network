from flask_admin.contrib.sqla import ModelView


def formatter_posts_object(view, context, model, name):
    return len(model.posts)

def formatter_user_object_followers(view, context, model, name):
    return len(model.followers.all())

def formatter_user_object_following(view, context, model, name):
    return len(model.following.all())

def formatter_user_likes(view, context, model, name):
    return len(model.likes)

class UserView(ModelView):
    can_delete = True
    can_edit = True
    column_editable_list = ['username', 'email', 'flask_coin']
    edit_modal = True
    column_select_related_list = ['posts']
    column_display_all_relations = True
    form_choices = {
        'privacy': [
            ('public', 'Public'),
            ('private', 'Private'),
            ('followers', 'Followers')]}
    
    
    column_formatters = dict(posts=formatter_posts_object,
                             followers=formatter_user_object_followers,
                             following=formatter_user_object_following,
                             likes=formatter_user_likes)    

class PostView(ModelView):
    can_delete = False
    can_edit = True
    edit_modal = True
    column_display_all_relations = True
    can_create = True
    

class LikesView(ModelView):
    can_delete = False
    can_create = True 
    can_edit = True
    column_display_actions = True
    column_display_all_relations = True
    column_list = ['user', 'post']
    form_choices = {
        'like_status': [
            ('active', 'Active'),
            ('disabled', 'Disabled')
        ]
    }
    
class FollowsView(ModelView):
    can_delete = False
    # display all the columns in the table
    column_list = ['id', 'following_to_id', 'following_from_id']
    column_display_all_relations = True
    can_edit = True
    form_choices = {
        'following_status': [
            ('active', 'Active'),
            ('disabled', 'Disabled')
        ]
    }
    can_view_details = True
    column_auto_select_related = True
    column_display_pk = True
