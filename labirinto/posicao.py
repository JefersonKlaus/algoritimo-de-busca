class Posicao:
    x = None
    Y = None

    def __init__(self, x, y):
        """
        :param x: posicao X
        :param y: posicao Y
        """
        self.x = x
        self.y = y

    def __str__(self):
        return 'x = %s, y = %s' % (self.x, self.y)
