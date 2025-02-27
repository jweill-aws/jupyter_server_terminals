import json

from jupyter_server.base.handlers import APIHandler
from tornado import web


class TerminalRootHandler(APIHandler):
    @web.authenticated
    def get(self):
        models = self.terminal_manager.list()
        self.finish(json.dumps(models))

    @web.authenticated
    def post(self):
        """POST /terminals creates a new terminal and redirects to it"""
        data = self.get_json_body() or {}

        model = self.terminal_manager.create(**data)
        self.finish(json.dumps(model))


class TerminalHandler(APIHandler):
    SUPPORTED_METHODS = ("GET", "DELETE")

    @web.authenticated
    def get(self, name):
        model = self.terminal_manager.get(name)
        self.finish(json.dumps(model))

    @web.authenticated
    async def delete(self, name):
        await self.terminal_manager.terminate(name, force=True)
        self.set_status(204)
        self.finish()
