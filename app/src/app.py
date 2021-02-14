import os
import csv
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Customer, Product, OrderStatus


from utils import process_order, insert_row

app = Flask(__name__)
app.config.from_pyfile('application.cfg')
db.init_app(app)
migrate = Migrate(app, db)

# VIEWS
@app.route('/')
def upload():
    return render_template("upload.html")


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file_obj = request.files['file']

        if file_obj.filename == '' or file_obj.filename.split('.')[-1] != 'tsv':
            error = 'Invalid file!'
            return render_template('upload.html', error=error)

        if file_obj:
            filename = secure_filename(file_obj.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_obj.save(file_path)

        with open(file_path) as order_data:
            reader = csv.reader(order_data, delimiter='\t')

            app.logger.info('Begin processing File')

            for row in reader:
                customer, product, order_status, previous_order = process_order(row)

                if not previous_order:
                    insert_row(db.session, Customer(**customer), app.logger)
                    db.session.commit()

                    insert_row(db.session, Product(**product), app.logger)
                    db.session.commit()

                    insert_row(db.session, OrderStatus(**order_status), app.logger)
                    db.session.commit()

                else:
                    order = OrderStatus.query.filter_by(status='new', **previous_order).first()

                    if order:
                        order.status = 'canceled'
                        order.updated_at = order_status['updated_at']
                    else:
                        app.logger.warn('Unable to load row: {}'.format(order_status))

                    db.session.commit()

        return redirect(url_for('uploaded_file', filename=filename))


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return render_template("upload_file.html")


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
