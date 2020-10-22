import random
import time
from copy import deepcopy


class Labirinto:
    # Use a breakpoint in the code line below to debug your script.
    dim_x = None  # int
    dim_y = None  # int
    labirinto = []  # matriz
    nos = []  # direcao que cada caminho pode ir

    tx_obstaculos = None
    posicao_atual = None  # Posicao
    posicao_saida = None  # Posicao

    def __init__(self, dim_x, dim_y, taxa_obstaculos=0.3) -> None:
        """
        0 = livre
        1 = obstaculo
        2 = entrada
        3 = saida
        :param dim_x: tamanho X
        :param dim_y: tamanho Y
        :param taxa_obstaculos: taxa de obstaculos 0 = 0% / 1 = 100%
        """
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.labirinto = [[Labirinto.__criar_obstaculo(taxa_obstaculos) for _ in range(dim_y)] for _ in range(dim_x)]

        self.posicao_atual = Posicao(x=int(random.random() * dim_x),
                                     y=int(random.random() * dim_y))

        self.labirinto[self.posicao_atual.x][self.posicao_atual.y] = 2

        self.posicao_saida = Posicao(x=int(random.random() * dim_x),
                                     y=int(random.random() * dim_y))

        self.labirinto[self.posicao_saida.x][self.posicao_saida.y] = 3

        # essa funcao nao eh obrigatoria
        self._mapea_nos()

    def _mapea_nos(self):
        """
        carrega um array com todas posiveis caminhos que cada no pode ir
           0  1  2  3
        0 [1, 0, 2, 0]
        1 [0, 0, 0, 3]
        2 [0, 1, 0, 1]
        3 [0, 1, 0, 0]

        [[4, 1], [5],  [1, 6, 3], [7],  [8, 5], [1, 4, 6], [5, 10, 7]... posicao que cada ponto da matriz pode ir

        Exemplo
        item 1 na posicao [0,0] da matriz, pode se deslocar para direita, posicao 1 no array ([5]) e para baixo posicao
        4 no array ([7])
        :return:
        """
        for index_linha, linha in enumerate(self.labirinto):
            for index_coluna, item in enumerate(linha):
                self.nos.append(self.__pega_vizinhos(index_linha, index_coluna))

    def __pega_vizinhos(self, index_linha, index_coluna, tipo_lista=True):
        """
        Retorna um array com os vizinhos
        :param index_linha:
        :param index_coluna:
        :return: Array<Posicao>
        """
        _posicoes = []
        if index_linha > 0:
            if self.labirinto[index_linha - 1][index_coluna] == 0 or \
                    self.labirinto[index_linha - 1][index_coluna] == 3:
                if tipo_lista:
                    _posicoes.append(self.__posicao_matriz_para_posicao_lista(index_linha - 1, index_coluna))
                else:
                    _posicoes.append(Posicao(x=index_linha - 1, y=index_coluna))

        if index_coluna > 0:
            if self.labirinto[index_linha][index_coluna - 1] == 0 or \
                    self.labirinto[index_linha][index_coluna - 1] == 3:
                if tipo_lista:
                    _posicoes.append(self.__posicao_matriz_para_posicao_lista(index_linha, index_coluna - 1))
                else:
                    _posicoes.append(Posicao(x=index_linha, y=index_coluna - 1))

        if index_linha < len(self.labirinto) - 1:
            if self.labirinto[index_linha + 1][index_coluna] == 0 or \
                    self.labirinto[index_linha + 1][index_coluna] == 3:
                if tipo_lista:
                    _posicoes.append(self.__posicao_matriz_para_posicao_lista(index_linha + 1, index_coluna))
                else:
                    _posicoes.append(Posicao(x=index_linha + 1, y=index_coluna))

        if index_coluna < len(self.labirinto[0]) - 1:
            if self.labirinto[index_linha][index_coluna + 1] == 0 or \
                    self.labirinto[index_linha][index_coluna + 1] == 3:
                if tipo_lista:
                    _posicoes.append(self.__posicao_matriz_para_posicao_lista(index_linha, index_coluna + 1))
                else:
                    _posicoes.append(Posicao(x=index_linha, y=index_coluna + 1))
        return _posicoes

    def __posicao_matriz_para_posicao_lista(self, index_linha, index_coluna):
        """
        Pega a posicao da matriz e retorna a posicao como se fosse uma lista
        :param index_linha:
        :param index_coluna:
        :return:
        """
        return index_linha * len(self.labirinto) + index_coluna

    def imprimir_labirinto(self, labirinto=None):
        """
        imprime o labirinto de forma mais visual
        :return:
        """
        _labirinto = deepcopy(labirinto) if labirinto else deepcopy(self.labirinto)
        try:
            print('   ' + '  '.join([str(numero) for numero in range(len(_labirinto))]))
            [print(numero, linha) for numero, linha in enumerate(_labirinto)]
        except:
            print('----ERRO----')
            print(_labirinto)
            print('----ERRO----')

    def desenha_labirinto(self, labirinto=None):
        """
        imprime o labirinto apenas para visualizar
        :return:
        """
        _temp = deepcopy(labirinto) if labirinto else deepcopy(self.labirinto)

        for linha in range(self.dim_x):
            for coluna in range(self.dim_y):
                if _temp[linha][coluna] == 0:
                    _temp[linha][coluna] = '     |'

                if _temp[linha][coluna] == 1:
                    _temp[linha][coluna] = '+++++|'

                if _temp[linha][coluna] == 2:
                    _temp[linha][coluna] = '  E  |'

                if _temp[linha][coluna] == 3:
                    _temp[linha][coluna] = '  S  |'

                if _temp[linha][coluna] == 8:
                    _temp[linha][coluna] = '  *  |'

        [print(linha) for linha in _temp]

    def faz_busca_em_largura(self,
                             labirinto=None,
                             no=None,
                             caminho_percorrido=[],
                             print_map=False):
        """
        faz busca em largura e imprime o passo a passo
        :param caminho_percorrido:
        :param print_map:
        :param labirinto:
        :param no:
        :return:
        """

        _no_atual = None
        _temp_labirinto = deepcopy(self.labirinto) if labirinto is None else labirinto

        if no is None:
            _no_atual = No(posicao=self.posicao_atual, saida=self.posicao_saida)
        else:
            _no_atual = no

        if _no_atual.posicao.x < 0 or _no_atual.posicao.x >= self.dim_x:
            return False

        if _no_atual.posicao.y < 0 or _no_atual.posicao.y >= self.dim_y:
            return False

        if print_map:
            time.sleep(0.1)
            print('\n')
            self.desenha_labirinto(labirinto=_temp_labirinto)

        # obsatculo
        if int(_temp_labirinto[_no_atual.posicao.x][_no_atual.posicao.y]) == 1:
            return False

        # ja passou por aqui
        if int(_temp_labirinto[_no_atual.posicao.x][_no_atual.posicao.y]) == 8:
            return False

        # achou a saida
        if int(_temp_labirinto[_no_atual.posicao.x][_no_atual.posicao.y]) == 3:
            caminho_percorrido.append([_no_atual.posicao.x, _no_atual.posicao.y])
            return _no_atual.pega_caminho()
            # return True

        # espaco posicao inicial apenas para colocar no array de solucao
        if int(_temp_labirinto[_no_atual.posicao.x][_no_atual.posicao.y]) == 2:
            print(caminho_percorrido)
            caminho_percorrido.append([_no_atual.posicao.x, _no_atual.posicao.y])

        # espaco livre
        if int(_temp_labirinto[_no_atual.posicao.x][_no_atual.posicao.y]) != 2:
            _temp_labirinto[_no_atual.posicao.x][_no_atual.posicao.y] = 8
            caminho_percorrido.append([_no_atual.posicao.x, _no_atual.posicao.y])

        found = self.faz_busca_em_largura(_temp_labirinto,
                                          No(
                                              pai=_no_atual,
                                              posicao=Posicao(x=_no_atual.posicao.x - 1, y=_no_atual.posicao.y),
                                              saida=self.posicao_saida),
                                          caminho_percorrido,
                                          print_map) or \
                self.faz_busca_em_largura(_temp_labirinto,
                                          No(
                                              pai=_no_atual,
                                              posicao=Posicao(x=_no_atual.posicao.x + 1, y=_no_atual.posicao.y),
                                              saida=self.posicao_saida),
                                          caminho_percorrido,
                                          print_map) or \
                self.faz_busca_em_largura(_temp_labirinto,
                                          No(
                                              pai=_no_atual,
                                              posicao=Posicao(x=_no_atual.posicao.x, y=_no_atual.posicao.y - 1),
                                              saida=self.posicao_saida),
                                          caminho_percorrido,
                                          print_map) or \
                self.faz_busca_em_largura(_temp_labirinto,
                                          No(
                                              pai=_no_atual,
                                              posicao=Posicao(x=_no_atual.posicao.x, y=_no_atual.posicao.y + 1),
                                              saida=self.posicao_saida),
                                          caminho_percorrido,
                                          print_map)

        return found

    def faz_busca_com_informacao(self):
        """
        Faz busca com informacao/A*
        :return:
        """
        abertos = [No(posicao=self.posicao_atual, saida=self.posicao_saida)]
        fechados = []

        while len(abertos) > 0:
            for index, no_em_aberto in enumerate(abertos):
                abertos.pop(index)  # retirado estado mais a esquerda
                # print(no_em_aberto)

                if no_em_aberto == No(posicao=self.posicao_saida):
                    # return abertos
                    fechados.append(no_em_aberto)
                    # return fechados[-1].pega_caminho()
                    return no_em_aberto.pega_caminho()
                else:
                    # busca vizinhos/filhos retorna posicao da matriz deles
                    _filhos_do_no = self.__pega_vizinhos(
                        index_linha=no_em_aberto.posicao.x,
                        index_coluna=no_em_aberto.posicao.y,
                        tipo_lista=False
                    )
                    for posicao_filho in _filhos_do_no:
                        no_filho = No(
                            posicao=posicao_filho,
                            pai=no_em_aberto,
                            saida=self.posicao_saida
                        )

                        if no_filho not in abertos and no_filho not in fechados:
                            abertos.append(no_filho)
                            continue

                        if no_filho in abertos:
                            _index = abertos.index(no_filho)
                            _no = abertos[_index]
                            if no_filho.v_caminho <= _no.v_caminho:
                                abertos[_index] = no_filho
                            continue

                        if no_filho in fechados:
                            _index = fechados.index(no_filho)
                            _no = fechados[_index]
                            if no_filho.v_heuristico <= _no.v_heuristico:
                                fechados.pop(_index)
                                abertos.append(no_filho)
                            continue

                    fechados.append(no_em_aberto)
                    abertos.sort()

    @staticmethod
    def __criar_obstaculo(taxa=0.3):
        _random = random.random()
        return 1 if _random <= taxa else 0


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


if __name__ == '__main__':
    lab = Labirinto(
        dim_x=10,
        dim_y=10,
        taxa_obstaculos=.2
    )
    # lab.imprimir_labirinto()
    lab.desenha_labirinto()

    print(lab.faz_busca_em_largura(print_map=True))
    # print(lab.faz_busca_com_informacao())
