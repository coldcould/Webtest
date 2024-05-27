from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from flask_login import login_required

from bluelog.extensions import db
from bluelog.forms import PostForm
from bluelog.models import Post, Category
from bluelog.utils import redirect_back

# ???这边的__name__是什么意思
admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
@login_required
def login_protect():
    pass

@admin_bp.route('/settings/')
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/post/new/', methods=['GET','POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category)
        db.session.add(post)
        db.session.commit()
        flash('Post created.','success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    return render_template('admin/new_post.html', form=form)

@admin_bp.route('/post/<int:post_id>/edit/', methods=['GET', 'POST'])
def edit_post(post_id):
    form = PostForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash('Post updated.', 'success')
        return redirect(url_for('blog.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('admin/edit_post.html', form=form)

@admin_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted.', 'success')
    return redirect(request.args.get('next'))

@admin_bp.route('/new_category/')
def new_category():
    return render_template('base.html')

@admin_bp.route('/post/manage')
def manage_post():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['BLUELOG_MANAGE_POST_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/manage_post.html', pagination=pagination,
                           posts=posts)

@admin_bp.route('/manage_category/')
def manage_category():
    pass

@admin_bp.route('/manage_comment/')
def manage_comment():
    pass

