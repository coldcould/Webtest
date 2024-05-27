from flask import Blueprint, render_template, request, current_app, url_for, redirect

from bluelog.extensions import db
from bluelog.forms import CommentForm
from bluelog.models import Post, Category, Comment

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/', defaults={'page': 1})
@blog_bp.route('/page/<int:page>')
def index(page):
    # page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination =Post.query.order_by(Post.timestamp.desc()).paginate(page=page,per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)

@blog_bp.route('/about/')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.
                                desc()).paginate(page=page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category,
                           pagination=pagination, posts=posts)



@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).order_by(Comment.timestamp.asc()).paginate(page=page,per_page=per_page)
    comments = pagination.items

    # 发表评论
    # if current_user.is_authenticated: # 如果用户已登录
    #     pass
    form = CommentForm()

    if form.validate_on_submit():
        author = form.author.data
        body = form.body.data
        comment = Comment(
            author=author, body=body, post=post
        )
        replied_id = request.args.get('reply')
        if replied_id: # 如果URL中reply查询参数存在， 那么说明是回复
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)

@blog_bp.route('/reply_comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('.show_post', post_id=comment.post_id, reply=comment_id,
                            author=comment.author) + '#comment-form')


@blog_bp.route('/testbase/')
def base():
    return render_template('base.html')

@blog_bp.route('/example/')
def example():
    return render_template('example.html')


