
from hhservice import api

def main():
    options = api.get_program_options()

    api.initial(api.app)

    api.app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
