from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User, Blog
from flask_login import login_user, current_user, logout_user, login_required


bp = Blueprint('routes', __name__)


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(username=data['username'], email=data['email'],         password=hashed_password)

    db.session.add(user)
    db.session.commit()
    
    return jsonify(message="User registered successfully"), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify(message="Login successful"), 200
    return jsonify(message="Login failed"), 401


@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message="Logout successful"), 200


@bp.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    #if user_id != current_user.id:
     #   return jsonify(message="Unauthorized"), 401
    
    user = User.query.get(user_id)
    print(user)
    return jsonify(user.to_dict()), 200


@bp.route('/create-blog', methods=['POST'])
@login_required
def create_blog():
    data = request.get_json()
    blog = Blog(title=data['title'], content=data['content'], author_id=current_user.id)

    db.session.add(blog)
    db.session.commit()
    return jsonify(message="Blog post created successfully"), 201


@bp.route('/blog/<int:blog_id>', methods=['GET'])
@login_required
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    print(blog)
    return jsonify(blog.to_dict()), 200



@bp.route('/blog/update/<int:blog_id>', methods=['POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    if blog.author_id != current_user.id:
       return jsonify(message="Unauthorized"), 401
    
    data = request.get_json()
    blog.title = data['title']
    blog.content = data['content']

    db.session.commit()
    return jsonify(message="Blog post updated successfully"), 200



@bp.route('/blog/delete/<int:blog_id>', methods=['DELETE'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    
    if blog.author_id != current_user.id:
       return jsonify(message="Unauthorized"), 401
    
    db.session.delete(blog)
    db.session.commit()

    return jsonify(message="Blog post deleted successfully"), 200