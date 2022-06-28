class Logger:
    instance = None

    @staticmethod
    def get_logger():
        if Logger.instance is None:
            Logger.instance = Logger()
        return Logger.instance

    def info(self, *args):
        print("\u001b[31m[barb]", *args)

    def error(self, *args):
        print("[barb] ERROR:", *args)