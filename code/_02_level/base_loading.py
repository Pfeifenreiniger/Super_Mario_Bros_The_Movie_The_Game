

class BaseLoading:
    def __init__(self):
        self.loading = False

    def check_loading_progression(self):
        if not isinstance(self, type(None)):
            self.loaded = True