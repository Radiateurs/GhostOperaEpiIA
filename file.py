import helper


class File:

    def __init__(self, jid: int):
        self._world = helper.World(jid)
        self._world.init_file()

    # Read question.
    def readQuestion(self):
        question = self._world.pull_question()
        return self._world.parse_question(question)

    # Write response.
    def writeResponse(self, response):
        self._world.push_response(response)
