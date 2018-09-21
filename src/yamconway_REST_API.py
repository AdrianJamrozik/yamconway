from flask import Flask
from flask_restful import Resource, Api
from yamconwaylib import YamConway

app = Flask(__name__)
api = Api(app)
yc = YamConway()


class BoardState(Resource):
    def get(self):
        yc.next_turn()
        return yc.board1


class GetNetworkBoard(Resource):
    def get(self):
        return yc.get_network_board()


class NextTurn(Resource):
    def get(self):
        yc.next_turn()
        return yc.get_network_board()


class Reset(Resource):
    def get(self):
        global yc
        yc = YamConway()
        return yc.board1


api.add_resource(GetNetworkBoard, '/networkboardstate')  # Route_1
api.add_resource(BoardState, '/boardstate')  # Route_1
api.add_resource(NextTurn, '/nextturn')  # Route_1
api.add_resource(Reset, '/reset')

if __name__ == '__main__':
    app.run(port='5002')
