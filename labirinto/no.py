class No:
    """

    """

    def __init__(self, posicao=None, pai=None, saida=None):
        """

        :param pos: Posicao
        :param pai: No
        :param g:
        :param h:
        """
        self.posicao = posicao
        self.saida = saida
        self.v_heuristico = 100000  # como nao foi iniciado considero um valor alto (longe)
        self.v_caminho = 0
        self.pai = None

        if pai:
            self.pai = pai
            _pai = pai
            while _pai:
                self.v_caminho += 1
                _pai = _pai.pai

        if saida:
            self.v_heuristico = (self.posicao.x ** 2) + (self.posicao.y ** 2) ** (1 / 2)

    def __eq__(self, other):
        return self.posicao.x == other.posicao.x and self.posicao.y == other.posicao.y

    def __le__(self, other):
        return self.v_heuristico <= other.v_heuristico

    def __lt__(self, other):
        return self.v_heuristico < other.v_heuristico

    def __gt__(self, other):
        return self.v_heuristico > other.v_heuristico

    def __ge__(self, other):
        return self.v_heuristico >= other.v_heuristico

    def __str__(self):
        return 'pos = %s, Heu. = %d, Camin. = %s \n' % (self.posicao, self.v_heuristico, self.v_caminho)

    def __repr__(self):
        return str(self)

    def pega_caminho(self):
        """
        Cria um array com todos os nos que percorreu ate chegar neste.
        :return:
        """
        _caminho = [self]
        _pai = self.pai
        while _pai:
            _caminho.insert(0, _pai)  # inserio no inicio da lista para ficar na posicao correta
            _pai = _pai.pai
        return _caminho
