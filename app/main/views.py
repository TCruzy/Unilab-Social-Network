import random
from flask import redirect, render_template, request, url_for, Blueprint, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import login_manager
from app.main.models import User, Follow, Post, Like
from app.main.forms import LoginForm, Registrationform
from app.main.models import User
from flask_bcrypt import Bcrypt
import os
import uuid


templates_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
images_folder_in_static_folder = os.path.join(static_folder, 'post-images')
pfp_folder_in_static_folder = os.path.join(static_folder, 'pfp')
print(pfp_folder_in_static_folder)
# print('templates_folder', templates_folder, 'static_folder', static_folder)
# Create blueprint

main_bp = Blueprint('main',
                    __name__,
                    template_folder=templates_folder,
                    static_folder=static_folder,
                    url_prefix='/')
                            
# register login manager with the application
@login_manager.user_loader
def load_user(user_id):
    # example 
    # This is User Model from your models file 
    # this function is called to load a user given an ID
    return User.query.get(user_id)

# Simple index page route
@main_bp.route('/')
@main_bp.route('/home')
@login_required
def index():
    # get all posts sorted by post_type and amount of likers
    # firstly, display all posts with post_type = 'vip' then display all posts with post_type = 'anonym' then display all posts with post_type = 'normal'
    # then sort all posts by amount of likers
    all_post = Post.query.all()

    posts_data = {
        'vip_posts': [],
        'anonym_posts': [],
        'normal_posts': []
    }
    for post in all_post:

        user = User.query.get(post.user_id)

        likers = [likers.user_id for likers in post.likers]
        likers_data = []
        for liker in likers:
            liker_data = Like.query.filter_by(user_id=liker,like_status='active',post_id=post.id).first()
            if liker_data:
                like_user = User.query.get(liker_data.user_id)
                likers_data.append(like_user)
        like_object = Like.query.filter_by(post_id=post.id, user_id=current_user.id).first()
        # ვამოწმებთ აქვს თუ არა დალაიქებული დალოგინებულ იუზერს
        if like_object:
            # თუ like_object აქტიურია ანუ დალაიქებულიაქვს
            if like_object.like_status == 'active':
                liked_by_current_user = True
            else: # თუ like_object არაა აქტიური და disabled ია, ანუ დისლაიქი აქვს გაკეთებული
                liked_by_current_user = False
        else: # თუ like_object არაა , იუზერს არ აქვს დალაიქებული პოსტი
            liked_by_current_user = False
        if post.post_type == 'vip':
            posts_data['vip_posts'].append({
                'id': post.id,
                'user_id': post.user_id,
                'user_name': user.username,
                'user_image': user.user_image,
                'post_text': post.post_text,
                'post_image': post.post_image,
                'post_date': post.post_date,
                'post_type': post.post_type,
                'likers': likers_data,
                'likes_count': len(likers_data),
                'liked_by_me': liked_by_current_user
            })
        elif post.post_type == 'anonym':
            posts_data['anonym_posts'].append({
                'id': post.id,
                'user_id': post.user_id,
                'user_name': user.username,
                'user_image': user.user_image,
                'post_text': post.post_text,
                'post_image': post.post_image,
                'post_date': post.post_date,
                'post_type': post.post_type,
                'likers': likers_data,
                'likes_count': len(likers_data),
                'liked_by_me': liked_by_current_user
            })
        elif post.post_type == 'normal':
            posts_data['normal_posts'].append({
                'id': post.id,
                'user_id': post.user_id,
                'user_name': user.username,
                'user_image': user.user_image,
                'post_text': post.post_text,
                'post_image': post.post_image,
                'post_date': post.post_date,
                'post_type': post.post_type,
                'likers': likers_data,
                'likes_count': len(likers_data),
                'liked_by_me': liked_by_current_user
            })
    #
    return render_template('posts.html', all_post=posts_data)

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    loginform = LoginForm()
    registrationform = Registrationform()
    if request.method == 'POST':
        if loginform.validate_on_submit():
            email = loginform.email.data
            password = loginform.password.data
            user = User.query.filter_by(email=email).first()
            if user is not None:
                password_from_db = user.password
                check_password = Bcrypt().check_password_hash(password_from_db, password)
                if check_password:
                    login_user(user)
                    return redirect(url_for('main.index'))
                else:
                    flash('Invalid password')
                    return redirect(url_for('main.login'))
                    
            else:
                flash('Invalid username or password')
                return redirect(url_for('main.login'))
        else:
            return render_template('auth.html', loginform=loginform, registrationform=registrationform)

    return render_template('auth.html', loginform=loginform, registrationform=registrationform)

@main_bp.route('/signup', methods=['POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    registrationform = Registrationform()
    if registrationform.validate_on_submit():
        username = registrationform.username.data
        email = registrationform.email.data
        password = registrationform.password.data
        hashed_password = Bcrypt().generate_password_hash(password).decode('utf-8')
        user = User(username=username, password=hashed_password, email=email)
        user.create()
        flash('თქვენ წარმატებით დარეგისტრირდით', 'success')
        return redirect(url_for('main.login'))
    else:
        return render_template('auth.html', loginform=LoginForm(), registrationform=registrationform)

@main_bp.route('/delete-all-users', methods=['GET'])
def delete_all_users():
    users = User.query.all()
    for user in users:
        user.delete()
    return redirect(url_for('main.index'))

@main_bp.route('/create-post', methods=['POST'])
@login_required
def create_post():
    vip_post_price = 100
    anonym_post_price = 80
    normal_post_price = 50
    post_type = request.form['poster_type']
    post_text = request.form['post_content']
    post_image = request.files['post_image']
    if not post_type and not post_text:
        return redirect(url_for('main.index'))
    else:
        if post_type == 'vip':
            if current_user.flask_coin < vip_post_price:
                flash('You do not have enough Flask Coin to create a vip post')
                return redirect(url_for('main.index'))
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.flask_coin -= vip_post_price
            loggined_user.update()
            if post_image:
                image_uuid = str(uuid.uuid4())
                post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                new_post = Post(post_type=post_type, post_text=post_text, post_image=post_image_url,user_id=current_user.id)
                new_post.create()
            else:
                new_post = Post(post_type=post_type, post_text=post_text,user_id=current_user.id)
                new_post.create()

            return redirect(url_for('main.index'))
        elif post_type == 'anonym':
            if current_user.flask_coin < anonym_post_price:
                flash('You do not have enough Flask Coin to create a anonym post')
                return redirect(url_for('main.index'))
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.flask_coin -= anonym_post_price
            loggined_user.update()
            if post_image:
                image_uuid = str(uuid.uuid4())
                post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                new_post = Post(post_type=post_type, post_text=post_text, post_image=post_image_url,user_id=current_user.id)
                new_post.create()
            else:
                new_post = Post(post_type=post_type, post_text=post_text,user_id=current_user.id)
                new_post.create()

            return redirect(url_for('main.index'))
        elif post_type == 'normal':
            if current_user.flask_coin < normal_post_price:
                flash('You do not have enough Flask Coin to create a normal post')
                return redirect(url_for('main.index'))
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.flask_coin -= normal_post_price
            loggined_user.update()
            if post_image:
                image_uuid = str(uuid.uuid4())
                post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                new_post = Post(post_type=post_type, post_text=post_text, post_image=post_image_url,user_id=current_user.id)
                new_post.create()
            else:
                new_post = Post(post_type=post_type, post_text=post_text,user_id=current_user.id)
                new_post.create()

            return redirect(url_for('main.index'))
    return render_template('posts.html')

@main_bp.route('/user-profile')
@login_required
def user_profile():
    curr_user_liked_posts = Like.query.filter_by(user_id=current_user.id, like_status='active').all() # დალოგინებულმა იუზერმა რომელი პოსტებიც დაალაიქა
    curr_user_posts = Post.query.filter_by(user_id=current_user.id).all() # დალოგინებული იუზერის დადებული პოსტები
    curr_user_followers = Follow.query.filter_by(following_to_id=current_user.id, following_status='active').all() # დალოგინებული იუზერის ფოლოუერები
    curr_user_following = Follow.query.filter_by(following_from_id=current_user.id, following_status='active').all() # დალოგინებული იუზერი ვისაც აფოლოვებს
    user_liked_curr_posts = []
    for post in curr_user_posts:
        like_to_currents_post = Like.query.filter_by(post_id=post.id, like_status='active').all()
        if like_to_currents_post:
            user_liked_curr_posts.append(like_to_currents_post) # თუ რომეილიმე იუზერმა დალოგინებული იუზერის პოსტი დაალაიქა
        
    return render_template('user-profile.html', curr_user_posts=curr_user_posts,
                           curr_user_liked_posts=curr_user_liked_posts,
                           user_liked_curr_posts=user_liked_curr_posts,
                           curr_user_followers=curr_user_followers,
                           curr_user_following=curr_user_following)

@main_bp.route('/user-settings', methods=['GET', 'POST'])
@login_required
def user_settings():
    if request.method == 'GET':
        return render_template('user-settings.html')

@main_bp.route('/users-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def users_profile(user_id):
    if user_id == current_user.id:
        return redirect(url_for('main.user_profile'))
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return redirect(url_for('main.index'))
    current_user_following = Follow.query.filter_by(following_from_id=current_user.id, following_to_id=user_id, following_status='active').first()
    # only posts where post_type is not 'anonym'
    user_posts = Post.query.filter(Post.user_id == user_id, Post.post_type != 'anonym').all()
    user_liked_posts = Like.query.filter_by(user_id=user_id, like_status='active').all()
    user_followers = Follow.query.filter_by(following_to_id=user_id, following_status='active').all()
    user_followers_ids = [user_follower.following_from_id for user_follower in user_followers]
    user_following = Follow.query.filter_by(following_from_id=user_id, following_status='active').all()
    user_liked_it_posts = []
    for post in user_posts:
        like_to_currents_post = Like.query.filter_by(post_id=post.id, like_status='active').all()
        if like_to_currents_post:
            user_liked_it_posts.append(like_to_currents_post)
    return render_template('users-profile.html', user=user, user_posts=user_posts,
                           user_liked_posts=user_liked_posts, user_followers=user_followers,
                           user_following=user_following, user_liked_it_posts=user_liked_it_posts,
                           current_user_following=current_user_following, user_followers_ids=user_followers_ids)   


@main_bp.route('/change_pfp', methods=['GET', 'POST'])
@login_required
def change_pfp():
    if request.method == 'POST':
        pfp = request.files['profile_picture']
        if pfp:
            image_uuid = str(uuid.uuid4())
            pfp.save(os.path.join(pfp_folder_in_static_folder, image_uuid + f'{pfp.filename}'))
            pfp_url = url_for('static', filename='pfp/' + image_uuid + f'{pfp.filename}')
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.user_image = pfp_url
            loggined_user.update()
            flash('Profile picture changed successfully')
            return redirect(url_for('main.user_settings'))
        else:
            flash('Please select a profile picture')
            return redirect(url_for('main.user_settings'))

@main_bp.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    if request.method == 'POST':
        post = Post.query.filter_by(id=post_id).first()
        if post:
            post.delete()
            flash('Post deleted successfully')
            return redirect(url_for('main.index'))
        else:
            flash('Post not found')
            return redirect(url_for('main.index'))


@main_bp.route('/change_privacy', methods=['GET', 'POST'])
@login_required
def change_privacy():
    if request.method == 'POST':
        privacy = request.form.get('info_privacy')
        if privacy:
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.privacy = privacy
            loggined_user.update()
            flash('Privacy changed successfully')
            return redirect(url_for('main.user_settings'))
        else:
            flash('Please select a privacy')
            return redirect(url_for('main.user_settings'))
        
# edit post view, takes post_id as parameter
# then take poster_type and post_content from form
# then return edit-post.html
@main_bp.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if request.method == 'GET':
        print('get')
        post = Post.query.filter_by(id=post_id).first()
        if not post:
            print('post not found')
            return redirect(url_for('main.index'))
        return render_template('edit-post.html', post=post)
    elif request.method == 'POST':
        post_type = request.form.get('poster_type')
        post_text = request.form.get('post_content')
        
        post_image = request.files['post_image']
        post = Post.query.filter_by(id=post_id).first()
        if not post or not post_type or not post_text:
            flash('Please fill all fields')
            return redirect(url_for('main.index'))
        if post.post_type != 'vip' and post_type == 'vip':
            if current_user.flask_coin < 40:
                flash(f'You dont have enough coins to edit this post  {post.post_type} -> {post_type}')
                return redirect(url_for('main.index'))
            else:
                curr_user = User.query.filter_by(id=current_user.id).first()
                # თუ anonym იდან vip ზე გაანახლა -40 დააკლებს
                if post.post_type == 'anonym':
                    curr_user.flask_coin -= 40
                else:# თუ norm იდან vip ზე გაანახლა -50 დააკლებს
                    curr_user.flask_coin -= 50
                curr_user.update()
                post.post_type = post_type
                post.post_text = post_text
                if post_image:
                    image_uuid = str(uuid.uuid4())

                    post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                    post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                    post.post_image = post_image_url
                    post.update()
                    return redirect(url_for('main.index'))
                else:
                    post.update()
                    return redirect(url_for('main.index'))
        elif post.post_type != 'normal' and post_type == 'normal':
            curr_user = User.query.filter_by(id=current_user.id).first()
            if post.post_type == 'anonym':
                # თუ anonym იდან norm ზე გაანახლა +10 დაამატებს
                curr_user.flask_coin += 20
                curr_user.update()
            elif post.post_type == 'vip':
                # თუ vip იდან norm ზე გაანახლა +50 დაამატებს
                curr_user.flask_coin += 50
                curr_user.update()
            post.post_type = post_type
            post.post_text = post_text
            if post_image:
                image_uuid = str(uuid.uuid4())
                post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                post.post_image = post_image_url
                post.update()
                return redirect(url_for('main.index'))
            else:
                post.update()
                return redirect(url_for('main.index'))
        elif post.post_type != 'anonym' and post_type == 'anonym':
            curr_user = User.query.filter_by(id=current_user.id).first()
            if post.post_type == 'vip':
                # თუ vip იდან anonym ზე გაანახლა +20 დაამატებს
                curr_user.flask_coin += 20
            else:
                # თუ norm იდან anonym ზე გაანახლა -10 დააკლებს
                if current_user.flask_coin < 10:
                    flash(f'You dont have enough coins to edit this post {post.post_type} -> {post_type}')
                    return redirect(url_for('main.index'))
                curr_user.flask_coin -= 10
            curr_user.update()
            post.post_type = post_type
            post.post_text = post_text
            if post_image:
                image_uuid = str(uuid.uuid4())

                post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                post.post_image = post_image_url
                post.update()
                return redirect(url_for('main.index'))
            else:
                post.update()
                return redirect(url_for('main.index'))
        else:
            post.post_type = post_type
            post.post_text = post_text
            if post_image:
                image_uuid = str(uuid.uuid4())
                post_image.save(os.path.join(images_folder_in_static_folder, image_uuid + f'{post_image.filename}'))
                post_image_url = url_for('static', filename='post-images/' + image_uuid + f'{post_image.filename}')
                post.post_image = post_image_url
                post.update()
                return redirect(url_for('main.index'))
            else:
                post.update()
                return redirect(url_for('main.index'))
            
@main_bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        search_text = request.form.get('search')
        search_filter = request.form.get('search_filter')
        if search_filter == 'posts':
            if not search_text:
                flash('Please enter search text')
                return redirect(url_for('main.index'))
            posts = Post.query.filter(Post.post_text.like(f'%{search_text}%')).all()
            post_data = []
            for post in posts:
                user = User.query.filter_by(id=post.user_id).first()
                post_data.append({
                    'post': post,
                    'user': user
                })
                
            return render_template('search-post.html', posts=post_data)
        elif search_filter == 'users':
            if not search_text:
                flash('Please enter search text')
                return redirect(url_for('main.index'))
            users = User.query.filter(User.username.like(f'%{search_text}%')).all()
            return render_template('search-name.html', users=users)
    return render_template('search.html')

@main_bp.route('/leaderboard')
@login_required
def leaderboard():
    # get top 5 user by flask_coin.desc
    users = User.query.order_by(User.flask_coin.desc()).limit(5).all()
    user_data = []
    for user in users:
        post = Post.query.filter(Post.user_id == user.id, Post.post_type != 'anonym').all()
        user_data.append({
            'user': user,
            'posts': len(post)
        })
    return render_template('leaderboard.html', users=user_data)

@main_bp.route('/following/<int:user_id>', methods=['GET', 'POST'])
@login_required
def following(user_id):
    if user_id == current_user.id:
        return redirect(url_for('main.user_profile'))
    follow_status = request.form.get('follow_status')
    already_exists = Follow.query.filter_by(following_from_id=current_user.id, following_to_id=user_id).first()
    if follow_status == 'follow':
        if already_exists:
            already_exists.following_status = 'active'
            already_exists.update()
            return redirect(url_for('main.users_profile', user_id=user_id))
        else:
            follow = Follow(following_from_id=current_user.id, following_to_id=user_id)
            follow.create()
            user = User.query.filter_by(id=user_id).first()
            user.flask_coin += 10
            user.update()
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.flask_coin += 20
            loggined_user.update()
            return redirect(url_for('main.users_profile', user_id=user_id))
    elif follow_status == 'unfollow':
        follow = Follow.query.filter_by(following_from_id=current_user.id, following_to_id=user_id).first()
        follow.following_status = 'disabled'
        follow.update()
        return redirect(url_for('main.users_profile', user_id=user_id))
        
@main_bp.route('/play-for-earn')
@login_required
def play_for_earn():
    random_50_small_english_word = [
        'shallow', 'sudden', 'suspicious', 'sweater', 'swim', 'tall', 'taste', 'tender',
        'tense', 'terrible', 'test', 'thank', 'thick', 'thin', 'thirsty', 'thunder',
        'tired', 'tongue', 'tooth', 'toothbrush', 'toothpaste', 'tough', 'tower', 'toy', 
        'train', 'tray', 'treat', 'trouble', 'trousers', 'truck', 'trunk', 'truth', 'uncle', 
        'underwear', 'vacation', 'valuable', 'vase', 'vegetable', 'verse', 'vessel', 'victory', 
        'view', 'violent', 'voice', 'volcano', 'volleyball', 'voyage', 'wealth', 'weapon', 'weather', 
        'week', 'weight', 'wheel', 'whip', 'whistle', 'wind', 'window', 'wine', 'wire',
        'wise', 'wish', 'witness',
    ]
    random_25_big_english_word = [
        'friendship','government', 'society', 'education', 'environment', 'economy', 'politics', 'technology', 
        'population', 'communication', 'transportation', 'agriculture', 'industry', 'science', 'health', 
        'literature', 'sports', 'entertainment', 'military', 'religion', 'history', 
        'philosophy']
    rand_num = random.randint(0, 1)
    if rand_num == 0:
        random_word = random.choice(random_50_small_english_word)
        shuffled_word = ''.join(random.sample(random_word, len(random_word)))
        return render_template('play-for-earn.html', random_word=random_word, shuffled_word=shuffled_word)
    elif rand_num == 1:
        random_word = random.choice(random_25_big_english_word)
        shuffled_word = ''.join(random.sample(random_word, len(random_word)))
        return render_template('play-for-earn.html', random_word=random_word, shuffled_word=shuffled_word)

@main_bp.route('/check-word/<string:random_word>', methods=['GET', 'POST'])
@login_required
def check_word(random_word):
    word = request.form.get('word')
    random_50_small_english_word = [
        'shallow', 'sudden', 'suspicious', 'sweater', 'swim', 'tall', 'taste', 'tender',
        'tense', 'terrible', 'test', 'thank', 'thick', 'thin', 'thirsty', 'thunder',
        'tired', 'tongue', 'tooth', 'toothbrush', 'toothpaste', 'tough', 'tower', 'toy', 
        'train', 'tray', 'treat', 'trouble', 'trousers', 'truck', 'trunk', 'truth', 'uncle', 
        'underwear', 'vacation', 'valuable', 'vase', 'vegetable', 'verse', 'vessel', 'victory', 
        'view', 'violent', 'voice', 'volcano', 'volleyball', 'voyage', 'wealth', 'weapon', 'weather', 
        'week', 'weight', 'wheel', 'whip', 'whistle', 'wind', 'window', 'wine', 'wire',
        'wise', 'wish', 'witness',
    ]
    random_25_big_english_word = [
        'friendship','government', 'society', 'education', 'environment', 'economy', 'politics', 'technology', 
        'population', 'communication', 'transportation', 'agriculture', 'industry', 'science', 'health', 
        'literature', 'sports', 'entertainment', 'military', 'religion', 'history', 
        'philosophy']
    if not word:
        flash('Please enter a word', 'danger')
        return redirect(url_for('main.play_for_earn'))
    
    if word == random_word:
        if word in random_50_small_english_word:
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.flask_coin += 5
            loggined_user.update()
            flash('You are right, You Won 5 Flask Coin', 'success')
        else:
            loggined_user = User.query.filter_by(id=current_user.id).first()
            loggined_user.flask_coin += 10
            loggined_user.update()
            flash('You are right, You Won 15 Flask Coin', 'success')
        return redirect(url_for('main.play_for_earn'))
    else:
        flash('Incorrect! A new word appeared on the screen', 'danger')
        return redirect(url_for('main.play_for_earn'))
   
   
       
@main_bp.route('/anonymous')
@login_required
def anonymous():
    return render_template('anonymous.html')
        

# Logout route
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

