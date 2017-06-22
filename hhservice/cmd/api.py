
from hhservice import api

def main():
    options = api.get_program_options()
    app = api.create_app()

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
