from flask import Blueprint,render_template

bp=Blueprint('inventory',__name__,url_prefix='/inventory')


@bp.route('/item/<int:id>')
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