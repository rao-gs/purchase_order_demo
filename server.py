from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'po_db')
app.secret_key = "ThisIsSecret"
# @app.route('/')
# return redirect('/purchasing')


@app.route('/')
def reroute():
    return redirect('/POS')

@app.route('/POS')
def index():
    result = mysql.query_db("SELECT * FROM po_header ORDER BY po_header_id DESC")
    return render_template('index.html', result=result)

@app.route('/POS/new')
def new():
    result = mysql.query_db("SELECT * FROM po_header ORDER BY po_header_id DESC")
    return render_template('new.html', result=result)

@app.route('/POS', methods=["POST"])
def create():
    query = "INSERT INTO po_header (company_code, supplier_id, supplier_desc, payment_term, gr_text) VALUES (:company_code, :supplier_id, :supplier_desc, :payment_term, :gr_text)"
    data = {
        'company_code': request.form['company_code'],
        'supplier_id': request.form['supplier_id'],
        'supplier_desc': request.form['supplier_desc'],
        'payment_term': request.form['payment_term'],
        'gr_text': request.form['gr_text']
    }
    po_header_id = mysql.query_db(query, data)
    query1 = "INSERT INTO po_item (po_header_id, sr_no, prod_desc, qty, price_purch, price_total_item) VALUES (:po_header_id, :sr_no, :prod_desc, :qty, :price_purch, :price_total_item)"
    data1 = {
        "po_header_id": po_header_id,
        'sr_no': request.form['sr_no'],
        'prod_desc': request.form['prod_desc'],
        'qty': request.form['qty'],
        'price_purch': request.form['price_purch'],
        'price_total_item': float(request.form['qty']) * float(request.form['price_purch'])
    }
    po_item = mysql.query_db(query1, data1)
    # print '/countries/'+str(country_id)
    return redirect('/POS/'+str(po_header_id))

@app.route('/POS/<po_header_id>')
def show(po_header_id):
    result = mysql.query_db("SELECT * FROM po_header WHERE po_header_id = {}".format(po_header_id))
    result_i = mysql.query_db("SELECT * FROM po_item WHERE po_header_id = {}".format(po_header_id))
    # print result_i
    # [{'name':'Legoland', 'population':500000}]
    return render_template('show.html', po_header=result[0], po_item=result_i[0])


@app.route('/POS/<po_header_id>/edit')
def edit(po_header_id):
    # print po_header_id
    query = "SELECT * FROM po_header LEFT JOIN po_item on po_header.po_header_id = po_item.po_header_id WHERE po_header.po_header_id = :po_header_id"
    data = {
        'po_header_id': po_header_id
    }
    po_header = mysql.query_db(query, data) # [{}]
    # print po_header
    query1 = "SELECT * FROM po_item WHERE po_header_id = :po_header_id"
    data1 = {
        'po_header_id': po_header_id
    }
    po_item = mysql.query_db(query1, data1) # [{}]
    # print po_item
    # if po_item != '0' :
    return render_template('edit.html', po_header=po_header[0], po_item=po_item[0])
    # else:
    #     return render_template('edit.html', po_header=po_header[0])
    # return redirect('/POS/edit/'+str(po_header_id))

@app.route('/POS/<po_header_id>/edit', methods=["POST"])
def update(po_header_id):
    print po_header_id

    query = "UPDATE po_header SET company_code = :company_code, supplier_id = :supplier_id, supplier_desc = :supplier_desc, payment_term = :payment_term, gr_text = :gr_text WHERE po_header_id = :po_header_id"
    data = {
        'company_code': request.form['company_code'],
        'supplier_id': request.form['supplier_id'],
        'supplier_desc': request.form['supplier_desc'],
        'payment_term': request.form['payment_term'],
        'gr_text': request.form['gr_text'],
        'po_header_id': po_header_id
    }
    print data
    mysql.query_db(query, data)

    query1 = "UPDATE po_item SET sr_no = :sr_no, prod_desc = :prod_desc, qty = :qty, price_purch = :price_purch, price_total_item = :price_total_item WHERE po_header_id = :po_header_id"
    data1 = {
        'sr_no': request.form['sr_no'],
        'prod_desc': request.form['prod_desc'],
        'qty': request.form['qty'],
        'price_purch': request.form['price_purch'],
        'price_total_item': float(request.form['qty']) * float(request.form['price_purch']),
        "po_header_id": po_header_id
    }
    print data1
    po_item = mysql.query_db(query1, data1)
    return redirect('/POS')

@app.route('/POS/<po_header_id>/delete', methods=["POST"])
def destroy(po_header_id):

    query1 = "DELETE FROM po_item WHERE po_header_id = :po_header_id LIMIT 1"
    data1 = {
        'po_header_id': po_header_id
    }
    mysql.query_db(query1, data1)
    query = "DELETE FROM po_header WHERE po_header_id = :po_header_id LIMIT 1"
    data = {
        'po_header_id': po_header_id
    }
    mysql.query_db(query, data)

    return redirect('/POS')

# @app.route('/')
# def po_display():
#     # data1 = int(request.form['user_num'])
#     # query = "SELECT * FROM po_header"
#     session['id'] = request.form['po_header_id']

#     print session['id']

#     query = "SELECT * from po_item LEFT JOIN po_header ON po_item.po_header_id = po_header.po_header_id WHERE po_header.po_header_id = 'session[id]' "
#     data = {
#         po.header
#     }
#     # where po_header_id = data1"
#     # data1 = {
#     #         'po_header_id': request.form['po_header_id']
#     #         }          # define your query

#     results1 = mysql.query_db(query)
#                           # run query with query_db()
#     # print results
#     # query1 = "SELECT * from po_item where po_item.po_header_id = po_header.po_header_id"
#     # print query1
#     # # print query1
#     # po_item_results = mysql.query_db(query1)
#     return render_template('index.html', results=results[0]) # pass data to our template
    # po_item_results=po_item_results[0]


# @app.route('/getPO', methods=['POST'])
# def po_edit():
#     # session['id'] == { "po_header_id" : { request.form['po_header_id'] }
#     session['id'] = request.form['po_header_id']

#         # +po_header_id
#     # data1 = int(request.form['user_num'])
#     # query = "SELECT * FROM po_header"
#     # po_header_id = sesssion['po_header_id']
#     # print po_header_id
#     # x = po_header_id
#     po_header_id = session['id']
#     print po_header_id
#     return redirect('/getPO/'+str(po_header_id))

# @app.route('/getPO/<po_header_id>')
# def po_display1(po_header_id):

#     # print po_header_id

#     # results = mysql.query_db("SELECT * FROM po_header where po_header_id = {}".format(po_header_id))
#     results = mysql.query_db("SELECT * FROM po_header where po_header_id = {}".format(po_header_id))

#     po_item_results = mysql.query_db("SELECT * from po_item where po_header_id = {}".format(po_header_id))
#     # print po_item_results
#     # po_item_results = mysql.query_db(query1)
#     # results = mysql.query_db("SELECT * FROM po_header")
#     return render_template('index.html', results=results[0], po_item_results =po_item_results[0]) # pass data to our template
#     po_header_id = session['id']
#     print po_header_id
#     return redirect('/getPO/edit/'+str(po_header_id))


# @app.route('/pos/create', methods=['POST'])
# def create():
#     # Write query as a string. Notice how we have multiple values
#     # we want to insert into our query.
#     # session['po_hdeader_id'] = request.form['po_header_id']
#     if session['id'] != 0:
#         query = "INSERT INTO po_header (company_code, supplier_id) VALUES (:company_code, :supplier_id)"
#         # We'll then create a dictionary of data from the POST data received.
#         data = {
#                  # 'po_header_id': request.form['po_header_id'],
#                  'company_code':  request.form['company_code'],
#                  'supplier_id': request.form['supplier_id']
#                }
#         # Run query, with dictionary values injected into the query.
#         po = mysql.query_db(query, data)

#         print data

#         print po
#         # po_header_id1 = request.form['po_header_id1']
#         # # po_header_id2 = int(po_header_id1)
#         # item_query = "INSERT INTO po_item (prod_desc, po_header_id) VALUES (:prod_desc, :po_header_id)"
#         # # We'll then create a dictionary of data from the POST data received.
#         # item_data = {
#         #          # 'po_item_id': request.form['po_item_id'],
#         #          'prod_desc':  request.form['prod_desc'],
#         #           'po_header_id': session['id']
#         #        }
#         # # Run query, with dictionary values injected into the query.
#         # mysql.query_db(item_query, item_data)

#         return redirect('/')
#     else:
#         return redirect('/')

# @app.route('/pos/edit/<po_header_id>', methods=['POST'])
# def update(po_header_id):
#     query = "UPDATE po_header SET supplier_id = :supplier_id, company_code = :company_code where po_header_id = :po_header_id"
#     data = {
#                  'company_code':  request.form['company_code'],
#                  'supplier_id': request.form['supplier_id'],
#                  'po_header_id': po_header_id
#     }
#     po_edit = mysql.query_db(query, data)

#     return render_template('/')
    # return jsonify(po_edit)


app.run(debug=True)
