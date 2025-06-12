from flask import render_template, request, flash, redirect, url_for
from app import db
from app.main import bp
from app.models import Project, BlogPost, ContactMessage
from app.main.forms import ContactForm
from datetime import datetime

@bp.route('/')
def index():
    featured_projects = Project.query.order_by(Project.created_at.desc()).limit(3).all()
    recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('main/index.html', 
                         featured_projects=featured_projects,
                         recent_posts=recent_posts,
                         now=datetime.utcnow())

@bp.route('/projects')
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('main/projects.html', 
                         projects=projects,
                         now=datetime.utcnow())

@bp.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=5, error_out=False)
    return render_template('main/blog.html', 
                         posts=posts,
                         now=datetime.utcnow())

@bp.route('/blog/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug).first_or_404()
    return render_template('main/blog_post.html', 
                         post=post,
                         now=datetime.utcnow())

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent! I will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('main/contact.html', 
                         form=form,
                         now=datetime.utcnow()) 