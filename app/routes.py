from flask import render_template,redirect
from app import app
from app.sample_form import SampleForm

@app.route('/')
def index():
    return render_template('page.html', title='Welcome!')

@app.route('/help')
def help():
    return render_template('page.html', title='Help!')

@app.route('/item/<int:id>')
def item(id):
    if 0<id<100:
        item={
            "id": id,
            "name": f"Fancy Item {id}",
            "description": "A Description of the Item"
        }
        return render_template('item.html', item=item)
    else:
        return '<h1>Not Found</h1>'
    
@app.route('/form', methods=['GET', 'POST'])
def form():
    # load form from Jinja template
    form = SampleForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('form.html', form=form)