from app.main.views import main_bp
from flask import request, jsonify, url_for, Blueprint
from flask_login import login_required, current_user
from app.main.models import Post, User, Like

bp_for_api = Blueprint('api', __name__, url_prefix='/api')

@bp_for_api.route('/like-post', methods=['POST','GET'])
def like_post():

    post_id = request.args.get('postid')
    like_status = request.args.get('like_status')

    like_object = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if like_object: # თუ იოუზერს უკვე ააქვს დალაიქებული ეს პოსტი 
        if like_status == 'like':
            # თუ ლაიქის ღილაკს დააჭირა მოწმება თუ like_status აქტიური არ არის ლაიქდება და თუ like_status აქტიურია unlike
            if like_object.like_status != 'active':
                like_object.like_status = 'active'
                like_object.update()
                post_likes_count = Like.query.filter_by(post_id=post_id, like_status='active').count()
                return jsonify(liked_by_current_user=True, post_likes_count=post_likes_count)
            else:
                like_object.like_status = 'disabled'
                like_object.update()
                post_likes_count = Like.query.filter_by(post_id=post_id, like_status='active').count()
                return jsonify(liked_by_current_user=False, post_likes_count=post_likes_count)
        elif like_status == 'unlike':
            # თუ დისლაიქის ბათნია active > disabled
            if like_object.like_status == 'active':
                like_object.like_status = 'disabled'
                like_object.update()
                post_likes_count = Like.query.filter_by(post_id=post_id, like_status='active').count()
                return jsonify(liked_by_current_user=False, post_likes_count=post_likes_count)
            else:
                like_object.like_status = 'active'
                like_object.update()
                post_likes_count = Like.query.filter_by(post_id=post_id, like_status='active').count()
                return jsonify(liked_by_current_user=True, post_likes_count=post_likes_count)
    else:
        like = Like(post_id=post_id, user_id=current_user.id, like_status='active')
        like.create()
        user_from_post = Post.query.filter_by(id=post_id).first()
        post_type = user_from_post.post_type
        poster_user_id = user_from_post.user_id
        if poster_user_id != current_user.id:
            if post_type == 'normal':
                poster_user = User.query.filter_by(id=poster_user_id).first()
                poster_user.flask_coin += 10
                poster_user.update()
                current_user.flask_coin += 5
                current_user.update()
            elif post_type == 'anonym':
                poster_user = User.query.filter_by(id=poster_user_id).first()
                poster_user.flask_coin += 20
                poster_user.update()
                current_user.flask_coin += 5
                current_user.update()
            else:
                poster_user = User.query.filter_by(id=poster_user_id).first()
                poster_user.flask_coin += 25
                poster_user.update()
                current_user.flask_coin += 5
                current_user.update()
            post_likes_count = Like.query.filter_by(post_id=post_id, like_status='active').count()
            return jsonify(liked_by_current_user=True, post_likes_count=post_likes_count)
        else:
            post_likes_count = Like.query.filter_by(post_id=post_id, like_status='active').count()
            return jsonify(liked_by_current_user=True, post_likes_count=post_likes_count)

@bp_for_api.route('/get-balance', methods=['POST','GET'])
@login_required
def get_balance():
    return jsonify(user_balance=current_user.flask_coin)