import os
from app import app
from Clientes import cliente
from login import login
from Destinos import destino
from Reserva import reserva
from user import user

app.register_blueprint(cliente)
app.register_blueprint(login)
app.register_blueprint(destino)
app.register_blueprint(reserva)
app.register_blueprint(user)


# starting the app
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
