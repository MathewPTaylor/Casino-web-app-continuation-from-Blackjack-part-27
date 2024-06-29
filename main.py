from casinoapp import app, socketio


if __name__ == "__main__":
  socketio.run(app, host='0.0.0.0', port=81, debug=True)
  # app.run(host='0.0.0.0', port=81, debug=True)



mylambda = lambda x, y: print(x, y)

# suck your mum