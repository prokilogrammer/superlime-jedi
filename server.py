import jedi
import json
import cherrypy
import os

class PythonSuggestor(object):
    @cherrypy.expose
    def suggest(self, code=''):
        # Split code into lines and remove any empty line at the end
        lines = code.split('\n')
        if len(lines) > 1 and lines[-1] == '':
            del lines[-1]

        lineno = len(lines)
        colno = len(lines[-1])

        script = jedi.Script(code, lineno, colno)
        completions = script.completions()

        result = []
        for comp in completions:
            result.append({'complete': comp.complete, 'name': comp.name})

        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        return json.dumps(result);

    @cherrypy.expose
    def index(self):
        return "Hello world"


if __name__ == '__main__':

    cherrypy.config.update({'server.socket_host': '0.0.0.0',})
    cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', 9000)),})
    cherrypy.quickstart(PythonSuggestor())
