
from hhservice import web

def main():
    options = web.get_program_options()
    
    web.app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )
