from flask import Flask, render_template, request, make_response, jsonify
from web3 import Web3, HTTPProvider
from solc import compile_source
from web3.contract import ConciseContract
from uuid import uuid4
import time
import sudoku


def get_receipt(tx_hash):
    transaction_receipt = None
    while not transaction_receipt:
        time.sleep(1)
        transaction_receipt = w3.eth.getTransactionReceipt(tx_hash)
    return transaction_receipt


with open('sudoku_contract.sol', 'rb') as f:
    compiled_sol = compile_source(f.read())

contract_interface = compiled_sol['<stdin>:Sudoku']

time.sleep(10)
w3 = Web3(HTTPProvider("http://ganache:8545"))

contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
tr_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 4100000})

tx_receipt = get_receipt(tr_hash)
contract_address = tx_receipt['contractAddress']
contract_instance = w3.eth.contract(contract_interface['abi'], contract_address, ContractFactoryClass=ConciseContract)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('default.html')


@app.route('/game')
def game():
    game_id = uuid4()
    resp = make_response(render_template('game.html'))
    resp.set_cookie('game_id', str(game_id))
    return resp


@app.route('/ajax/start', methods=['GET', 'POST'])
def init():
    game_id = request.cookies.get('game_id')
    field = sudoku.gen_grid()
    preset = list(map(lambda x: x != 0, field))
    tx_hash = contract_instance.new_game(game_id, field, preset, transact={'from': w3.eth.accounts[0]})
    get_receipt(tx_hash)
    data = {"field": field, "preset": preset}
    return jsonify(data)


@app.route('/ajax/step', methods=['GET', 'POST'])
def step():
    game_id = request.cookies.get('game_id')
    cell = request.form.get('cell')
    value = request.form.get('value')
    if cell is None or value is None:
        return jsonify({"error": "gtfo hacker"})
    try:
        tx_hash = contract_instance.set_cell(game_id, int(cell), int(value), transact={'from': w3.eth.accounts[0]})
    except:
        return jsonify({"error": "something went wrong (probably because of you)"})
    get_receipt(tx_hash)
    field = contract_instance.get_field(game_id)
    data = {"field": field}
    if field.count(0) == 0:
        data['result'] = sudoku.check_grid(field)
    return jsonify(data)
