from flask import Blueprint,render_template,redirect,session
from app.sample_form import SampleForm

bp=Blueprint('',__name__)

def track_views():
    if 'views' in session:
        session['views']=session.get('views')+1
    else:
        session['views']=1


@bp.route('/')
def index():
    track_views()
    return render_template('page.html', title='Welcome!')


@bp.route('/help')
def help():
    track_views()
    return render_template('page.html', title='Help!')


@bp.route('/views')
def views():
    return f'Total Views: {session.get("views")}'


@bp.route('/views/reset')
def reset_views():
    views = session.pop('views',None)
    return f'Reset Views (previously {views})'


@bp.route('/form', methods=['GET', 'POST'])
def form():
    # load form from Jinja template
    form = SampleForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('form.html', form=form)