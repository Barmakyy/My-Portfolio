from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.admin import bp
from app.admin.forms import ProjectForm, BlogPostForm
from app.models import Project, BlogPost, ContactMessage, User
from werkzeug.utils import secure_filename
import os
from slugify import slugify
from datetime import datetime

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@bp.route('/')
@login_required
@admin_required
def index():
    projects_count = Project.query.count()
    posts_count = BlogPost.query.count()
    messages_count = ContactMessage.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    return render_template('admin/index.html',
                         projects_count=projects_count,
                         posts_count=posts_count,
                         messages_count=messages_count,
                         unread_messages=unread_messages,
                         now=datetime.utcnow())

# Project management routes
@bp.route('/projects')
@login_required
@admin_required
def projects():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', 
                         projects=projects,
                         now=datetime.utcnow())

@bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            github_url=form.github_url.data,
            demo_url=form.demo_url.data,
            tags=form.tags.data
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            project.image_url = filename
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', 
                         form=form, 
                         title='New Project',
                         now=datetime.utcnow())

@bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.github_url = form.github_url.data
        project.demo_url = form.demo_url.data
        project.tags = form.tags.data
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            project.image_url = filename
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    return render_template('admin/project_form.html', 
                         form=form, 
                         title='Edit Project',
                         now=datetime.utcnow())

@bp.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# Blog post management routes
@bp.route('/posts')
@login_required
@admin_required
def posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/posts.html', 
                         posts=posts,
                         now=datetime.utcnow())

@bp.route('/posts/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            slug=slugify(form.title.data),
            author=current_user
        )
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.image_url = filename
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('admin.posts'))
    return render_template('admin/post_form.html', 
                         form=form, 
                         title='New Post',
                         now=datetime.utcnow())

@bp.route('/posts/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    form = BlogPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.slug = slugify(form.title.data)
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            form.image.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post.image_url = filename
        db.session.commit()
        flash('Post updated successfully!', 'success')
        return redirect(url_for('admin.posts'))
    return render_template('admin/post_form.html', 
                         form=form, 
                         title='Edit Post',
                         now=datetime.utcnow())

@bp.route('/posts/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', 'success')
    return redirect(url_for('admin.posts'))

# Contact message management routes
@bp.route('/messages')
@login_required
@admin_required
def messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', 
                         messages=messages,
                         now=datetime.utcnow())

@bp.route('/messages/<int:id>/read')
@login_required
@admin_required
def mark_message_read(id):
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    flash('Message marked as read!', 'success')
    return redirect(url_for('admin.messages'))

@bp.route('/messages/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin.messages')) 