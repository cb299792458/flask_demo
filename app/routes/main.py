from flask import Blueprint,render_template,redirect
from app.sample_form import SampleForm

bp=Blueprint('',__name__)

@bp.route('/')
def index():
    return render_template('page.html', title='Welcome!')


@bp.route('/help')
def help():
    return render_template('page.html', title='Help!')

    
@bp.route('/form', methods=['GET', 'POST'])
def form():
    # load form from Jinja template
    form = SampleForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('form.html', form=form)