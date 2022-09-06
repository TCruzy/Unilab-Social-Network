from flask_admin.contrib.sqla import ModelView



class UserView(ModelView):
    can_delete = False
    can_edit = True
    column_editable_list = ['username', 'email', 'flask_coin']
    edit_modal = True
    
    
    
class PostView(ModelView):
    can_delete = False

class LikesView(ModelView):
    can_delete = False
    form_choices = {
        'like_status': [
            ('active', 'Active'),
            ('disabled', 'Disabled')
        ]
    }
    
class FollowsView(ModelView):
    can_delete = False
    # display all the columns in the table
    column_list = ['id', 'following_to_id', 'following_from_id', 'timestamp']
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
